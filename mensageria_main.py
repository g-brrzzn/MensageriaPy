from imports_globais import *

logging.basicConfig(filename='registro_mensagens.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

class RelogioLogico:
    def __init__(self):
        self.timestamp = 0
        self.trava = threading.Lock()

    def tick(self):
        with self.trava:
            self.timestamp += 1
            return self.timestamp

relogio_global = RelogioLogico()

class Mensagem:
    def __init__(self, remetente, conteudo):
        self.remetente = remetente
        self.conteudo = conteudo
        self.ts_prod = relogio_global.tick()
        self.consumido_por = {}

    def adicionar_consumo(self, nome_consumidor):
        ts = relogio_global.tick()
        self.consumido_por[nome_consumidor] = ts
        return ts

    def __str__(self):
        return (f"De: {self.remetente} | Mensagem: '{self.conteudo}' | "
                f"TS_Prod: {self.ts_prod} | TS_Consumos: {self.consumido_por}")

class Usuario:
    def __init__(self, nome, corretor):
        self.nome = nome
        self.corretor = corretor
        self.caixa_de_entrada = queue.Queue()

    def enviar_mensagem(self, conteudo, canal, modo="unicast", alvos=None):
        msg = Mensagem(self.nome, conteudo)
        logging.info(f"Producao - {self.nome} enviou: '{conteudo}' | TS: {msg.ts_prod}")
        self.corretor.enfileirar(msg, canal, modo, alvos)

    def receber_mensagem(self, msg):
        ts_consumo = msg.adicionar_consumo(self.nome)
        self.caixa_de_entrada.put(msg)
        logging.info(f"Consumo - {self.nome} recebeu: '{msg.conteudo}' | TS: {ts_consumo}")

    def processar_caixa(self):
        while not self.caixa_de_entrada.empty():
            msg = self.caixa_de_entrada.get()
            print(f"[{self.nome}] Processando: {msg}")

class BrokerMensagens:
    def __init__(self):
        self.fila_mensagens = queue.Queue()
        self.canais = {}
        self.clientes = {}
        self.trava = threading.Lock()

    def registrar_cliente(self, usuario, canal="default"):
        with self.trava:
            self.clientes[usuario.nome] = usuario
            if canal not in self.canais:
                self.canais[canal] = []
            self.canais[canal].append(usuario)
            print(f"{usuario.nome} registrado no canal '{canal}'.")

    def remover_cliente(self, usuario, canal="default"):
        with self.trava:
            if usuario.nome in self.clientes:
                del self.clientes[usuario.nome]
            if canal in self.canais and usuario in self.canais[canal]:
                self.canais[canal].remove(usuario)
            print(f"{usuario.nome} removido do canal '{canal}'.")

    def enfileirar(self, msg, canal, modo, alvos):
        self.fila_mensagens.put((msg, canal, modo, alvos))

    def iniciar(self):
        threading.Thread(target=self._processar_mensagens, daemon=True).start()

    def _processar_mensagens(self):
        while True:
            try:
                msg, canal, modo, alvos = self.fila_mensagens.get(timeout=5)
                self._rotear_mensagem(msg, canal, modo, alvos)
            except queue.Empty:
                continue

    def _rotear_mensagem(self, msg, canal, modo, alvos):
        if modo == "unicast" and alvos:
            alvo = alvos[0]
            if alvo in self.clientes:
                threading.Thread(target=self.clientes[alvo].receber_mensagem, args=(msg,)).start()
        elif modo == "multicast" and alvos:
            for alvo in alvos:
                if alvo in self.clientes:
                    threading.Thread(target=self.clientes[alvo].receber_mensagem, args=(msg,)).start()
        elif modo == "broadcast":
            if canal in self.canais:
                for usuario in self.canais[canal]:
                    threading.Thread(target=usuario.receber_mensagem, args=(msg,)).start()
        else:
            print("Modo de envio inválido ou sem alvos especificados.")

def main():
    corretor = BrokerMensagens()
    corretor.iniciar()

    usuario1 = Usuario("Usuario1", corretor)
    usuario2 = Usuario("Usuario2", corretor)
    usuario3 = Usuario("Usuario3", corretor)
    usuario4 = Usuario("Usuario4", corretor)

    corretor.registrar_cliente(usuario1, canal="canal1")
    corretor.registrar_cliente(usuario2, canal="canal1")
    corretor.registrar_cliente(usuario3, canal="canal1")
    corretor.registrar_cliente(usuario4, canal="canal2")

    usuario1.enviar_mensagem("Mensagem Unicast de Usuario1 para Usuario2", "canal1", modo="unicast", alvos=["Usuario2"])
    usuario2.enviar_mensagem("Mensagem Multicast de Usuario2", "canal1", modo="multicast", alvos=["Usuario1", "Usuario3"])
    usuario3.enviar_mensagem("Mensagem Broadcast de Usuario3", "canal1", modo="broadcast")
    usuario4.enviar_mensagem("Mensagem Broadcast de Usuario4 em canal2", "canal2", modo="broadcast")

    time.sleep(3)

    usuario1.processar_caixa()
    usuario2.processar_caixa()
    usuario3.processar_caixa()
    usuario4.processar_caixa()

if __name__ == "__main__":
    main()
