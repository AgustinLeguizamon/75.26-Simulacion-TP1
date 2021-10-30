from enums import Movimiento
from Entidades.Poisson import Poisson

class AreaEspera:
    # Cuenta cuantos peatones tiene
    # Cuenta cuantos peatones cruzaron
    MAX_CANTIDAD_PEATONES = 100

    def __init__(self, celdas_matriz, posicion, origen_paso_peatonal_x, origen_paso_peatonal_y, paso_peatonal_ancho):
        self.peatones_esperando = 0
        self.peatones_cruzaron = 0
        self.posicion = posicion

        self.celdas_generadoras = []
        
        self.preparar(celdas_matriz, origen_paso_peatonal_x, origen_paso_peatonal_y, paso_peatonal_ancho) 
    
    def preparar(self, celdas_matriz, origen_paso_peatonal_x, origen_paso_peatonal_y, paso_peatonal_ancho):
        if self.posicion == Movimiento.OESTE:
            for i in range(paso_peatonal_ancho):
                self.celdas_generadoras.append(celdas_matriz[origen_paso_peatonal_y + i][origen_paso_peatonal_x])
            
    # Generamos un nuevo arribo de peaton según las condiciones establecidas
    # Si se genera un nuevo arribo, sumamos un contador para luego crear un peaton
    def arribo_de_peaton(self, tiempo):
        ocurre_evento = self.calcular_ocurrencia_arribo_de_peaton(tiempo)
        if (ocurre_evento and self.peatones_esperando < self.MAX_CANTIDAD_PEATONES):
            self.peatones_esperando += 1
                

    # Calcula la ocurrencia del evento del arribo del peaton
    # Retorna: true si arriba un peaton, false caso contrario
    def calcular_ocurrencia_arribo_de_peaton(self, tiempo) -> bool:
        poisson = Poisson()
        tiempo_arribo = poisson.generar()
        return tiempo_arribo < tiempo

    def peaton_entra_paso_peatonal(self):
        # peaton = Peaton()
        # celda.agregar_movible(peaton)
        self.peatones_esperando -= 1

    def peaton_cruza_paso_peatonal(self):
        self.peatones_cruzaron += 1
