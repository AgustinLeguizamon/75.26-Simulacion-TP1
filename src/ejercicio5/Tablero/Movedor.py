from enums import Direccion


class Movedor:
    def __init__(self):
        pass
    
    def mover(self, movible, tablero):
        fila = movible.get_fila()
        columna = movible.get_columna()
        direccion = movible.get_direccion()
        velocidad = movible.get_velocidad()
        
        # calculamos nueva posicion
        fila_final = fila + velocidad * direccion[Direccion.FILA]
        columna_final = columna + velocidad * direccion[Direccion.COLUMNA]

        # obtenemos celdas
        celda_inicial = tablero.get_celda(fila, columna)
        celda_final = tablero.get_celda(fila_final, columna_final)
        
        # si se va de la matriz
        if celda_final == None:
            celda_inicial.limpiar_entidad()
            return

        # si esta ocupada, no me muevo
        if celda_final.entidad != None:
            return

        # si no esta ocupada, me muevo
        celda_inicial.limpiar_entidad() 
        celda_final.colocar_entidad(movible)
