class Movible:
    def __init__(self, sentido, velocidad):
        self.celda = None
        self.sentido = sentido
        self.velocidad = velocidad

    def setear_celda(self, celda):
        self.celda = celda

    def dar_paso(self):
        self.celda.mover_movible(self.velocidad, self.sentido)

    def salir_de_celda(self):
        if self.celda is not None:
            self.celda.quitar_movible()
            self.celda = None

    def dibujar(self):
        if self.velocidad == 0:
            return 'x'
        if self.sentido == Sentido.NORTE:
            return '^'
        if self.sentido == Sentido.SUR:
            return 'v'
        if self.sentido == Sentido.ESTE:
            return '>'
        if self.sentido == Sentido.OESTE:
            return '<'
