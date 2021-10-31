from .Movible import Movible
from enums import Sentido

class Vehiculo(Movible):
    LARGO_CELDAS = 6
    ANCHO_CELDAS = 5

    def __init__(self, sentido: Sentido, velocidad: float):
        super().__init__(sentido, velocidad)

    def get_dibujo(self):
        if self.sentido == Sentido.SUR:
            return 'v'
        if self.sentido == Sentido.NORTE:
            return '^'
