class Peaton(Movible):
    def __init__(self, id_peaton, sentido, velocidad):
        super().__init__(sentido, velocidad)
        self.id = id_peaton

    def dar_paso(self):
        self.celda.mover_peaton(self.velocidad, self.sentido)

    def actualizar_velocidad(self, d):
        self.velocidad = min(d, self.velocidad)
        return self.velocidad
