from imports_globais import *
from relogio_logico import relogio_global

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
