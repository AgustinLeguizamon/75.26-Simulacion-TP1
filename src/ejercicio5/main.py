import os
import random
import time

from Tablero.Tablero import Tablero
from enums import Direccion

def limpiarPantalla():
   # Para Mac y Linux
   if os.name == 'posix':
      os.system('clear')
   else:
      # Para Windows
      os.system('cls')

def main():
   # Init game variables
   isRunning = True
   segundos_por_paso: int = 0.5
   tiempo_transcurrido = 0
   tablero = Tablero(segundos_por_paso=segundos_por_paso)

   # TODO: para debug colisiones peatones
   
   tablero._debug_colocar_peaton(4,38, Direccion.ESTE, 1)

   tablero._debug_colocar_peaton(5,5, Direccion.ESTE, 0)
   # tablero._debug_colocar_peaton(0,0, Direccion.ESTE, 1)
   
   #

   while isRunning:
      limpiarPantalla()
      tablero.ejecutar_paso(tiempo_transcurrido, segundos_por_paso)
      tiempo_transcurrido += segundos_por_paso
      time.sleep(segundos_por_paso)

if __name__ == "__main__":
    main()

