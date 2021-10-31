from .Movible import Movible
from enums import Direccion

class Peaton(Movible):
    def __init__(self, direccion: Direccion, velocidad: float):
        super().__init__(direccion, velocidad)

    def get_dibujo(self):
        if self.direccion == Direccion.ESTE:
            return '◐'
        if self.direccion == Direccion.OESTE:
            return '◑'

        return super().get_dibujo()

    def __str__(self):
        return "Peaton"
