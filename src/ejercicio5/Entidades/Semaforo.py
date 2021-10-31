class Semaforo():
    TIEMPO_MAXIMO = 90

    def __init__(self, fila, columna, tiempo_paso_peaton = 25):
        self.fila = fila
        self.columna = columna
        self.estado = "verde"
        self.tiempo_paso_peaton = tiempo_paso_peaton

    def get_dibujo(self):
        if (self.estado == "rojo"):
            return "🔴"

        if (self.estado == "verde"):
            return "🟢"

    def permitir_paso(self):
        return self.estado == "verde"

    def cambiar_estado(self, tiempo):
        tiempo_final = tiempo % self.TIEMPO_MAXIMO
        
        if (tiempo_final <= self.tiempo_paso_peaton):
            self.estado = "verde"
        else:
            self.estado = "rojo"

