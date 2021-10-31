from enums import Direccion

class Movible:
    def __init__(self, direccion, velocidad):
        self.direccion = direccion
        self.velocidad = velocidad
        self.celda = None

    def set_celda(self, celda):
        self.celda = celda

    # def salir_de_celda(self):
    #    if self.celda is not None:
    #        self.celda.quitar_movible()
    #        self.celda = None

    def get_dibujo(self):
        if self.velocidad == 0:
            return 'x'
        if self.direccion == Direccion.NORTE:
            return '^'
        if self.direccion == Direccion.SUR:
            return 'v'
        if self.direccion == Direccion.ESTE:
            return '◐'
        if self.direccion == Direccion.OESTE:
            return '◑'

    def get_fila(self):
        return self.celda.get_fila()

    def get_columna(self):
        return self.celda.get_columna()
    
    def get_direccion(self):
        return self.direccion
    
    def get_velocidad(self):
        return self.velocidad
    
    def limpiar_celda(self):
        self.celda = None
