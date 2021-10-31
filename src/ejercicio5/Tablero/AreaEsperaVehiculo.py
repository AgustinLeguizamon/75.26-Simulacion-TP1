from numpy import array
from Entidades.VehiculoParte import VehiculoParte
from Entidades.Poisson import Poisson
from enums import Sentido
from .Celda import Celda
from utils import velocidad_inicial_vehiculo, generar_color_random

class AreaEsperaVehiculo:
    VEHICULO_LARGO_CELDAS = 6

    def __init__(self, celda_inicial: Celda, celda_matriz: list[list[Celda]], sentido_vehiculos: Sentido, vehiculos: array):
        self.celda_inicial = celda_inicial
        self.celda_matriz = celda_matriz
        self.sentido_vehiculos = sentido_vehiculos
        self.vehiculos = vehiculos
        self.poisson = Poisson()

    # Chequeamos si hay que colocar un nuevo vehículo en el paso peatonal
    # Sino esperamos
    def accionar(self, semaforos: array, tiempo: float):
        # Chequeo primero si la celda inicial está ocupada
        # Si lo está, no hago nada
        if (self.celda_inicial.esta_ocupada()):
            return

        # Luego chequeo si hay arribo de vehículo según poisson 
        # Si no hay, no hago nada
        ocurre_evento = self.poisson.ocurrio_nuevo_evento(tiempo)
        if (not ocurre_evento):
            return

        celda_inicial_fila = self.celda_inicial.get_fila()
        celda_inicial_columna = self.celda_inicial.get_columna()

        # Agrego partes de vehiculos en las celda inicial y las columnas restantes (6)
        color_vehiculo = generar_color_random()
        for i in range(self.VEHICULO_LARGO_CELDAS):
            fila_relativa = 0
            columna_relativa = i
            vehiculo = VehiculoParte(self.sentido_vehiculos, velocidad_inicial_vehiculo(), fila_relativa, columna_relativa, color_vehiculo)
            celda = self.celda_matriz[celda_inicial_fila + fila_relativa][celda_inicial_columna + columna_relativa]
            celda.agregar_entidad(vehiculo)
            self.vehiculos.append(vehiculo)



