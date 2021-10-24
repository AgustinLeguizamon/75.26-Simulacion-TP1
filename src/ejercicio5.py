import random
from enum import Enum

INF = 99


class Sentido(Enum):
    NORTE = -1
    SUR = 1


class Regla(Enum):
    NINGUNA = 0
    AMBOS = 1
    DER = 2
    IZQ = 3


class CeldaOcupadaExcepcion(Exception):
    pass

def dibujar_paso_peatonal(pasoPeatonal):
    print("-------------Norte----------------")
    for i in range(pasoPeatonal.largo):
        print('|', end='')
        for j in range(pasoPeatonal.ancho):
            print(str(pasoPeatonal.paso_peatonal[i][j].dibujar()) + str('|'), end='')
        print('')
    print("--------------Sur-----------------")
    print("#######################################################")


def metros_a_celdas(metros):
    celdas_por_metro = 2
    return metros * celdas_por_metro


def probabilidad(proba):
    p = random.random()
    return p < proba


def velocidad_inicial():
    p = random.random()
    velocidad = 2
    if p > 0.978:
        velocidad = 6
        return velocidad
    if p > 0.93:
        velocidad = 5
        return velocidad
    if p > 0.793:
        velocidad = 4
        return velocidad
    if p > 0.273:
        velocidad = 3
        return velocidad
    return velocidad


class Peaton:
    def __init__(self, id_peaton, sentido, se_mueve):
        self.id = id_peaton
        self.celda = None
        self.velocidad = velocidad_inicial()
        if not se_mueve:
            self.velocidad = 0
        self.sentido = sentido

    def dar_paso(self):
        self.celda.mover_peaton(self.velocidad, self.sentido)

    def setear_celda(self, celda):
        self.celda = celda

    def actualizar_velocidad(self, d):
        self.velocidad = min(d, self.velocidad)
        return self.velocidad

    def dibujar(self):
        if self.velocidad == 0:
            return 'x'
        if self.sentido == Sentido.NORTE:
            return '^'
        if self.sentido == Sentido.SUR:
            return 'v'


class Celda:
    def __init__(self, x, y, paso_peatonal):
        self.x = x
        self.y = y
        self.ocupada = False
        self.peaton = None
        self.paso_peatonal = paso_peatonal

    def poner_peaton(self, peaton):
        if self.ocupada:
            raise CeldaOcupadaExcepcion
        self.ocupada = True
        self.peaton = peaton
        peaton.setear_celda(self)

    def dibujar(self):
        if self.ocupada:
            return self.peaton.dibujar()
        return ' '

    def mover_peaton(self, velocidad, sentido):
        self.paso_peatonal.mover_peaton(self.x, self.y, velocidad, sentido)

    def quitar_peaton(self):
        self.ocupada = False
        peaton = self.peaton
        self.peaton = None
        return peaton

    def dar_paso(self):
        if self.peaton is not None:
            self.peaton.dar_paso()


class PasoPeatonal:
    def __init__(self, ancho):
        self.largo = metros_a_celdas(4)
        self.ancho = metros_a_celdas(ancho)
        self.paso_peatonal = [[Celda(x, y, self) for x in range(self.ancho)] for y in range(self.largo)]
        self.peatones = []
        self.sig_id = 0

    def agregar_peaton(self, inicial_x, inicial_y, sentido, se_mueve=True):
        peaton = Peaton(self.sig_id, sentido, se_mueve)
        self.sig_id = self.sig_id + 1
        self.peatones.append(peaton)
        self.poner_peaton(peaton, inicial_x, inicial_y)

    def poner_peaton(self, peaton, x, y):
        # si se fue del tablero, no la coloco
        if y < 0 or y > self.largo - 1:
            peaton.setear_celda(None)
            return
        self.paso_peatonal[y][x].poner_peaton(peaton)

    def quitar_peaton(self, x, y):
        peaton = self.paso_peatonal[y][x].quitar_peaton()
        return peaton

    def mover_peaton(self, x, y, velocidad, sentido):
        d = self.distancia_al_prox_peaton(x, y, sentido)
        print("sentido: " + str(sentido) + " - distancia:" + str(d))
        peaton = self.quitar_peaton(x, y)
        regla = self.cambio_de_linea(x, y, velocidad, sentido)
        if regla == Regla.AMBOS:
            # muevo peaton
            x += 1 if probabilidad(0.5) else -1
        elif regla == Regla.DER:
            x += -sentido.value
        elif regla == Regla.IZQ:
            x += sentido.value
        if regla != Regla.NINGUNA:
            # Recalculo distancia despues de resolver conflicto
            d = self.distancia_al_prox_peaton(x, y, sentido)
        velocidad = peaton.actualizar_velocidad(d)
        if velocidad == 0:
            dibujar_paso_peatonal(self)
        self.poner_peaton(peaton, x, y + velocidad * sentido.value)


    def pasar_un_segundo(self):
        for peaton in self.peatones:
            peaton.dar_paso()
        # Todos aquellos peatones que esten fuera del tablero son eliminados
        self.peatones = [peaton for peaton in self.peatones if peaton.celda is not None]

    def distancia_al_prox_peaton(self, x, y, sentido):
        d = 0
        limite = self.largo
        hay_peaton_adelante = False
        if sentido == Sentido.NORTE:
            limite = -1
        for j in range(y + sentido.value, limite, sentido.value):
            if self.paso_peatonal[j][x].ocupada:
                hay_peaton_adelante = True
                break
            d += 1
        # si resulta que no hay nadie adelante, la distancia es inf
        if not hay_peaton_adelante:
            d = INF
        return d

    def cambio_de_linea(self, x, y, velocidad, sentido):
        # si su velocidad es 0, break
        if velocidad == 0:
            return Regla.NINGUNA
        # si tiene uno adelante:
        # condicion1 = Celda(x,y-1).ocupada
        condicion1 = self.distancia_al_prox_peaton(x, y, sentido) == 0

        # si no se cumple la condicion1, break
        if not condicion1:
            return Regla.NINGUNA

        # defino que es derecha e izquierda segun el sentido
        derecha = 1
        if sentido == Sentido.SUR:
            derecha = -1
        izquierda = -derecha
        # a la derecha y a la izquierda esta vacio:
        # condicion2 = not Celda(x-1,y).ocupada and not Celda(x+1,y).ocupada
        tiene_carril_der = (x + derecha) < self.ancho
        tiene_carril_izq = (x + izquierda) >= 0
        tiene_vecino_der = tiene_carril_der and self.paso_peatonal[y][x + derecha].ocupada
        tiene_vecino_izq = tiene_carril_izq and self.paso_peatonal[y][x + izquierda].ocupada

        if tiene_vecino_izq and tiene_vecino_der:
            return Regla.NINGUNA
        # la distancia al vecino lateral mas cercano es mayor a su velocidad actual
        # condicion3 = distancia_al_prox_vecino_izq_adelante() > mi_velocidad
        # condicion4 = distancia_al_prox_vecino_der_adelante() > mi_velocidad
        condicion3 = tiene_carril_izq and self.distancia_al_prox_peaton(x + izquierda, y, sentido) > velocidad
        condicion4 = tiene_carril_der and self.distancia_al_prox_peaton(x + derecha, y, sentido) > velocidad

        # 'velocidad de los primeros vecinos laterales que estan n celdas mas atras' es
        # menor a mi velocidad actual
        # distancia_al_prox_vecino_der_atras() > mi_velocidad
        # distancia_al_prox_vecino_izq_atras() > mi_velocidad
        condicion5 = True
        condicion6 = True
        sentido_contrario = Sentido.NORTE
        if sentido == Sentido.NORTE:
            sentido_contrario = Sentido.SUR

        if tiene_carril_izq:
            condicion5 = self.mi_velocidad_mayor_vecino_lateral_atras(izquierda, sentido_contrario, x, y, velocidad)

        if tiene_carril_der:
            condicion6 = self.mi_velocidad_mayor_vecino_lateral_atras(derecha, sentido_contrario, x, y, velocidad)

        if condicion1 and not tiene_vecino_der and not tiene_vecino_izq and condicion3 and condicion4 and condicion5 and condicion6:
            return Regla.AMBOS
        if condicion1 and not tiene_vecino_der and condicion4 and condicion5 and condicion6:
            return Regla.DER
        if condicion1 and not tiene_vecino_izq and condicion3 and condicion5 and condicion6:
            return Regla.IZQ
        return Regla.NINGUNA

    def mi_velocidad_mayor_vecino_lateral_atras(self, lateral, sentido_contrario, x, y, velocidad):
        distancia_lateral_atras = self.distancia_al_prox_peaton(x + lateral, y, sentido_contrario)
        vecino_lateral_atras = None
        if distancia_lateral_atras != INF:
            vecino_lateral_atras = self.paso_peatonal[y + distancia_lateral_atras * sentido_contrario.value +
                                                      sentido_contrario.value][x + lateral]
        return not vecino_lateral_atras or velocidad > vecino_lateral_atras.peaton.velocidad



def ejercicio5():
    pasoPeatonal = PasoPeatonal(4)
    dibujar_paso_peatonal(pasoPeatonal)

    # Creo un peaton
    area_espera = 0
    area_espera += 1

    # lo pongo en el paso peatonal
    pasoPeatonal.agregar_peaton(4, pasoPeatonal.largo-1, Sentido.NORTE)

    pasoPeatonal.agregar_peaton(4, 3, Sentido.SUR, False)
    pasoPeatonal.agregar_peaton(3, 3, Sentido.SUR, False)
    # pasoPeatonal.agregar_peaton(6, 0, Sentido.SUR)
    #

    # peaton que no se mueve
    # pasoPeatonal.agregar_peaton(1, 4, Sentido.NORTE, False)
    # pasoPeatonal.agregar_peaton(3, 4, Sentido.NORTE, False)
    # actualizo
    dibujar_paso_peatonal(pasoPeatonal)

    x = input("cualquier tecla para dar un paso, q para salir")
    while x != 'q':
        pasoPeatonal.pasar_un_segundo()
        dibujar_paso_peatonal(pasoPeatonal)
        x = input("cualquier tecla para dar un paso, q para salir")
