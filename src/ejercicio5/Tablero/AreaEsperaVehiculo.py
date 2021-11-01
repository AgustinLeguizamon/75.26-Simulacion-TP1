from numpy import array
from Entidades.VehiculoParte import VehiculoParte
from Entidades.Poisson import Poisson
from enums import Direccion
from .Celda import Celda
from utils import velocidad_inicial_vehiculo, generar_color_random

class AreaEsperaVehiculo:

    def __init__(self, celda_inicial: Celda, celda_matriz: list[list[Celda]], direccion_vehiculos: Direccion, vehiculos: list[VehiculoParte], poisson: Poisson):
        self.celda_inicial = celda_inicial
        self.celda_matriz = celda_matriz
        self.direccion_vehiculos = direccion_vehiculos
        self.vehiculos = vehiculos
        self.poisson = poisson

    # Chequeamos si hay que colocar un nuevo vehículo en el paso peatonal
    # Sino esperamos
    def accionar(self, semaforos: array, tiempo: float):
        # Si la celda inicial está ocupada no hago nada
        if (self.celda_inicial.esta_ocupada()):
            return

        # Chequeo si hay arribo de vehículo según poisson, si no hay, no hago nada
        eventos_ocurridos = self.poisson.eventos_en_rango_de_tiempo(0, tiempo)
        if (eventos_ocurridos == 0):
            return

        if (self.direccion_vehiculos == Direccion.SUR):
            return
        
        # Agregamos una fila con partes de vehiculo, 1 fila por iteración
        if (not self.celda_inicial.esta_ocupada()):
            vehiculo = Vehiculo(self.direccion_vehiculos, velocidad_inicial_vehiculo(), generar_color_random()) if len(self.vehiculos_incompletos) == 0 else self.vehiculos_incompletos[0]
            vehiculo.agregar_siguiente_fila_al_tablero(self.celda_matriz, self.celda_inicial.get_fila(), self.celda_inicial.get_columna(), self.vehiculos)

            # Si not tiene filas para dibujar, lo removemos de la lista de "vehiculos incompletos"
            if (not vehiculo.tiene_filas_para_dibujar()):
                self.vehiculos_incompletos.remove(vehiculo)
            else:
                # Si todavia tiene, y no fue agregado a esa lista, lo agregamos
                if (vehiculo not in self.vehiculos_incompletos):
                    self.vehiculos_incompletos.append(vehiculo)

           
class Vehiculo:
    VEHICULO_LARGO_CELDAS = 6
    VEHICULO_ANCHO_CELDAS = 5

    def __init__(self, direccion, velocidad, color):
        self.direccion = direccion
        self.velocidad = velocidad
        self.color = color

        self.partes_de_vehiculo: list[list[VehiculoParte]] = []

        self.crear_partes_vehiculo()

    def crear_partes_vehiculo(self):
        # Creamos todas las partes del vehiculo
        for fila_relativa in range(self.VEHICULO_ANCHO_CELDAS):
            partes_de_vehiculo_en_la_fila = []

            for columna_relativa in range(self.VEHICULO_LARGO_CELDAS):
                parte_de_vehiculo = VehiculoParte(self.direccion, self.velocidad, fila_relativa, columna_relativa, self.color)
                partes_de_vehiculo_en_la_fila.append(parte_de_vehiculo)

            self.partes_de_vehiculo.append(partes_de_vehiculo_en_la_fila)

    def tiene_filas_para_dibujar(self):
        return len(self.partes_de_vehiculo) > 0

    def agregar_siguiente_fila_al_tablero(self, celda_matriz, celda_inicial_fila, celda_inicial_columna, vehiculos):
        siguiente_fila_a_dibujar = self.partes_de_vehiculo.pop(0)
        
        for parte_de_vehiculo in siguiente_fila_a_dibujar:
            celda = celda_matriz[celda_inicial_fila][celda_inicial_columna + parte_de_vehiculo.columna_relativa]
            celda.agregar_entidad(parte_de_vehiculo)
            vehiculos.append(parte_de_vehiculo)

