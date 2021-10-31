from enums import Sentido
from Entidades.Movible import Movible

class Movedor:
    def __init__(self):
        pass
    
    def mover(self, movible: Movible, tablero):
        fila_inicial = movible.get_fila()
        columna_inicial = movible.get_columna()
        sentido = movible.get_sentido()
        velocidad = movible.get_velocidad()
        
        # calculamos nueva posicion
        fila_final = fila_inicial + (velocidad * (1 if sentido == Sentido.SUR else -1 if sentido == Sentido.NORTE else 0))
        columna_final = columna_inicial + (velocidad * (1 if sentido == Sentido.ESTE else -1 if sentido == Sentido.OESTE else 0))

        # obtenemos celdas
        celda_inicial = tablero.get_celda(fila_inicial, columna_inicial)
        celda_final = tablero.get_celda(fila_final, columna_final)
        
        # si se va de la matriz
        if celda_final == None:
            celda_inicial.remover_entidad()
            return

        # si esta ocupada, no me muevo
        if celda_final.esta_ocupada():
            return

        # si no esta ocupada, me muevo
        celda_inicial.remover_entidad() 
        celda_final.agregar_entidad(movible)
