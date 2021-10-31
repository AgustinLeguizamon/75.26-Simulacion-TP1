from .Movible import Movible

class Peaton(Movible):
    def __init__(self, id_peaton, direccion, velocidad):
        super().__init__(direccion, velocidad)
        self.id = id_peaton

    # def dar_paso(self):
    #     self.celda.mover_peaton(self.velocidad, self.direccion)

    # def actualizar_velocidad(self, d):
    #    self.velocidad = min(d, self.velocidad)
    #    return self.velocidad
