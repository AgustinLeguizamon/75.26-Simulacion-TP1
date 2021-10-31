from .Movible import Movible
from enums import Sentido

class VehiculoParte(Movible):
    
    def __init__(self, sentido: Sentido, velocidad: float, fila_relativa, columna_relativa, color):
        super().__init__(sentido, velocidad, color)
        self.fila_relativa = fila_relativa
        self.columna_relativa = columna_relativa

    def get_dibujo(self):
        # ◢☗☗☗☗◣
        # ██████
        # ██████
        # ██████
        # ◥▆▆▆▆◤

        if (self.fila_relativa == 0 and self.columna_relativa == 0):
            return '◢' if self.sentido == Sentido.NORTE else '◥'

        if (self.fila_relativa == 0 and 0 < self.columna_relativa < 5):
            return '☗' if self.sentido == Sentido.NORTE else '▆'

        if (self.fila_relativa == 0 and self.columna_relativa):
            return '◣' if self.sentido == Sentido.NORTE else '◤'

        if (0 < self.fila_relativa < 5):
            return '█'

        if (self.fila_relativa == 5 and self.columna_relativa == 0):
            return '◥' if self.sentido == Sentido.NORTE else '◢'

        if (self.fila_relativa == 5 and 0 < self.columna_relativa < 5):
            return '▆' if self.sentido == Sentido.NORTE else '☗'

        if (self.fila_relativa == 5 and self.columna_relativa):
            return '◤' if self.sentido == Sentido.NORTE else '◣'

        return "?"

