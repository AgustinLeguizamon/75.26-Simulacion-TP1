from Excepciones.celda_ocupada_excepcion import CeldaOcupadaExcepcion
from enums import TipoDeCelda

class Celda:
    def __init__(self, fila, columna, tipo, tablero, entidad = None):
        self.fila = fila
        self.columna = columna
        self.tipo = tipo
        self.entidad = entidad
        self.tablero = tablero
    
    # para cuando se mueven las entidades en el paso peatonal
    def colocar_entidad(self, entidad):
        if self.entidad != None:
            raise CeldaOcupadaExcepcion
        entidad.set_celda(self)
        self.entidad = entidad

        
    # solo la puede llamar el AreaDeEspera
    def set_entidad(self, entidad):
        if self.entidad != None:
            return False
        self.colocar_entidad(entidad)
        return True
    
    def mover_movible(self, movible):
        self.tablero.move_movible_en(self.fila, self.columna, movible)
        # PIN
        #  salio_de_celda = 
        # if salio_de_celda:
        #    self.entidad = None
            
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
