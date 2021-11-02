from utils import generar_color_random

class Entidad:
    def __init__(self, color = None):
        self.celda = None
        self.color = color if color != None else generar_color_random()

    def remover_celda(self):
        self.celda = None

    def set_celda(self, celda):
        if self.celda != None:
            self.celda.remover_entidad()
        self.celda = celda

    def es_peaton(self):
        return False

    def get_dibujo(self):
        return "?"
    
    def get_dibujo_color(self):
        return self.color

    def get_fila(self):
        return self.celda.get_fila()

    def get_columna(self):
        return self.celda.get_columna()


