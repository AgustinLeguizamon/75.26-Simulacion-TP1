import random as rn

def velocidad_inicial_peaton():
    p = rn.random()
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

def velocidad_inicial_vehiculo():
    return 1

def generar_color_random():
    colores = ["white", "red", "green", "yellow", "blue", "magenta", "cyan"]
    color_elegido = rn.randint(0, len(colores) - 1)
    return colores[color_elegido]
