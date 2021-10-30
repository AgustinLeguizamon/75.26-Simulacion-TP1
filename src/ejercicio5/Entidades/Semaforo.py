class Semaforo():
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.estado = "verde"

    def get_dibujo(self):
        if (self.estado == "rojo"):
            return "🔴"

        if (self.estado == "verde"):
            return "🟢"


