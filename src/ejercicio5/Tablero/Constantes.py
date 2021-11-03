class Constantes:
    SEGUNDOS_POR_PASO = 0.5
    
    MAX_CANTIDAD_PEATONES = 100

    VEHICULO_LARGO_CELDAS = 6
    VEHICULO_ANCHO_CELDAS = 5

    ARRIBOS_POR_SEGUNDO_AUTO = 1 / 6
    ARRIBO_POR_SEGUNDO_PEATON = 5

    ANCHO_VEREDA_METROS = 10
    ANCHO_PARTE_SUPERIOR_METROS = 8
    ANCHO_PARTE_INFERIOR_METROS = 8

    CALLE_LARGO_METROS = 21
    PASO_PEATONAL_ANCHO_METROS = 3
    CANTIDAD_DE_CARRILES = 6
    ANCHO_CARRIL_METROS = 3.5
    ANCHO_CELDA_METROS = 0.5

    TIEMPO_MAXIMO_SEMAFORO = 90
    TIEMPO_DE_LUZ_VERDE = 10
    TIEMPO_DE_LUZ_AMARILLO = 30
    PERMITIR_AMARILLO = False

    HABILITAR_AREA_IZQUIERDA_PEATONES = True
    HABILITAR_AREA_DERECHA_PEATONES = True

# Simulaciones
# --------------
# 1. Valores iniciales (todo asi como está)
# 2. Cambiamos el arribo de peatones y el arribo de autos
#   ARRIBOS_POR_SEGUNDO_AUTO = 2 / 6
#   ARRIBO_POR_SEGUNDO_PEATON = 1

# Modificaciones
# --------------
# 1. Cambiar autos por motos
#   VEHICULO_LARGO_CELDAS = 1
#   VEHICULO_ANCHO_CELDAS = 5

# 2. Los peatones viajan por una sola dirección
#   HABILITAR_AREA_IZQUIERDA_PEATONES = False
#   HABILITAR_AREA_DERECHA_PEATONES = True

# 3. Habilitamos luces amarillas
#   Constantes.PERMITIR_AMARILLO = True
