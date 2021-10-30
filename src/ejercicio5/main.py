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

    while isRunning:
        limpiarPantalla()

        # Dibujar
        tablero.accionar()

        # Dormir por X segundos
        segs = 1
        time.sleep(segs)

if __name__ == "__main__":
    main()

