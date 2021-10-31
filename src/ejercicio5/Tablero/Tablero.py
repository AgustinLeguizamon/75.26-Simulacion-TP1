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
        
        self.dibujador = Dibujador()
        self.movedor = Movedor()
        self.armador_tablero = ArmadorTablero(self)
        self.armador_tablero.armar_tablero()

        # definimos extremos del paso peatonal
        self._COLUMNA_ORIGEN_PASO_PEATONAL = self.armador_tablero.vereda_izquierda_largo + 1
        self._FILA_ORIGEN_PASO_PEATONAL = self.armador_tablero.parte_superior_ancho + 1
        self._COLUMNA_FIN_PASO_PEATONAL = self._COLUMNA_ORIGEN_PASO_PEATONAL + self.armador_tablero.calle_largo - 2
        self._FILA_FIN_PASO_PEATONAL = self._FILA_ORIGEN_PASO_PEATONAL + self.armador_tablero.parte_peatonal_ancho - 3

        self.celdas_matriz = self.armador_tablero.celdas_matriz
        self.semaforos = self.armador_tablero.semaforos
        self.vehiculos = self.armador_tablero.vehiculos
        self.peatones = self.armador_tablero.peatones
        self.areas_de_espera = self.armador_tablero.areas_de_espera
        
        pass

    def ejecutar_paso(self, tiempo):
        # Cambiamos estados de los semáforos
        for semaforo in self.semaforos:
            semaforo.cambiar_estado(tiempo)

        # Movemos a los peatones
        for peaton in self.peatones:
            self.movedor.mover(peaton, self)
        
        # for peaton in self.peatones:
        #    self.movedor.ejecuta(self)
    
        self.celdas_matriz[self._FILA_ORIGEN_PASO_PEATONAL][self._COLUMNA_ORIGEN_PASO_PEATONAL].tipo = 99
        self.celdas_matriz[self._FILA_FIN_PASO_PEATONAL][self._COLUMNA_FIN_PASO_PEATONAL].tipo = 99

        # Movemos a los vehiculos
        # for vehiculo in self.vehiculos:
        #    self.movedor.mover(vehiculo, self)

        # Chequeamos si tenemos que colocar peatones y/o vehículos
        # en las áreas de espera
        for area_espera in self.areas_de_espera:
            area_espera.accionar(self.semaforos, tiempo)
        
        # TODO: Resolver colisiones

        # Dibujamos las celdas
        self.dibujador.dibujar_tablero(self.celdas_matriz)

        self.dibujar_estadisticas()

        # Borramos peatones que salieron del tablero
        peatones_a_remover = [peaton for peaton in self.peatones if peaton.celda is None]
        for peaton in peatones_a_remover:
            self.peatones.remove(peaton)

        # Borramos vehiculos que salieron del tablero
        vehiculos_a_remover = [vehiculo for vehiculo in self.vehiculos if vehiculo.celda is None]
        for vehiculo in vehiculos_a_remover:
            self.vehiculos.remove(vehiculo)

    def get_celda(self, fila, columna) -> Celda or None:
        return self.armador_tablero.get_celda(fila, columna)

    def dibujar_estadisticas(self):
        print()
        print("Peatones en área de espera izquierda: ", self.areas_de_espera[0].peatones_esperando)
        print("Peatones en área de espera derecha: ", self.areas_de_espera[1].peatones_esperando)
