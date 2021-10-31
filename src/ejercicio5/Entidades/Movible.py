from .Entidad import Entidad
from enums import Direccion

class Movible(Entidad):
    def __init__(self, direccion: Direccion, velocidad: float, color = None):
        super().__init__(color)
        self.direccion = direccion
        self.velocidad = velocidad

    def get_direccion(self):
        return self.direccion
    
    def get_velocidad(self):
        return self.velocidad
