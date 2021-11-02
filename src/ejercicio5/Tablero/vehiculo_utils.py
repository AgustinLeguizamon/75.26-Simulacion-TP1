from typing import Dict
from enums import Direccion

# Averiguamos el estado del vehiculo de acuerdo a sus partes
# Retorna: si puede moverse y/o si debe borrarse
def detectar_estado_vehiculo(vehiculo_partes, tablero):
    puede_moverse = True
    debe_borrarse = False

    for parte in vehiculo_partes:
        celda_inicial, celda_final = get_celda_inicial_y_final(parte, tablero)
        
        # si la celda final de alguna de las partes del vehiculo no existe, 
        # debe borrarse el vehiculo
        if celda_final == None:
            debe_borrarse = True
            break
        
        # Si la celda final está ocupada, el vehiculo no debe moverse
        if celda_final.esta_ocupada():
            puede_moverse = False
            break

    return puede_moverse, debe_borrarse
    

# Movemos todas las partes de un vehiculo
def mover_vehiculo(vehiculo_partes, tablero):

    for parte in vehiculo_partes:
        celda_inicial, celda_final = get_celda_inicial_y_final(parte, tablero)
        
        # Muevo a la parte
        celda_inicial.remover_entidad() 
        celda_final.agregar_entidad(parte)

def borrar_vehiculos(vehiculos_id_a_borrar, tablero):
    for vehiculo_id in vehiculos_id_a_borrar:
        vehiculo_partes = tablero.vehiculos[vehiculo_id]

        for vehiculo_parte in vehiculo_partes:
            celda_inicial, celda_final = get_celda_inicial_y_final(vehiculo_parte, tablero)
            celda_inicial.remover_entidad() 

        tablero.vehiculos.pop(vehiculo_id)

def get_celda_inicial_y_final(parte, tablero):
    fila_inicial = parte.get_fila()
    columna_inicial = parte.get_columna()
    direccion = parte.get_direccion()
    velocidad = parte.get_velocidad()

    # Calculamos posiciones finales
    fila_final = fila_inicial + velocidad * direccion[Direccion.FILA]
    columna_final = columna_inicial + velocidad * direccion[Direccion.COLUMNA]
    celda_inicial = tablero.get_celda(fila_inicial, columna_inicial)
    celda_final = tablero.get_celda(fila_final, columna_final)

    return celda_inicial, celda_final
