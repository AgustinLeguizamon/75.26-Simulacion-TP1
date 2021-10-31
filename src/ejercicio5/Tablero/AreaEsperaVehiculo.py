from numpy import array
from Entidades.Vehiculo import Vehiculo
from Entidades.Poisson import Poisson
from enums import Sentido
from .Celda import Celda
from utils import velocidad_inicial_vehiculo

class AreaEsperaVehiculo:

    def __init__(self, celda_inicial: Celda, sentido_vehiculos: Sentido, vehiculos: array):
        self.celda_inicial = celda_inicial
        self.sentido_vehiculos = sentido_vehiculos
        self.vehiculos = vehiculos
        self.poisson = Poisson()

    # Generamos un nuevo arribo de peaton según las condiciones establecidas
    # Retorna: verdadero si hay un arribo de vehiculo
    def hay_arribo_de_vehiculo(self, tiempo: float):
        tiempo_arribo = self.poisson.generar()
        ocurre_evento = tiempo_arribo < tiempo
        
        return ocurre_evento
    
    # Chequeamos si hay que colocar un nuevo vehículo en el paso peatonal
    # Sino esperamos
    def accionar(self, semaforos: array, tiempo: float):
        # Chequeo primero si la celda inicial está ocupada
        # Si lo está, no hago nada
        if (self.celda_inicial.esta_ocupada()):
            return

        # Luego chequeo si hay arribo de vehículo según poisson 
        # Si no hay, no hago nada

        # Agrego un vehículo en la celda inicial
        vehiculo = Vehiculo(self.sentido_vehiculos, velocidad_inicial_vehiculo())
        self.celda_inicial.agregar_entidad(vehiculo)


