import random

class Entidad:
    def __init__(self):
        self.celda = None
        self.color = self.generar_color_random()

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

    def generar_color_random(self):
        colores = ["grey", "red", "green", "yellow", "blue", "magenta", "cyan"]
        color_elegido = random.randint(0, len(colores) - 1)
        return colores[color_elegido]


