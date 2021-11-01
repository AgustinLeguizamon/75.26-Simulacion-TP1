from enums import Direccion
from Entidades.Movible import Movible
from Entidades.VehiculoParte import VehiculoParte
from Tablero import Tablero

class Movedor:
    def __init__(self):
        pass
    
    def declarar_intencion(self, movible:Movible, tablero):
        fila_inicial = movible.get_fila()
        columna_inicial = movible.get_columna()
        direccion = movible.get_direccion()
        velocidad = movible.get_velocidad()
        
        # TODO: el peaton tiene que resolver a que celda se va a mover usando las reglas del paper
        # por ahora siempre se mueve hacia adelante
        # calculamos nueva posicion
        fila_final = fila_inicial + velocidad * direccion[Direccion.FILA]
        columna_final = columna_inicial + velocidad * direccion[Direccion.COLUMNA]
        # 

        # obtenemos celda final
        celda_final = tablero.get_celda(fila_final, columna_final)

        # indicamos a la celda final que un peaton tiene intenciones de moverse a ella
        celda_final.agregar_intencion(movible)

    def resolver_y_mover(self, tablero: Tablero):
        # Recorro todas las celdas que pertenecen al paso peatonal
        for fila in range(tablero._FILA_ORIGEN_PASO_PEATONAL, tablero._FILA_FIN_PASO_PEATONAL):
            for columna in range(tablero._COLUMNA_ORIGEN_PASO_PEATONAL, tablero._COLUMNA_FIN_PASO_PEATONAL):
                celda_paso_peatonal = tablero.get_celda(fila, columna)
                celda_paso_peatonal.resolver()


    # TODO: deprecated
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
