from Entidades.Peaton import Peaton
from enums import Sentido
from .Celda import Celda
from Entidades.Poisson import Poisson
from utils import velocidad_inicial_vehiculo

class AreaEsperaVehiculo:

    def __init__(self, celda_inicial: Celda, sentido: Sentido):
        self.celda_inicial = celda_inicial
        self.sentido = sentido
        self.poisson = Poisson()

    # Generamos un nuevo arribo de peaton según las condiciones establecidas
    # Retorna: verdadero si hay un arribo de vehiculo
    def hay_arribo_de_vehiculo(self, tiempo):
        tiempo_arribo = self.poisson.generar()
        ocurre_evento = tiempo_arribo < tiempo
        
        return ocurre_evento
    
    # Chequeamos si hay que colocar un nuevo vehículo en el paso peatonal
    # Sino esperamos
    def accionar(self, semaforos, tiempo):
        # TODO: remove
        self.celda_inicial.tipo = 99
        
        # Chequeo primero si la celda inicial está ocupada
        # Si lo está, no hago nada

        # Luego chequeo si hay arribo de vehículo según poisson 
        # Si no hay, no hago nada

        # Agrego un vehículo en la celda inicial



        


