from Tablero.Constantes import Constantes
from .Entidad import Entidad

# The phase of
# pedestrian signal is designed as six classes, which are 25 s, 30 s, 35 s, 40s, 45 s, and 50 s green
# time length, corresponding to 65 s, 60 s, 55 s, 50 s, 45 s, and 40 s red time length, respectively.
class Semaforo(Entidad):
    VERDE = 0
    ROJO = 1

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

        return "purple"

    def permitir_paso(self):
        return self.estado == "verde"

    def cambiar_estado(self, tiempo_transcurrido, tablero):
        tiempo_final = tiempo_transcurrido % Constantes.TIEMPO_MAXIMO_SEMAFORO
        
        if (tiempo_final <= Constantes.TIEMPO_DE_LUZ_VERDE):
            self.estado = "verde"
            tablero.estado_peatones(self.VERDE)
        else:
            self.estado = "rojo"
            tablero.estado_peatones(self.ROJO)

