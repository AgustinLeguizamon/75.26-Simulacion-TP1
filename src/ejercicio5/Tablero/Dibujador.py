from .Celda import Celda
from Entidades.Semaforo import Semaforo
from .AreaEsperaPeaton import AreaEsperaPeaton

from enums import TipoDeCelda, Direccion

class Dibujador:
    def __init__(self):  
        pass

    def dibujar_tablero(self, celdas_matriz):
        for celdas_fila in celdas_matriz:
            # Imprimimos un salto de línea
            print() 
            for celda_fila in celdas_fila:
                # Imprimimos el dibujo de la celda
                print(celda_fila.get_dibujo(),end =" ")


