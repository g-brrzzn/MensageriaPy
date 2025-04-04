from imports_globais import *
from broker_mensagens import BrokerMensagens
from usuario import Usuario

logging.basicConfig(filename='registro_mensagens.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

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
