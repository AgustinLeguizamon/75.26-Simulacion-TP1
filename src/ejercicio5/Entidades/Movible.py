from .Entidad import Entidad
from enums import Direccion

class Movible(Entidad):
    def __init__(self, direccion: Direccion, velocidad: float, color = None):
        super().__init__(color)
        self.direccion = direccion
        self.velocidad = velocidad
        self.afuera = False

    def get_direccion(self):
        return self.direccion
    
    def get_velocidad(self):
        return self.velocidad
    
    def actualizar_velocidad(self, distancia):
        self.velocidad = min(distancia, self.velocidad)
        return self.velocidad
    
    def estas_afuera_paso_peatonal(self):
        self.afuera = True
