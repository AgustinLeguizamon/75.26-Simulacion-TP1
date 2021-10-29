from enums import TipoDeCelda

class Celda:
    def __init__(self, x, y, tipo, entidad = None, paso_peatonal = None):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.entidad = entidad
        self.paso_peatonal = paso_peatonal

    def esta_ocupada(self) -> bool:
        return self.entidad != None

    def dibujar(self):
        if self.esta_ocupada():
            return self.entidad.dibujar()

        return self.get_dibujo()

    def get_dibujo(self):
        if (self.tipo == TipoDeCelda.NORMAL):
            return " "
        
        if (self.tipo == TipoDeCelda.VEREDA_CORDON):
            return "╎"
        
        if (self.tipo == TipoDeCelda.CARRIL_SEPARADOR):
            return "|"
        
        if (self.tipo == TipoDeCelda.SEPARADOR_PEATONAL):
            return "="

        if (self.tipo == TipoDeCelda.SEMAFORO):
            return "🟢"

        return "X"
