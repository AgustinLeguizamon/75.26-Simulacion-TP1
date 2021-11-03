from Entidades.Peaton import Peaton
from Entidades.Semaforo import Semaforo
from .Dibujador import Dibujador
from .Movedor import Movedor
from .ArmadorTablero import ArmadorTablero
from .Celda import Celda
from Estadisticas import Estadisticas
from .vehiculo_utils import borrar_vehiculos

class Tablero:

    def __init__(self, segundos_por_paso, area_izquierda_peatones=True, area_derecha_peatones=True):  
        self.segundos_por_paso = segundos_por_paso
        
        self.dibujador = Dibujador()
        self.movedor = Movedor()
        self.armador_tablero = ArmadorTablero(self)
        self.armador_tablero.armar_tablero(area_izquierda_peatones, area_derecha_peatones)

        self.celdas_matriz = self.armador_tablero.celdas_matriz
        self.semaforos = self.armador_tablero.semaforos
        self.vehiculos = self.armador_tablero.vehiculos
        self.peatones = self.armador_tablero.peatones
        self.areas_de_espera = self.armador_tablero.areas_de_espera

        # definimos extremos del paso peatonal
        self._COLUMNA_ORIGEN_PASO_PEATONAL = self.armador_tablero.vereda_izquierda_largo
        self._FILA_ORIGEN_PASO_PEATONAL = self.armador_tablero.parte_superior_ancho + 1
        self._COLUMNA_FIN_PASO_PEATONAL = self._COLUMNA_ORIGEN_PASO_PEATONAL + self.armador_tablero.calle_largo
        self._FILA_FIN_PASO_PEATONAL = self._FILA_ORIGEN_PASO_PEATONAL + self.armador_tablero.parte_peatonal_ancho - 3

        pass

    def ejecutar_paso(self, tiempo_transcurrido, segundos_por_paso):
        # fila_inicio_calle = 0
        # fila_fin_calle = len(self.celdas_matriz) - 1
        # columna_inicio_calle = self.armador_tablero.vereda_izquierda_largo
        # columna_fin_calle = columna_inicio_calle + self.armador_tablero.calle_largo
        # self.celdas_matriz[fila_inicio_calle][columna_inicio_calle].tipo = 99
        # self.celdas_matriz[self._FILA_FIN_PASO_PEATONAL][self._COLUMNA_FIN_PASO_PEATONAL].tipo = 99
        
        # Cambiamos estados de los semáforos
        for semaforo in self.semaforos:
            semaforo.cambiar_estado(tiempo_transcurrido, self)

        # Cada peaton declara a que celda se quiere mover
        self.movedor.declarar_intenciones_peatones(self)

        # Cada vehiculo declara a que celda se quiere mover
        vehiculos_id_a_borrar = self.movedor.declarar_intenciones_vehiculos(self)

        # Resolvemos colisiones y movemos los peatones
        self.movedor.resolver_intenciones_y_mover_movibles(self,tiempo_transcurrido)

        # Borramos vehiculos que ya se van
        borrar_vehiculos(vehiculos_id_a_borrar, self)

        # Chequeamos si tenemos que colocar peatones y/o vehículos
        # en las áreas de espera
        for area_espera in self.areas_de_espera:
            area_espera.accionar(self.semaforos, tiempo_transcurrido, segundos_por_paso)

        # Dibujamos las celdas
        self.dibujador.dibujar_tablero(self.celdas_matriz)

        self.dibujar_estadisticas()

        # Borramos peatones que salieron del tablero
        peatones_a_remover = [peaton for peaton in self.peatones if peaton.celda is None]
        for peaton in peatones_a_remover:
            ## agregar si esta en verde 1, rojo 0
            Estadisticas().guardar_cruce_completos([tiempo_transcurrido,1])
            self.peatones.remove(peaton)
    
    def estado_peatones(self, estado):
        for peaton in self.peatones:
            peaton.cambiar_estado(estado)

    def get_celda(self, fila, columna) -> Celda or None:
        return self.armador_tablero.get_celda(fila, columna)
    
    def pos_esta_en_paso_peatonal(self, fila, columna):
        return self._COLUMNA_ORIGEN_PASO_PEATONAL <= columna <= self._COLUMNA_FIN_PASO_PEATONAL and \
        self._FILA_ORIGEN_PASO_PEATONAL <= fila <= self._FILA_FIN_PASO_PEATONAL

    def dibujar_estadisticas(self):
        print()
        if (len(self.areas_de_espera) == 2): 
            print("Peatones en área de espera izquierda: ", self.areas_de_espera[0].peatones_esperando)
            print("Peatones en área de espera derecha: ", self.areas_de_espera[1].peatones_esperando)

    # debug only
    def _debug_colocar_peaton(self, fila_peatonal, columna_peatonal, direccion, velocidad):
        fila = fila_peatonal + self._FILA_ORIGEN_PASO_PEATONAL
        columna = columna_peatonal + self._COLUMNA_ORIGEN_PASO_PEATONAL

        celda = self.armador_tablero.get_celda(fila, columna)
        peaton = Peaton(direccion, velocidad)
        celda.agregar_entidad(peaton)
        self.peatones.append(peaton)
