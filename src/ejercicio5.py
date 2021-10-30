import random
from enum import Enum

INF = 99


class Movimiento:
    # en x y en y
    NORTE = [0, -1]
    ESTE = [1, 0]
    SUR = [0, 1]
    OESTE = [-1, 0]
    
    
class Sentido(Enum):
    NORTE = -1
    SUR = 1
    ESTE = 2
    OESTE = 3


class Regla(Enum):
    NINGUNA = 0
    AMBOS = 1
    DER = 2
    IZQ = 3
    NO_RESUELTO = 4


class CeldaOcupadaExcepcion(Exception):
    pass


class MovimientoNoLateralExcepcion(Exception):
    pass


class PeatonNoPuedeSalirPorLosLateralesExcepcion(Exception):
    pass


class QuitandoMovibleDeCeldaVaciaExcepcion(Exception):
    pass


def dibujar_paso_peatonal(pasoPeatonal):
    print("-------------Norte----------------")
    print('\t ', end='')
    for i in range(pasoPeatonal.ancho):
        print('' + str(i) + ' ', end='')
    print('')
    for i in range(pasoPeatonal.largo):
        print(str(i) + '\t|', end='')
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


class Paso:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Movible:
    def __init__(self, sentido, velocidad):
        self.celda = None
        self.sentido = sentido
        self.velocidad = velocidad

    def setear_celda(self, celda):
        self.celda = celda

    def dar_paso(self):
        self.celda.mover_movible(self.velocidad, self.sentido)

    def salir_de_celda(self):
        if self.celda is not None:
            self.celda.quitar_movible()
            self.celda = None

    def dibujar(self):
        if self.velocidad == 0:
            return 'x'
        if self.sentido == Movimiento.NORTE:
            return '^'
        if self.sentido == Movimiento.SUR:
            return 'v'
        if self.sentido == Movimiento.ESTE:
            return '>'
        if self.sentido == Movimiento.OESTE:
            return '<'


class Peaton(Movible):
    def __init__(self, id_peaton, sentido, velocidad):
        super().__init__(sentido, velocidad)
        self.id = id_peaton

    def dar_paso(self):
        self.celda.mover_peaton(self.velocidad, self.sentido)

    def actualizar_velocidad(self, d):
        self.velocidad = min(d, self.velocidad)
        return self.velocidad


class Vehiculo:
    LARGO = 6
    ANCHO = 5

    def __init__(self, sentido):
        self.sentido = sentido
        self.velocidad = 1
        self.movibles = [Movible(sentido, 1) for i in range(self.LARGO * self.ANCHO)]
        self.x = -1
        self.y = -1
        self.paso = Paso(1 if Movimiento.ESTE == sentido else -1, 0)
        self.esta_afuera = False

    def set_posicion(self, x, y):
        self.x = x
        self.y = y

    def asignar_celda(self, fila, columna, celda):
        pos = fila * self.ANCHO + columna
        celda.poner_movible(self.movibles[pos])

    def dar_paso(self, paso_peatonal):
        self.__salir_de_celdas()
        if paso_peatonal.puede_moverse(self.x + self.velocidad * self.paso.x, self.y):
            paso_peatonal.mover_vehiculo(self, self.paso.x, self.paso.y)
        else:
            # lo vuelvo a colocar en sus celdas
            paso_peatonal.mover_vehiculo(self, 0, 0)

    def estas_afuera(self):
        self.esta_afuera = True

    def __salir_de_celdas(self):
        # Primero levanta todos los elementos
        for movible in self.movibles:
            movible.salir_de_celda()


class Celda:
    def __init__(self, x, y, paso_peatonal):
        self.x = x
        self.y = y
        self.ocupada = False
        self.movible = None
        self.paso_peatonal = paso_peatonal

    def poner_movible(self, movible):
        if self.ocupada:
            raise CeldaOcupadaExcepcion
        self.ocupada = True
        self.movible = movible
        movible.setear_celda(self)

    def dibujar(self):
        if self.ocupada:
            return self.movible.dibujar()
        return ' '

    def mover_peaton(self, velocidad, sentido):
        self.paso_peatonal.mover_peaton(self.x, self.y, velocidad, sentido)

    def mover_movible(self, velocidad, sentido):
        self.paso_peatonal.mover_movible(self.x, self.y, velocidad, sentido)

    def quitar_movible(self):
        if self.movible is None:
            raise QuitandoMovibleDeCeldaVaciaExcepcion
        self.ocupada = False
        movible = self.movible
        self.movible = None
        return movible

    def dar_paso(self):
        if self.movible is not None:
            self.movible.dar_paso()


class AreaEspera:
    # Cuenta cuantos peatones tiene
    # Cuenta cuantos peatones cruzaron
    MAX_CANTIDAD_PEATONES = 100

    def __init__(self, posicion):
        self.peatones_esperando = 0
        self.peatones_cruzaron = 0
        self.posicion = posicion

    def peaton_arriba(self, sentido):
        if (sentido != self.posicion) and (self.peatones_esperando < self.MAX_CANTIDAD_PEATONES):
            self.peatones_esperando += 1

    def peaton_entra_paso_peatonal(self):
        self.peatones_esperando -= 1

    def peaton_cruza_paso_peatonal(self):
        self.peatones_cruzaron += 1


class PasoPeatonal:
    def __init__(self, ancho):
        self.largo = metros_a_celdas(21)
        self.ancho = metros_a_celdas(ancho)
        self.paso_peatonal = [[Celda(x, y, self) for x in range(self.ancho)] for y in range(self.largo)]
        self.peatones = []
        self.sig_id = 0
        self.calle_norte = AreaEspera(Movimiento.NORTE)
        self.calle_sur = AreaEspera(Movimiento.SUR)
        self.vehiculos = []

    def peaton_arriba(self, sentido):
        # TODO: evento de poisson
        self.calle_sur.peaton_arriba(sentido)
        self.calle_norte.peaton_arriba(sentido)

    # TODO: una vez que termino de testear, los peatones van a empezar siempre en el extremo de cada paso peatonal
    def agregar_peaton(self, inicial_x, inicial_y, sentido, velocidad=-1):
        _velocidad = velocidad
        if velocidad == -1:
            _velocidad = velocidad_inicial()
        peaton = Peaton(self.sig_id, sentido, _velocidad)
        self.sig_id = self.sig_id + 1
        self.peatones.append(peaton)
        self.poner_peaton(peaton, inicial_x, inicial_y)

    def poner_vehiculo(self, inicial_x, inicial_y, vehiculo):
        vehiculo.set_posicion(inicial_x, inicial_y)
        # veo si la posicion del auto termina fuera del paso peatonal y lo elimino
        if inicial_x + vehiculo.LARGO < 0 or inicial_x > self.ancho:
            vehiculo.estas_afuera()
        else:
            for x in range(Vehiculo.LARGO):
                for y in range(Vehiculo.ANCHO):
                    # Si se va del paso peatonal simplemente no le asigna una celda
                    # es decir queda un cacho del vehiculo
                    if 0 <= inicial_y + y < self.largo and 0 <= inicial_x + x < self.ancho:
                        vehiculo.asignar_celda(x, y, self.paso_peatonal[inicial_y + y][inicial_x + x])

    def agregar_vehiculo(self, inicial_x, inicial_y, sentido):
        vehiculo = Vehiculo(sentido)
        self.vehiculos.append(vehiculo)
        self.poner_vehiculo(inicial_x, inicial_y, vehiculo)

    def poner_peaton(self, peaton, x, y):
        if x < 0 or x >= self.ancho:
            raise PeatonNoPuedeSalirPorLosLateralesExcepcion
        # si se fue del tablero no lo coloco
        if y < 0 or y > self.largo - 1:
            peaton.setear_celda(None)
            return
        self.paso_peatonal[y][x].poner_movible(peaton)

    def quitar_movible(self, x, y):
        peaton = self.paso_peatonal[y][x].quitar_movible()
        return peaton

    def mover_peaton(self, x, y, velocidad, sentido):
        d = self.distancia_al_prox_peaton(x, y, sentido)
        # print("sentido: " + str(sentido) + " - distancia:" + str(d))
        peaton = self.quitar_movible(x, y)
        regla = self.cambio_de_linea(x, y, velocidad, sentido)
        if regla == Regla.AMBOS:
            # muevo movible
            x += 1 if probabilidad(0.5) else -1
        elif regla == Regla.DER:
            x += 1 if peaton.sentido == Movimiento.NORTE else -1
        elif regla == Regla.IZQ:
            x += -1 if peaton.sentido == Movimiento.NORTE else 1
        if regla != Regla.NINGUNA:
            # Recalculo distancia despues de resolver conflicto
            d = self.distancia_al_prox_peaton(x, y, sentido)
        # el peaton en este turno no se mueve si no puedo resolver el conflicto, pero mantiene la velocidad
        velocidad = 0
        if regla != Regla.NO_RESUELTO:
            # si resulta que no hubo conflicto actualizo la velocidad
            velocidad = peaton.actualizar_velocidad(d)
        self.poner_peaton(peaton, x, y + velocidad * sentido[1])

    def puede_moverse(self, inicial_x, inicial_y):
        for offset_x in range(Vehiculo.LARGO):
            for offset_y in range(Vehiculo.ANCHO):
                x = inicial_x + offset_x
                y = inicial_y + offset_y
                # si esta dentro del paso_peatonal y esta ocupada entonces no se puede mover
                if 0 <= x < self.ancho and 0 <= y < self.largo and self.paso_peatonal[y][x].ocupada:
                    return False
        return True

    def mover_vehiculo(self, vehiculo, paso_x, paso_y):
        self.poner_vehiculo(vehiculo.x + vehiculo.velocidad * paso_x, vehiculo.y + paso_y, vehiculo)

    def pasar_un_segundo(self):
        # TODO: peaton_arriba()
        # TODO: peaton_entra_paso_peatonal()
        for peaton in self.peatones:
            peaton.dar_paso()
        for vehiculo in self.vehiculos:
            vehiculo.dar_paso(self)
        # Todos aquellos peatones que esten fuera del tablero son eliminados
        self.peatones = [peaton for peaton in self.peatones if peaton.celda is not None]
        self.vehiculos = [vehiculo for vehiculo in self.vehiculos if not vehiculo.esta_afuera]

    def distancia_al_prox_peaton(self, x, y, sentido):
        d = 0
        limite = self.largo
        hay_peaton_adelante = False
        if sentido == Movimiento.NORTE:
            limite = -1
        for j in range(y + sentido[1], limite, sentido[1]):
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
        # TODO: para optimizar, si no se meuve no tiene sentido cambiar de linea
        if velocidad == 0:
            return Regla.NINGUNA
        # si tiene uno adelante:
        # condicion1 = Celda(x,y-1).ocupada
        condicion1 = self.distancia_al_prox_peaton(x, y, sentido) == 0

        # si no se cumple la condicion de conflicto, break
        if not condicion1:
            return Regla.NINGUNA

        # defino que es derecha e izquierda segun el sentido
        derecha = 1
        if sentido == Movimiento.SUR:
            derecha = -1
        izquierda = -derecha
        # a la derecha y a la izquierda esta vacio:
        # condicion2 = not Celda(x-1,y).ocupada and not Celda(x+1,y).ocupada
        tiene_carril_der = 0 <= (x + derecha) < self.ancho
        tiene_carril_izq = 0 <= (x + izquierda) < self.ancho
        tiene_vecino_der = tiene_carril_der and self.paso_peatonal[y][x + derecha].ocupada
        tiene_vecino_izq = tiene_carril_izq and self.paso_peatonal[y][x + izquierda].ocupada

        if tiene_vecino_izq and tiene_vecino_der:
            return Regla.NO_RESUELTO
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
        sentido_contrario = Movimiento.NORTE
        if sentido == Movimiento.NORTE:
            sentido_contrario = Movimiento.SUR

        if tiene_carril_izq:
            condicion5 = self.mi_velocidad_mayor_vecino_lateral_atras(izquierda, sentido_contrario, x, y, velocidad)

        if tiene_carril_der:
            condicion6 = self.mi_velocidad_mayor_vecino_lateral_atras(derecha, sentido_contrario, x, y, velocidad)

        if condicion1 and not tiene_vecino_der and not tiene_vecino_izq and condicion3 and condicion4 and condicion5 and condicion6:
            return Regla.AMBOS
        if condicion1 and not tiene_vecino_der and condicion4 and condicion6:
            return Regla.DER
        if condicion1 and not tiene_vecino_izq and condicion3 and condicion5:
            return Regla.IZQ
        return Regla.NO_RESUELTO

    def mi_velocidad_mayor_vecino_lateral_atras(self, lateral, sentido_contrario, x, y, velocidad):
        distancia_lateral_atras = self.distancia_al_prox_peaton(x + lateral, y, sentido_contrario)
        vecino_lateral_atras = None
        if distancia_lateral_atras != INF:
            vecino_lateral_atras = self.paso_peatonal[y + distancia_lateral_atras * sentido_contrario[1] +
                                                      sentido_contrario[1]][x + lateral]
        return not vecino_lateral_atras or velocidad > vecino_lateral_atras.movible.velocidad


def ejercicio5():
    pasoPeatonal = PasoPeatonal(4)
    dibujar_paso_peatonal(pasoPeatonal)
    inicior_sur = pasoPeatonal.largo - 1
    inicio_este = pasoPeatonal.ancho - 1

    # lo pongo en el paso peatonal
    pasoPeatonal.agregar_peaton(0, 0, Movimiento.SUR)
    pasoPeatonal.agregar_peaton(1, 0, Movimiento.SUR)
    pasoPeatonal.agregar_peaton(2, 0, Movimiento.SUR)
    pasoPeatonal.agregar_peaton(3, 0, Movimiento.SUR)
    pasoPeatonal.agregar_peaton(4, 0, Movimiento.SUR)
    pasoPeatonal.agregar_peaton(5, 0, Movimiento.SUR)
    pasoPeatonal.agregar_peaton(6, 0, Movimiento.SUR)
    pasoPeatonal.agregar_peaton(7, 0, Movimiento.SUR)

    '''
    pasoPeatonal.agregar_peaton(3, 1, Movimiento.SUR)
    pasoPeatonal.agregar_peaton(4, 1, Movimiento.SUR)
    pasoPeatonal.agregar_peaton(5, 1, Movimiento.SUR)
    pasoPeatonal.agregar_peaton(6, 1, Movimiento.SUR)
    pasoPeatonal.agregar_peaton(7, 1, Movimiento.SUR)

    pasoPeatonal.agregar_peaton(2, inicior_sur, Movimiento.NORTE)
    pasoPeatonal.agregar_peaton(3, inicior_sur, Movimiento.NORTE)
    pasoPeatonal.agregar_peaton(4, inicior_sur, Movimiento.NORTE)
    pasoPeatonal.agregar_peaton(5, inicior_sur, Movimiento.NORTE)
    pasoPeatonal.agregar_peaton(6, inicior_sur, Movimiento.NORTE)
    '''
    pasoPeatonal.agregar_peaton(0, inicior_sur, Movimiento.NORTE)
    pasoPeatonal.agregar_peaton(1, inicior_sur, Movimiento.NORTE)
    pasoPeatonal.agregar_peaton(2, inicior_sur, Movimiento.NORTE)
    pasoPeatonal.agregar_peaton(3, inicior_sur, Movimiento.NORTE)
    pasoPeatonal.agregar_peaton(4, inicior_sur, Movimiento.NORTE)
    pasoPeatonal.agregar_peaton(5, inicior_sur, Movimiento.NORTE)
    pasoPeatonal.agregar_peaton(6, inicior_sur, Movimiento.NORTE)
    pasoPeatonal.agregar_peaton(7, inicior_sur, Movimiento.NORTE)

    # 6 lineas de 7 cuadrados cada una
    # los autos miden 5 por lo tanto queda 1 cuadrado entre cada linea

    # 3 lineas de autos sentido OESTE

    # for i in range(3):
        # pasoPeatonal.agregar_vehiculo(inicio_este, 1 + 2*i + Vehiculo.ANCHO * i, Movimiento.OESTE)
    # pongo autos sentido ESTE
    # for i in range(3):
        # pasoPeatonal.agregar_vehiculo(1 - Vehiculo.LARGO, 1 + 2*i + Vehiculo.ANCHO * i + 21, Movimiento.ESTE)

    # actualizo
    dibujar_paso_peatonal(pasoPeatonal)

    x = input("cualquier tecla para dar un paso, q para salir")
    while x != 'q':
        pasoPeatonal.pasar_un_segundo()
        dibujar_paso_peatonal(pasoPeatonal)
        x = input("cualquier tecla para dar un paso, q para salir")
