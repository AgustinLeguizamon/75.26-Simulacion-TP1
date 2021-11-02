import os
import random
import time

from Tablero.Tablero import Tablero
from enums import Direccion
from Estadisticas import Estadisticas

def debug_agregar_peatones(tablero):
   fin_paso_peatonal = 40
   tablero._debug_colocar_peaton(0,0, Direccion.ESTE, 1)
   tablero._debug_colocar_peaton(1,0, Direccion.ESTE, 2)
   tablero._debug_colocar_peaton(2,0, Direccion.ESTE, 3)
   tablero._debug_colocar_peaton(3,0, Direccion.ESTE, 4)
   tablero._debug_colocar_peaton(4,0, Direccion.ESTE, 5)

   tablero._debug_colocar_peaton(0,2, Direccion.ESTE, 1)
   tablero._debug_colocar_peaton(1,3, Direccion.ESTE, 2)
   tablero._debug_colocar_peaton(2,4, Direccion.ESTE, 3)
   tablero._debug_colocar_peaton(3,5, Direccion.ESTE, 2)
   tablero._debug_colocar_peaton(4,6, Direccion.ESTE, 2)

   tablero._debug_colocar_peaton(1,fin_paso_peatonal, Direccion.OESTE, 5)
   tablero._debug_colocar_peaton(2,fin_paso_peatonal, Direccion.OESTE, 4)
   tablero._debug_colocar_peaton(3,fin_paso_peatonal, Direccion.OESTE, 3)
   tablero._debug_colocar_peaton(4,fin_paso_peatonal, Direccion.OESTE, 2)
   tablero._debug_colocar_peaton(5,fin_paso_peatonal, Direccion.OESTE, 1)

   tablero._debug_colocar_peaton(1,fin_paso_peatonal-2, Direccion.OESTE, 2)
   tablero._debug_colocar_peaton(2,fin_paso_peatonal-2, Direccion.OESTE, 4)
   tablero._debug_colocar_peaton(3,fin_paso_peatonal-2, Direccion.OESTE, 1)
   tablero._debug_colocar_peaton(4,fin_paso_peatonal-2, Direccion.OESTE, 2)
   tablero._debug_colocar_peaton(5,fin_paso_peatonal-2, Direccion.OESTE, 1)
   #

def limpiar_pantalla():
   # Para Mac y Linux
   if os.name == 'posix':
      os.system('clear')
   else:
      # Para Windows
      os.system('cls')

def main():
   # Init game variables
   esta_corriendo = True
   segundos_por_paso: int = 0.5
   tiempo_transcurrido = 0
   ##Estadisticas()
   tablero = Tablero(segundos_por_paso=segundos_por_paso, area_izq=True, area_der=True)

   # TODO: para debug colisiones peatones, acordarse de comentar areas de espera de autos
   debug_agregar_peatones(tablero)

   while esta_corriendo:
      limpiar_pantalla()
      tablero.ejecutar_paso(tiempo_transcurrido, segundos_por_paso)
      tiempo_transcurrido += segundos_por_paso
      time.sleep(segundos_por_paso)

if __name__ == "__main__":
    main()

