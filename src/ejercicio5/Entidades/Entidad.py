from enums import Sentido

class Entidad:
    def __init__(self):
        self.celda = None

    def set_celda(self, celda):
        self.celda = celda

    def get_dibujo(self):
        return "?"

    def get_fila(self):
        return self.celda.get_fila()

    def get_columna(self):
        return self.celda.get_columna()
