from .Celda import Celda
from Entidades.Semaforo import Semaforo
from .AreaEsperaPeaton import AreaEsperaPeaton
from termcolor import colored

class Dibujador:
    def __init__(self):  
        pass

    def dibujar_tablero(self, celdas_matriz):
        print() 

        for celdas_fila in celdas_matriz:
            # Imprimimos un salto de línea
            print() 
            for celda_fila in celdas_fila:
                # Imprimimos el dibujo de la celda
                print(colored(celda_fila.get_dibujo(), celda_fila.get_dibujo_color()), end =" ")

        print() 


