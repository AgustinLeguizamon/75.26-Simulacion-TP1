import numpy as np

def metros_a_celdas(metros):
    celdas_por_metro = 2
    return metros * celdas_por_metro


class Peaton:

    def __init__(self, velocidad_inicial):
        self.celda = None
        self.velocidad = velocidad_inicial

    def dar_paso(self):
        self.celda.moveme_hacia_adelante(self.velocidad)

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
        self.ocupada = True
        self.peaton = peaton
        peaton.setear_celda(self)

    def dibujar(self):
        if self.ocupada:
            return 'x'
        return ' '

    def moveme_hacia_adelante(self, velocidad):
        self.paso_peatonal.mover_peaton(self.x, self.y, velocidad)

    def quitar_peaton(self):
        self.ocupada = False
        peaton = self.peaton
        self.peaton = None
        return peaton


class PasoPeatonal:
    def __init__(self, ancho):
        self.largo = metros_a_celdas(4)
        self.ancho = metros_a_celdas(ancho)
        self.paso_peatonal = [[Celda(x, y, self) for x in range(self.ancho)] for y in range(self.largo)]

    def poner_peaton(self, peaton, x, y):
        self.paso_peatonal[y][x].poner_peaton(peaton)

    def quitar_peaton(self, x,y):
        peaton = self.paso_peatonal[y][x].quitar_peaton()
        return peaton

    def mover_peaton(self,x,y, velocidad):
        peaton = self.quitar_peaton(x,y)
        self.poner_peaton(peaton, x,y-velocidad)


def dibujar_paso_peatonal(pasoPeatonal):
    print("--------------Norte-----------------")
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
    peaton = Peaton(1)
    peaton_2 = Peaton(1)
    area_espera += 1

    # lo pongo en el paso peatonal
    pasoPeatonal.poner_peaton(peaton, 0, pasoPeatonal.largo-1)

    # actualizo
    dibujar_paso_peatonal(pasoPeatonal)

    x = input("cualquier tecla para dar un paso, q para salir")
    while x != 'q':
        # pasoPeatonal.pasa_un_segundo()
        peaton.dar_paso()
        dibujar_paso_peatonal(pasoPeatonal)
        x = input("cualquier tecla para dar un paso, q para salir")
