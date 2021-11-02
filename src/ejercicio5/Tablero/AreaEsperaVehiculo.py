from numpy import array
from Entidades.VehiculoParte import VehiculoParte
from Entidades.Poisson import Poisson
from enums import Direccion
from .Celda import Celda
from utils import velocidad_inicial_vehiculo, generar_color_random
import random as rn

class AreaEsperaVehiculo:
    VEHICULO_LARGO_CELDAS = 6
    VEHICULO_ANCHO_CELDAS = 5

    def __init__(self, celda_inicial: Celda, celda_matriz: list[list[Celda]], direccion_vehiculos: Direccion, vehiculos: dict[int,list[VehiculoParte]]):
        self.celda_inicial = celda_inicial
        self.celda_matriz = celda_matriz
        self.direccion_vehiculos = direccion_vehiculos
        self.vehiculos = vehiculos
        self.poisson = Poisson(0.05)

    # Chequeamos si hay que colocar un nuevo vehículo en el paso peatonal
    # Sino esperamos
    def accionar(self, semaforos: array, tiempo_transcurrido: float, segundos_por_paso: float):
        
        # Si las celdas donde creamos un nuevo auto estan ocupadas, no hago nada
        if (self.celdas_iniciales_estan_ocupadas()):
            return

        # Chequeo si hay arribo de vehículo según poisson, si no hay, no hago nada
        eventos_ocurridos = self.poisson.eventos_en_rango_de_tiempo(tiempo_transcurrido - segundos_por_paso, tiempo_transcurrido)
        if (eventos_ocurridos == 0):
            return

        # Creamos un auto completo en la celda de inicio
        self.crear_vehiculo_y_agregarlo_al_tablero(segundos_por_paso)

    def celdas_iniciales_estan_ocupadas(self) -> bool:
        celda_inicial_fila = self.celda_inicial.fila
        celda_inicial_columna = self.celda_inicial.columna
        hay_alguna_celda_ocupada = False
       
        for fila in range(self.VEHICULO_ANCHO_CELDAS):
            for columna in range(self.VEHICULO_LARGO_CELDAS):
                celda = self.celda_matriz[celda_inicial_fila + fila][celda_inicial_columna + columna]
                hay_alguna_celda_ocupada = hay_alguna_celda_ocupada or celda.esta_ocupada()

        return hay_alguna_celda_ocupada

    def crear_vehiculo_y_agregarlo_al_tablero(self, segundos_por_paso):
        celda_inicial_fila = self.celda_inicial.fila
        celda_inicial_columna = self.celda_inicial.columna
        velocidad = velocidad_inicial_vehiculo(segundos_por_paso)
        direccion = self.direccion_vehiculos
        color = generar_color_random()
        multiplicador = 1 if self.direccion_vehiculos == Direccion.NORTE else -1
        vehiculo_id = rn.randint(100, 999)
        self.vehiculos[vehiculo_id] = []

        for fila in range(self.VEHICULO_ANCHO_CELDAS):
            for columna in range(self.VEHICULO_LARGO_CELDAS):
                parte_de_vehiculo = VehiculoParte(vehiculo_id, direccion, velocidad, fila, columna, color)
                celda = self.celda_matriz[celda_inicial_fila + (fila * multiplicador)][celda_inicial_columna + columna]
                celda.agregar_entidad(parte_de_vehiculo)
                self.vehiculos[vehiculo_id].append(parte_de_vehiculo)

