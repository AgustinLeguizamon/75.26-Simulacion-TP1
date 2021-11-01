from enums import Direccion, Regla
from Entidades.Movible import Movible
from Entidades.Peaton import Peaton
from Entidades.VehiculoParte import VehiculoParte
from Tablero import Tablero
from random import random

class Movedor:
    INF = 99

    def __init__(self):
        pass

    def probabilidad(proba):
        p = random.random()
        return p < proba
    
    def declarar_intencion(self, movible:Movible, tablero):
        fila_inicial = movible.get_fila()
        columna_inicial = movible.get_columna()
        direccion = movible.get_direccion()
        velocidad = movible.get_velocidad()
        
        
        # TODO: el peaton tiene que resolver a que celda se va a mover usando las reglas del paper
        # por ahora siempre se mueve hacia adelante
        # calculamos nueva posicion
        fila_final, columna_final = self.calcular_pos_celda_final(fila_inicial, columna_inicial, velocidad, direccion, tablero, movible)
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
        
        # TODO: todos los peatones que hayan declarado intencioens sobre celdas
        # que NO pertenecen al paso peatonal se marcan para ser eliminados


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


    def calcular_pos_celda_final(self, fila_peaton, columna_peaton, velocidad, direccion, tablero, peaton: Peaton):
        d = self.distancia_al_prox_peaton(fila_peaton, columna_peaton, direccion, tablero)
        movimiento_lateral = 0
        regla_a_aplicar = self.resolver_cambio_de_linea_de_peaton_en(fila_peaton, columna_peaton, velocidad, direccion, tablero)
        if regla_a_aplicar == Regla.AMBOS:
            movimiento_lateral += 1 if self.probabilidad(0.5) else -1
        elif regla_a_aplicar == Regla.DER:
            movimiento_lateral += direccion[Direccion.COLUMNA]
        elif regla_a_aplicar == Regla.IZQ:
            movimiento_lateral -= direccion[Direccion.COLUMNA]
        if regla_a_aplicar != Regla.NINGUNA:
            # Recalculo distancia despues de resolver conflicto
            d = self.distancia_al_prox_peaton(fila_peaton, columna_peaton, direccion, tablero)
        # el peaton en este turno no se mueve si no puedo resolver el conflicto, pero mantiene la velocidad
        velocidad = 0
        if regla_a_aplicar != Regla.NO_RESUELTO:
            # si resulta que no hubo conflicto, actualizo la velocidad
            velocidad = peaton.actualizar_velocidad(d)
    
        return fila_peaton + movimiento_lateral, columna_peaton + velocidad * direccion[Direccion.COLUMNA]

    
    def distancia_al_prox_peaton(self, fila_peaton, columna_peaton, direccion, tablero: Tablero):
        d = 0

        # el limite es el fin del paso peatonal, por defecto tomo sentido ESTE
        limite = tablero._COLUMNA_FIN_PASO_PEATONAL
        hay_peaton_adelante = False
        
        # si la direccion es el OESTE, entonces el limite es el principio del paso peatonal
        if direccion == Direccion.OESTE:
            limite = tablero._COLUMNA_ORIGEN_PASO_PEATONAL

        col_celda_de_adelante = columna_peaton + direccion[Direccion.COLUMNA]
        for columna in range(col_celda_de_adelante, limite, direccion[Direccion.COLUMNA]):
            if tablero.get_celda(fila_peaton, columna).esta_ocupada():
                hay_peaton_adelante = True
                break
            d += 1

        # si resulta que no hay nadie adelante, la distancia es inf
        if not hay_peaton_adelante:
            d = self.INF
        return d

    def resolver_cambio_de_linea_de_peaton_en(self, fila_peaton, columna_peaton, velocidad, sentido, tablero: Tablero):
        if velocidad == 0:
            return Regla.NINGUNA

        # si tiene uno adelante:
        # condicion1 = Celda(x,y-1).ocupada
        condicion1 = self.distancia_al_prox_peaton(fila_peaton, columna_peaton, sentido, tablero) == 0

        # si no se cumple la condicion de conflicto, break
        if not condicion1:
            return Regla.NINGUNA

        # defino que es derecha e izquierda segun el sentido
        derecha = 1
        if sentido == Direccion.OESTE:
            derecha = -1
        izquierda = -derecha

        # a la derecha y a la izquierda esta vacio:
        # condicion2 = not Celda(x-1,y).ocupada and not Celda(x+1,y).ocupada
        tiene_carril_der = tablero._FILA_ORIGEN_PASO_PEATONAL <= (fila_peaton + derecha) < tablero._FILA_FIN_PASO_PEATONAL
        tiene_carril_izq = tablero._FILA_ORIGEN_PASO_PEATONAL <= (fila_peaton + izquierda) < tablero._FILA_FIN_PASO_PEATONAL
        tiene_vecino_der = tiene_carril_der and tablero.get_celda(fila_peaton, columna_peaton + derecha).esta_ocupada()
        tiene_vecino_izq = tiene_carril_izq and tablero.get_celda(fila_peaton, columna_peaton + izquierda).esta_ocupada()

        if tiene_vecino_izq and tiene_vecino_der:
            # TODO: ver enums Regla
            return Regla.NO_RESUELTO

        # la distancia al vecino lateral mas cercano es mayor a su velocidad actual
        # condicion3 = distancia_al_prox_vecino_izq_adelante() > mi_velocidad
        # condicion4 = distancia_al_prox_vecino_der_adelante() > mi_velocidad
        condicion3 = tiene_carril_izq and self.distancia_al_prox_peaton(fila_peaton + izquierda, columna_peaton, sentido, tablero) > velocidad
        condicion4 = tiene_carril_der and self.distancia_al_prox_peaton(fila_peaton + derecha, columna_peaton, sentido, tablero) > velocidad

        # 'velocidad de los primeros vecinos laterales que estan n celdas mas atras' es
        # menor a mi velocidad actual
        # distancia_al_prox_vecino_der_atras() > mi_velocidad
        # distancia_al_prox_vecino_izq_atras() > mi_velocidad
        condicion5 = True
        condicion6 = True
        sentido_contrario = -sentido[Direccion.COLUMNA]

        if tiene_carril_izq:
            condicion5 = self.__mi_velocidad_mayor_vecino_lateral_atras(izquierda, sentido_contrario, fila_peaton, columna_peaton, velocidad, tablero)

        if tiene_carril_der:
            condicion6 = self.__mi_velocidad_mayor_vecino_lateral_atras(derecha, sentido_contrario, fila_peaton, columna_peaton, velocidad, tablero)

        if condicion1 and not tiene_vecino_der and not tiene_vecino_izq and condicion3 and condicion4 and condicion5 and condicion6:
            return Regla.AMBOS
        if condicion1 and not tiene_vecino_der and condicion4 and condicion6:
            return Regla.DER
        if condicion1 and not tiene_vecino_izq and condicion3 and condicion5:
            return Regla.IZQ
        return Regla.NO_RESUELTO

    def __mi_velocidad_mayor_vecino_lateral_atras(self, lateral, sentido_contrario, fila_peaton, columna_peaton, velocidad, tablero: Tablero):
        distancia_lateral_atras = self.distancia_al_prox_peaton(fila_peaton + lateral, columna_peaton, sentido_contrario, tablero)
        vecino_lateral_atras = None
        if distancia_lateral_atras != self.INF:
            vecino_lateral_atras = tablero.get_celda(fila_peaton + lateral, 
                                                    columna_peaton + distancia_lateral_atras * sentido_contrario[Direccion.COLUMNA] + 
                                                    sentido_contrario[Direccion.COLUMNA])
        return not vecino_lateral_atras or velocidad > vecino_lateral_atras.entidad.get_velocidad()

