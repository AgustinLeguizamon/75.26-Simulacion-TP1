import numpy as np
from Entidades.Movible import Movible
from Excepciones.celda_ocupada_excepcion import CeldaOcupadaExcepcion
from enums import TipoDeCelda
from Entidades.Peaton import Peaton
from random import choice
from Estadisticas import Estadisticas

class Celda:
    def __init__(self, fila, columna, tipo, tablero, entidad: Movible = None):
        self.fila = fila
        self.columna = columna
        self.tipo = tipo
        self.entidad = entidad
        self.tablero = tablero
        self.intenciones = []
    
    def esta_ocupada(self) -> bool:
        return (self.entidad != None)
    
    def tiene_peaton(self) -> bool:
        return (self.entidad and self.entidad.es_peaton())

    def agregar_entidad(self, entidad: Movible) -> np.void:
        if self.entidad != None:
           raise CeldaOcupadaExcepcion
        
        self.entidad = entidad
        entidad.set_celda(self)
    
    def remover_entidad(self):
        self.entidad = None
    
    # TODO: por ahora solo resuelve con peatones, pq capaz con vehiculos es distinto
    # TODO: podria hacer mas preguntas, mas que solo preguntar si esta ocupada
    # ¿El peaton esta a punto de salir del paso_peatonal? -> entonces si podria agregar la intencion, pq la celda va a estar vacia
    # ¿Paper: el peaton que esta en esta celda piensa moverse a la celda del de la intencion? Podrian intercambiar celdas
    def agregar_intencion(self, entidad, celdas_asociadas = []):
        # no deberia declarar intencion de moverse a una celda que esta ocupada (por ahora)
        if self.entidad == None:
            self.intenciones.append(entidad)
    
    # Elige entidades al azar y lo coloca en la celda
    def resolver(self,tiempo_transcurrido):
        # Si el peaton que esta en la celda del paso peatonal tiene intenciones de salir, lo elimino de la celda
        if self.entidad != None and self.entidad.afuera:
            self.entidad.set_celda(None)

        # Si la celda está ocupada, no hacemos nada
        if self.entidad != None:
            return

        if len(self.intenciones) == 0:
            return

        if len(self.intenciones) == 1:
            self.agregar_entidad(self.intenciones[0])
            self.intenciones = []
            return

        # Elegimos una entidad al azar
        Estadisticas().guardar_conflicto([tiempo_transcurrido, 1])
        entidad_seleccionada = choice(self.intenciones)
        self.agregar_entidad(entidad_seleccionada)
        self.intenciones = []

    # TODO: no se usa, borrar?
    def encontrar_vehiculo(elementos: 'list[Movible]', vehiculos_id: 'list[int]'):
        for item in elementos:
            vehiculo = [item for item in elementos if x["id"] == 1 ][0]

    def marcar_peaton_si_fuera_de_peatonal(self, movible, tablero):
        if not tablero.pos_esta_en_paso_peatonal(self.fila, self.columna):
            movible.estas_afuera_paso_peatonal()

    def get_fila(self):
        return self.fila
    
    def get_columna(self):
        return self.columna
            
    def get_dibujo(self):
        if self.esta_ocupada():
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

    def get_dibujo_color(self):
        if self.esta_ocupada():
            return self.entidad.get_dibujo_color()

        return "white"

    