from Tablero.Constantes import Constantes
from .Entidad import Entidad
import random as rn

# The phase of
# pedestrian signal is designed as six classes, which are 25 s, 30 s, 35 s, 40s, 45 s, and 50 s green
# time length, corresponding to 65 s, 60 s, 55 s, 50 s, 45 s, and 40 s red time length, respectively.
class Semaforo(Entidad):
    VERDE = 0
    ROJO = 1
    AMARILLO = 2

    def __init__(self):
        super().__init__()
        self.estado = "verde"

    def get_dibujo(self):
        return "⬤"

    def get_dibujo_color(self):
        if (self.estado == "rojo"):
            return "red"

        if (self.estado == "verde"):
            return "green"

        return "yellow"

    def permitir_paso(self):
        if (self.estado == "amarillo"):
            valor_random = rn.random()
            return valor_random < 0.5

        return self.estado == "verde"

    def cambiar_estado(self, tiempo_transcurrido, tablero):
        tiempo_final = tiempo_transcurrido % Constantes.TIEMPO_MAXIMO_SEMAFORO

        if (tiempo_final <= Constantes.TIEMPO_DE_LUZ_VERDE):
            self.estado = "verde"
            tablero.estado_peatones(self.VERDE)
            return

        if Constantes.PERMITIR_AMARILLO and tiempo_final <= Constantes.TIEMPO_DE_LUZ_AMARILLO:
            self.estado = "amarillo"
            tablero.estado_peatones(self.AMARILLO)
            return
            
        self.estado = "rojo"
        tablero.estado_peatones(self.ROJO)

