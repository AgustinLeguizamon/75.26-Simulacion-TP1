from numpy import void
from Entidades.Movible import Movible
from Excepciones.celda_ocupada_excepcion import CeldaOcupadaExcepcion
from enums import TipoDeCelda

class Celda:
    def __init__(self, fila, columna, tipo, tablero, entidad: Movible = None):
        self.fila = fila
        self.columna = columna
        self.tipo = tipo
        self.entidad = entidad
        self.tablero = tablero
    
    def esta_ocupada(self) -> bool:
        return self.entidad != None

    def agregar_entidad(self, entidad: Movible) -> void:
        if self.entidad != None:
            raise CeldaOcupadaExcepcion
        
        self.entidad = entidad
        entidad.set_celda(self)
    
    def remover_entidad(self):
        self.entidad.set_celda(None)
        self.entidad = None

    def get_fila(self):
        return self.fila
    
    def get_columna(self):
        return self.columna
            
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
