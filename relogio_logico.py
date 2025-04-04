from imports_globais import *

class RelogioLogico:
    def __init__(self):
        self.timestamp = 0
        self.trava = threading.Lock()

    def tick(self):
        with self.trava:
            self.timestamp += 1
            return self.timestamp

relogio_global = RelogioLogico()
