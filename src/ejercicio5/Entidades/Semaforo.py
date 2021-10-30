class Semaforo():
    _TIEMPO_MAXIMO = 90
    def __init__(self, fila, columna, tiempo_paso_peaton = 25):
        self.fila = fila
        self.columna = columna
        self.estado = "verde"

    def get_dibujo(self):
        if (self.estado == "rojo"):
            return "🔴"

        if (self.estado == "verde"):
            return "🟢"

    def permitir_paso(self):
        return self.estado == "verde"
