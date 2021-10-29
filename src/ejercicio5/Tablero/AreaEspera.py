class AreaEspera:
    # Cuenta cuantos peatones tiene
    # Cuenta cuantos peatones cruzaron
    MAX_CANTIDAD_PEATONES = 100

    def __init__(self, posicion):
        self.peatones_esperando = 0
        self.peatones_cruzaron = 0
        self.posicion = posicion

    def peaton_arriba(self, sentido):
        if (sentido != self.posicion) and (self.peatones_esperando < self.MAX_CANTIDAD_PEATONES):
            self.peatones_esperando += 1

    def peaton_entra_paso_peatonal(self):
        self.peatones_esperando -= 1

    def peaton_cruza_paso_peatonal(self):
        self.peatones_cruzaron += 1
