from .Movible import Movible
from enums import Sentido

class Peaton(Movible):
    def __init__(self, sentido: Sentido, velocidad: float):
        super().__init__(sentido, velocidad)

    def get_dibujo(self):
        if self.sentido == Sentido.ESTE:
            return '◐'
        if self.sentido == Sentido.OESTE:
            return '◑'

        return super().get_dibujo()

    def __str__(self):
        return "Peaton"
