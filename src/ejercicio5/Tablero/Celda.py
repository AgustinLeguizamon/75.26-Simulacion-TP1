from numpy import void
from Entidades.Movible import Movible
from Excepciones.celda_ocupada_excepcion import CeldaOcupadaExcepcion
from enums import TipoDeCelda
from Entidades.Peaton import Peaton
from random import choice

class Celda:
    def __init__(self, fila, columna, tipo, tablero, entidad: Movible = None):
        self.fila = fila
        self.columna = columna
        self.tipo = tipo
        self.entidad = entidad
        self.tablero = tablero
        self.intenciones = []
    
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
    
    # TODO: por ahora solo resuelve con peatones, pq capaz con vehiculos es distinto
    # no deberia declarar intencion de moverse a una celda que esta ocupada
    def agregar_intencion(self, peaton: Peaton):
        if self.entidad == None:
            self.intenciones.append(peaton)
    
    
    # elige algun peaton al azar y lo coloca en la celda
    def resolver(self):
        if len(self.intenciones) > 0:
            peaton = choice(self.intenciones)
            self.agregar_entidad(peaton)
            self.intenciones = []

    def get_fila(self):
        return self.fila
    
    def get_columna(self):
        return self.columna
            
    def get_dibujo(self):
        if self.esta_ocupada():
            return self.entidad.get_dibujo()

        if (self.tipo == TipoDeCelda.NORMAL):
            return "-"
        
        if (self.tipo == TipoDeCelda.VEREDA_CORDON):
            return "╎"
        
        if (self.tipo == TipoDeCelda.CARRIL_SEPARADOR):
            return "|"

        if (self.tipo == TipoDeCelda.CARRIL_SEPARADOR_DEL_MEDIO):
            return "║"
        
        if (self.tipo == TipoDeCelda.SEPARADOR_PEATONAL):
            return "="

        return "X"

    def get_dibujo_color(self):
        if self.esta_ocupada():
            return self.entidad.get_dibujo_color()

        return "white"

    