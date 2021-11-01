from .Entidad import Entidad

class Semaforo(Entidad):
    TIEMPO_MAXIMO = 90

    def __init__(self, tiempo_paso_peaton = 25):
        super().__init__()
        self.estado = "verde"
        self.tiempo_paso_peaton = tiempo_paso_peaton

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

    def cambiar_estado(self, tiempo_transcurrido):
        tiempo_final = tiempo_transcurrido % self.TIEMPO_MAXIMO
        
        if (tiempo_final <= self.tiempo_paso_peaton):
            self.estado = "verde"
        else:
            self.estado = "rojo"

