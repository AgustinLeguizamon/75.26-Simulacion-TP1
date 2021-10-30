from enums import TipoDeCelda

class Celda:
    def __init__(self, x, y, tipo, entidad = None):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.entidad = entidad

    def get_dibujo(self):
        esta_ocupada = self.entidad != None
        
        if esta_ocupada:
            return self.entidad.get_dibujo()

        if (self.tipo == TipoDeCelda.NORMAL):
            return " "
        
        if (self.tipo == TipoDeCelda.VEREDA_CORDON):
            return "╎"
        
        if (self.tipo == TipoDeCelda.CARRIL_SEPARADOR):
            return "|"

        if (self.tipo == TipoDeCelda.CARRIL_SEPARADOR_DEL_MEDIO):
            return "║"
        
        if (self.tipo == TipoDeCelda.SEPARADOR_PEATONAL):
            return "="

        return "X"
