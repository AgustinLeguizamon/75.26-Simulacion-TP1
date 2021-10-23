import random
from enum import Enum

class Sentido(Enum):
    NORTE = 0
    SUR = 1

class CeldaOcupadaExcepcion(Exception):
    pass


def metros_a_celdas(metros):
    celdas_por_metro = 2
    return metros * celdas_por_metro


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
    def __init__(self, id_peaton):
        self.id = id_peaton
        self.celda = None
        self.velocidad = velocidad_inicial()
        self.sentido = Sentido.NORTE

    def dar_paso(self):
        self.celda.mover_peaton(self.velocidad)

    def setear_celda(self, celda):
        self.celda = celda


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
            return 'P'
        return ' '

    def mover_peaton(self, velocidad):
        self.paso_peatonal.mover_peaton(self.x, self.y, velocidad)

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

    def agregar_peaton(self, inicial_x, inicial_y):
        # TODO: deshardcodear velocidad 1
        peaton = Peaton(self.sig_id)
        self.sig_id = self.sig_id + 1
        self.peatones.append(peaton)
        self.poner_peaton(peaton, inicial_x, inicial_y)

    def poner_peaton(self, peaton, x, y):
        # si se fue del tablero, no la coloco
        if y < 0:
            self.peatones.remove(peaton)
            return
        self.paso_peatonal[y][x].poner_peaton(peaton)

    def quitar_peaton(self, x, y):
        peaton = self.paso_peatonal[y][x].quitar_peaton()
        return peaton

    def mover_peaton(self, x, y, velocidad):
        peaton = self.quitar_peaton(x, y)
        self.poner_peaton(peaton, x, y-velocidad)

    def pasar_un_segundo(self):
        for peaton in self.peatones:
            peaton.dar_paso()


def dibujar_paso_peatonal(pasoPeatonal):
    print("-------------Norte----------------")
    for i in range(pasoPeatonal.largo):
        print('|', end='')
        for j in range(pasoPeatonal.ancho):
            print(str(pasoPeatonal.paso_peatonal[i][j].dibujar()) + str('|'), end='')
        print('')
    print("--------------Sur-----------------")


def ejercicio5():
    pasoPeatonal = PasoPeatonal(4)
    dibujar_paso_peatonal(pasoPeatonal)

    # Creo un peaton
    area_espera = 0
    area_espera += 1

    # lo pongo en el paso peatonal
    pasoPeatonal.agregar_peaton(0, pasoPeatonal.largo - 1)
    pasoPeatonal.agregar_peaton(1, pasoPeatonal.largo - 1)

    # actualizo
    dibujar_paso_peatonal(pasoPeatonal)

    x = input("cualquier tecla para dar un paso, q para salir")
    while x != 'q':
        pasoPeatonal.pasar_un_segundo()
        dibujar_paso_peatonal(pasoPeatonal)
        x = input("cualquier tecla para dar un paso, q para salir")
