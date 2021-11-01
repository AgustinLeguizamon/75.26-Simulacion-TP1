import random as rn

ANCHO_CELDA_EN_METROS: float = 0.5

# Velocidad en cantidad de celdas del peaton
# Retorna: la velocidad inicial del peaton (valor aleatorio)
def velocidad_inicial_peaton(segundos_por_paso: float) -> int:
    p = rn.random()
    velocidad_metros_sobre_segundo: float = 0

    if 0 < p < 0.273:
        velocidad_metros_sobre_segundo = 1

    if 0.273 < p < 0.793:
        velocidad_metros_sobre_segundo = 2

    if 0.793 < p < 0.93:
        velocidad_metros_sobre_segundo = 3

    if 0.93 < p < 0.978:
        velocidad_metros_sobre_segundo = 4
    
    return int(velocidad_metros_sobre_segundo * segundos_por_paso * ANCHO_CELDA_EN_METROS)

# Retorna la velocidad inicial del vehiculo
# en cantidad de celdas por segundo
def velocidad_inicial_vehiculo(segundos_por_paso: float) -> int:
    velocidad_metros_sobre_segundo = 5
    return int(velocidad_metros_sobre_segundo * segundos_por_paso * ANCHO_CELDA_EN_METROS)

def generar_color_random():
    colores = ["white", "red", "green", "yellow", "blue", "magenta", "cyan"]
    color_elegido = rn.randint(0, len(colores) - 1)
    return colores[color_elegido]
