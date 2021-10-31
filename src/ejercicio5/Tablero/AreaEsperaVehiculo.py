from numpy import array
from Entidades.VehiculoParte import VehiculoParte
from Entidades.Poisson import Poisson
from enums import Direccion
from .Celda import Celda
from utils import velocidad_inicial_vehiculo, generar_color_random

class AreaEsperaVehiculo:
    VEHICULO_LARGO_CELDAS = 6
    VEHICULO_ANCHO_CELDAS = 5

    def __init__(self, celda_inicial: Celda, celda_matriz: list[list[Celda]], sentido_vehiculos: Direccion, vehiculos: list[VehiculoParte]):
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
        eventos_ocurridos = self.poisson.eventos_en_rango_de_tiempo(0, tiempo)
        if (eventos_ocurridos == 0):
            return

        # TODO: agregar autos por cantidad de eventos ocurridos

        celda_inicial_fila = self.celda_inicial.get_fila()
        celda_inicial_columna = self.celda_inicial.get_columna()

        # A cada vehículo ya agregado le agregamos las "partes faltantes"
        # dado que en la línea de arriba sólo le agregamos el pedazo superior
        # self.agregar_partes_faltantes_de_vehiculos_actuales()
        
        # Y si sobra espacio, agrego partes de vehiculos en las celda inicial y las columnas restantes
        # La fila_inicial_relativa es 0 porque es la parte de "arriba"
        if (self.celda_inicial.esta_ocupada()):
            return
            
        self.agregar_fila_con_partes_de_vehiculo(celda_inicial_fila, celda_inicial_columna, 0, generar_color_random())

    def agregar_partes_faltantes_de_vehiculos_actuales(self):
        for vehiculo in self.vehiculos:
            multiplicador = 1 if Direccion.SUR else -1
            
            # Chequeamos primero que no sea la última fila
            if (vehiculo.fila_relativa == (5 * multiplicador)):
                continue

            siguiente_fila_relativa = vehiculo.fila_relativa + (1 * multiplicador)

            # Chequeamos si la siguiente fila puede entrar en el mapa
            siguiente_fila = vehiculo.get_fila() + (1 * multiplicador)
            siguiente_fila_puede_entrar_en_el_mapa  = 0 < siguiente_fila < len(self.celda_matriz) - 1
            if (not siguiente_fila_puede_entrar_en_el_mapa):
                continue

            # Chequeamos si no hay nada en las celdas donde van a ir las partes
            celda_fila_inicial = self.celda_matriz[siguiente_fila][vehiculo.get_columna()]
            if (celda_fila_inicial.esta_ocupada()):
                continue

            self.agregar_fila_con_partes_de_vehiculo(siguiente_fila, vehiculo.get_columna(), siguiente_fila_relativa, vehiculo.get_dibujo_color())

    def agregar_fila_con_partes_de_vehiculo(self, fila_inicial_absoluta, columna_inicial_absoluta, fila_inicial_relativa, color_vehiculo):
        for i in range(self.VEHICULO_LARGO_CELDAS):
            columna_relativa = i
            vehiculo = VehiculoParte(self.sentido_vehiculos, velocidad_inicial_vehiculo(), fila_inicial_relativa, columna_relativa, color_vehiculo)
            celda = self.celda_matriz[fila_inicial_absoluta][columna_inicial_absoluta + columna_relativa]
            celda.agregar_entidad(vehiculo)
            self.vehiculos.append(vehiculo)
