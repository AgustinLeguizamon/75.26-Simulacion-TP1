from .Dibujador import Dibujador
from .Movedor import Movedor
from .ArmadorTablero import ArmadorTablero
from .Celda import Celda

class Tablero:

    def __init__(self, calle_largo = 21, paso_peatonal_ancho = 3, cantidad_de_carriles = 6, ancho_carril = 3.5, ancho_celda = 0.5):  
        self.calle_largo = calle_largo
        self.paso_peatonal_ancho = paso_peatonal_ancho
        self.cantidad_de_carriles = cantidad_de_carriles
        self.ancho_carril = ancho_carril
        self.ancho_celda = ancho_celda
        
        self._COLUMNA_ORIGEN_PASO_PEATONAL = 0
        self._FILA_ORIGEN_PASO_PEATONAL = 0
        
        self.dibujador = Dibujador()
        self.movedor = Movedor()

        armador_tablero = ArmadorTablero(self)
        armador_tablero.armar_tablero()
        self.celdas_matriz = armador_tablero.celdas_matriz
        self.semaforos = armador_tablero.semaforos
        self.vehiculos = armador_tablero.vehiculos
        self.peatones = armador_tablero.peatones
        self.areas_de_espera = armador_tablero.areas_de_espera
        
        pass

    def ejecutar_paso(self, tiempo):
        # Cambiamos estados de los semáforos
        for semaforo in self.semaforos:
            semaforo.cambiar_estado(tiempo)

        # Chequeamos si tenemos que colocar peatones y/o vehículos
        # en las áreas de espera
        for area_espera in self.areas_de_espera:
            area_espera.accionar(self.semaforos, tiempo)

        # Movemos a los peatones
        for peaton in self.peatones:
            self.movedor.mover(peaton, self)

        # Movemos a los vehiculos
        for vehiculo in self.vehiculos:
            self.movedor.mover(vehiculo, self)

        # TODO: Resolver colisiones

        # Dibujamos las celdas
        self.dibujador.dibujar_tablero(self.celdas_matriz)

        # Borramos peatones que salieron del tablero
        peatones_a_remover = [peaton for peaton in self.peatones if peaton.celda is None]
        for peaton in peatones_a_remover:
            self.peatones.remove(peaton)

        # Borramos vehiculos que salieron del tablero
        vehiculos_a_remover = [vehiculo for vehiculo in self.vehiculos if vehiculo.celda is None]
        for vehiculo in vehiculos_a_remover:
            self.vehiculos.remove(vehiculo)

    def get_celda(self, fila, columna) -> Celda:
        if 0 <= fila < len(self.celdas_matriz) and 0 <= columna < len(self.celdas_matriz[0]):
            return self.celdas_matriz[fila][columna]
        return None
