from utils import generar_color_random

class Entidad:
    def __init__(self, color = generar_color_random()):
        self.celda = None
        self.color = color

    def set_celda(self, celda):
        self.celda = celda

    def get_dibujo(self):
        return "?"
    
    def get_dibujo_color(self):
        return self.color

    def get_fila(self):
        return self.celda.get_fila()

    def get_columna(self):
        return self.celda.get_columna()


