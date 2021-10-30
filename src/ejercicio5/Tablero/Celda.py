from Excepciones.celda_ocupada_excepcion import CeldaOcupadaExcepcion
from enums import TipoDeCelda

class Celda:
    def __init__(self, fila, columna, tipo, entidad = None):
        self.fila = fila
        self.columna = columna
        self.tipo = tipo
        self.entidad = entidad
    
    # para cuando se mueven las entidades en el paso peatonal
    def colocar_entidad(self, entidad):
        if self.entidad != None:
            raise CeldaOcupadaExcepcion
        self.entidad = entidad
        
    # solo la puede llamar el AreaDeEspera
    def set_entidad(self, entidad):
        if self.entidad != None:
            return False
        self.colocar_entidad(entidad)
        return True

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

    def ocupar(self, tipo):
        self.tipo = tipo

    def esta_ocupada(self):
        return self.tipo != " "
