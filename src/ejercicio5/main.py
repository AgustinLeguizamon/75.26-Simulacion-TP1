import os
import random
import time

from Tablero.Tablero import Tablero

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
    tablero = Tablero()

    segundos_por_paso = 0.5
    tiempo_transcurrido = 0

    while isRunning:
        limpiarPantalla()
        tablero.ejecutar_paso(tiempo_transcurrido)
        tiempo_transcurrido += segundos_por_paso
        time.sleep(segundos_por_paso)

if __name__ == "__main__":
    main()

