class Semaforo():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.estado = "verde"

    def get_dibujo(self):
        if (self.estado == "rojo"):
            return "🔴"

        if (self.estado == "verde"):
            return "🟢"


