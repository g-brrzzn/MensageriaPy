from imports_globais import *

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
