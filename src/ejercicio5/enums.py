from enum import Enum

class Sentido(Enum):
    NORTE = -1
    SUR = 1
    ESTE = 2
    OESTE = 3

class Direccion:
    FILA = 0
    COLUMNA = 1
    NORTE = [-1, 0]
    ESTE = [0, 1]
    SUR = [1, 0]
    OESTE = [0, -1]

class Regla(Enum):
    NINGUNA = 0
    AMBOS = 1
    DER = 2
    IZQ = 3
    NO_RESUELTO = 4

class TipoDeCelda(Enum):
    NORMAL = 0,
    VEREDA_CORDON = 1,
    CARRIL_SEPARADOR = 2,
    CARRIL_SEPARADOR_DEL_MEDIO = 3,
    SEPARADOR_PEATONAL = 4,
