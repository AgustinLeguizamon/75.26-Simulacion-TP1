class Vehiculo:
    LARGO = 6
    ANCHO = 5

    def __init__(self, sentido):
        self.sentido = sentido
        self.velocidad = 1
        self.movibles = [Movible(sentido, 1) for i in range(self.LARGO * self.ANCHO)]
        self.x = -1
        self.y = -1
        self.paso = Paso(1 if Sentido.ESTE == sentido else -1, 0)
        self.esta_afuera = False

    def set_posicion(self, x, y):
        self.x = x
        self.y = y

    def asignar_celda(self, fila, columna, celda):
        pos = fila * self.ANCHO + columna
        celda.poner_movible(self.movibles[pos])

    def dar_paso(self, paso_peatonal):
        self.__salir_de_celdas()
        if paso_peatonal.puede_moverse(self.x + self.velocidad * self.paso.x, self.y):
            paso_peatonal.mover_vehiculo(self, self.paso.x, self.paso.y)
        else:
            # lo vuelvo a colocar en sus celdas
            paso_peatonal.mover_vehiculo(self, 0, 0)

    def estas_afuera(self):
        self.esta_afuera = True

    def __salir_de_celdas(self):
        # Primero levanta todos los elementos
        for movible in self.movibles:
            movible.salir_de_celda()
