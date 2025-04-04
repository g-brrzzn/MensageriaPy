from imports_globais import *
from broker_mensagens import BrokerMensagens
from usuario import Usuario

class TesteMensageria(unittest.TestCase):
    def setUp(self):
        self.corretor = BrokerMensagens()
        self.corretor.iniciar()
        self.usuario1 = Usuario("Usuario1", self.corretor)
        self.usuario2 = Usuario("Usuario2", self.corretor)
        self.usuario3 = Usuario("Usuario3", self.corretor)
        self.usuario4 = Usuario("Usuario4", self.corretor)
        self.corretor.registrar_cliente(self.usuario1, canal="canal1")
        self.corretor.registrar_cliente(self.usuario2, canal="canal1")
        self.corretor.registrar_cliente(self.usuario3, canal="canal1")
        self.corretor.registrar_cliente(self.usuario4, canal="canal2")

    def test_unicast(self):
        self.usuario1.enviar_mensagem("Teste Unicast", "canal1", modo="unicast", alvos=["Usuario2"])
        time.sleep(1)
        self.assertTrue(self.usuario2.caixa_de_entrada.qsize() >= 1)
        self.assertEqual(self.usuario1.caixa_de_entrada.qsize(), 0)
        self.assertEqual(self.usuario3.caixa_de_entrada.qsize(), 0)

    def test_multicast(self):
        self.usuario2.enviar_mensagem("Teste Multicast", "canal1", modo="multicast", alvos=["Usuario1", "Usuario3"])
        time.sleep(1)
        self.assertTrue(self.usuario1.caixa_de_entrada.qsize() >= 1)
        self.assertTrue(self.usuario3.caixa_de_entrada.qsize() >= 1)
        self.assertEqual(self.usuario2.caixa_de_entrada.qsize(), 0)

    def test_broadcast(self):
        self.usuario3.enviar_mensagem("Teste Broadcast", "canal1", modo="broadcast")
        time.sleep(1)
        self.assertTrue(self.usuario1.caixa_de_entrada.qsize() >= 1)
        self.assertTrue(self.usuario2.caixa_de_entrada.qsize() >= 1)
        self.assertTrue(self.usuario3.caixa_de_entrada.qsize() >= 1)

    def test_broadcast_canal_diferente(self):
        self.usuario4.enviar_mensagem("Teste Broadcast Canal2", "canal2", modo="broadcast")
        time.sleep(1)
        self.assertTrue(self.usuario4.caixa_de_entrada.qsize() >= 1)
        self.assertEqual(self.usuario1.caixa_de_entrada.qsize(), 0)

if __name__ == "__main__":
    unittest.main()
