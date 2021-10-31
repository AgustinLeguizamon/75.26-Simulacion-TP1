from .Entidad import Entidad
from enums import Sentido

class Movible(Entidad):
    def __init__(self, sentido: Sentido, velocidad: float, color = None):
        super().__init__(color)
        self.sentido = sentido
        self.velocidad = velocidad

    def get_sentido(self):
        return self.sentido
    
    def get_velocidad(self):
        return self.velocidad
