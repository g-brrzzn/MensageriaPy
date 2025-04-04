from imports_globais import *
from mensagem import Mensagem

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
