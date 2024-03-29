from .Movible import Movible
from enums import Direccion

class VehiculoParte(Movible):
    
    def __init__(self, id: int, direccion: Direccion, velocidad: float, fila_relativa, columna_relativa, color):
        super().__init__(direccion, velocidad, color)
        self.id = id
        self.fila_relativa = fila_relativa
        self.columna_relativa = columna_relativa

    def __str__(self):
        return "VehiculoParte"

    def get_dibujo(self):
        # ◢____◣
        # ██████
        # ██████
        # ██████
        # ◥▆▆▆▆◤
        # ◢▆▆▆▆◣
        # ██████
        # ██████
        # ██████
        # ◥‾‾‾‾◤

        if (self.fila_relativa == 0 and self.columna_relativa == 0):
            return '◢' if self.direccion == Direccion.NORTE else '◥'

        if (self.fila_relativa == 0 and 0 < self.columna_relativa < 5):
            return '_' if self.direccion == Direccion.NORTE else '‾'

        if (self.fila_relativa == 0 and self.columna_relativa == 5):
            return '◣' if self.direccion == Direccion.NORTE else '◤'

        if (0 < self.fila_relativa < 4):
            return '█'

        if (self.fila_relativa == 4 and self.columna_relativa == 0):
            return '◥' if self.direccion == Direccion.NORTE else '◢'

        if (self.fila_relativa == 4 and 0 < self.columna_relativa < 5):
            return '▆' if self.direccion == Direccion.NORTE else '▆'

        if (self.fila_relativa == 4 and self.columna_relativa == 5):
            return '◤' if self.direccion == Direccion.NORTE else '◣'

        return "?"

