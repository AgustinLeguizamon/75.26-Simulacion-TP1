from .Semaforo import Semaforo
from .Movible import Movible
from enums import Direccion
from utils import velocidad_maxima_peaton

class Peaton(Movible):
    def __init__(self, direccion: Direccion, velocidad: float):
        super().__init__(direccion, velocidad)

    def es_peaton(self):
        return True

    # si la luz se pone en rojo y el peaton sigue en la calle, acelera a maxima velocidad
    def cambiar_estado(self, estado):
        if estado == Semaforo.ROJO:
            self.velocidad = velocidad_maxima_peaton()

    def get_dibujo(self):
        if self.direccion == Direccion.ESTE:
            return '◐'
        if self.direccion == Direccion.OESTE:
            return '◑'

        return super().get_dibujo()

    def __str__(self):
        return "Peaton"
