from enums import Direccion
from Entidades.Movible import Movible
from Entidades.VehiculoParte import VehiculoParte

class Movedor:
    def __init__(self):
        pass
    
    def mover(self, movible: Movible, tablero):
        fila_inicial = movible.get_fila()
        columna_inicial = movible.get_columna()
        direccion = movible.get_direccion()
        velocidad = movible.get_velocidad()
        
        # calculamos nueva posicion
        fila_final = fila_inicial + velocidad * direccion[Direccion.FILA]
        columna_final = columna_inicial + velocidad * direccion[Direccion.COLUMNA]

        # obtenemos celdas iniciales y finales
        celda_inicial = tablero.get_celda(fila_inicial, columna_inicial)
        celda_final = tablero.get_celda(fila_final, columna_final)
        
        # si se va de la matriz o no tiene celda final, lo removemos
        if celda_final == None:
            celda_inicial.remover_entidad()
            return

        # si la celda final está ocupada, no me muevo
        if celda_final.esta_ocupada():
            return

        # si no esta ocupada, me muevo
        celda_inicial.remover_entidad() 
        celda_final.agregar_entidad(movible)
