from Entidades.Peaton import Peaton
from enums import Direccion
from Entidades.Poisson import Poisson

class AreaEsperaPeaton:
    # Cuenta cuantos peatones tiene
    # Cuenta cuantos peatones cruzaron
    MAX_CANTIDAD_PEATONES = 100

    def __init__(self, celdas_matriz, posicion, origen_paso_peatonal_x, origen_paso_peatonal_y, paso_peatonal_ancho, calle_largo, peatones):
        self.peatones_esperando = 0
        self.peatones_cruzaron = 0
        self.posicion = posicion
        self.peatones = peatones

        self.celdas_generadoras = []
        
        self.preparar(celdas_matriz, origen_paso_peatonal_x, origen_paso_peatonal_y, paso_peatonal_ancho, calle_largo) 
    
    def preparar(self, celdas_matriz, origen_paso_peatonal_x, origen_paso_peatonal_y, paso_peatonal_ancho, calle_largo):
        if self.posicion == Direccion.OESTE:
            for i in range(paso_peatonal_ancho):
                self.celdas_generadoras.append(celdas_matriz[origen_paso_peatonal_y + i][origen_paso_peatonal_x])

        if self.posicion == Direccion.ESTE:
            for i in range(paso_peatonal_ancho):
                self.celdas_generadoras.append(celdas_matriz[origen_paso_peatonal_y + i][origen_paso_peatonal_x + calle_largo - 1])
            
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

    def colocar_peaton_en_paso_peatonal(self):
        for celda in self.celdas_generadoras:
            if (celda.esta_ocupada()):
                celda.ocupar("sss")
                self.peatones_esperando -= 1
        

    def peaton_cruza_paso_peatonal(self):
        self.peatones_cruzaron += 1
    
    # El área de espera chequea si tiene que colocar un peaton
    # en la senda peatonal
    def accionar(self, semaforos, tiempo):
        self.arribo_de_peaton(tiempo)
        primerSemaforo = semaforos[0]
        segundoSemaforo = semaforos[1]
        if (primerSemaforo and segundoSemaforo):
            self.colocar_peaton_en_paso_peatonal()
    def _debug_colocar_peaton(self, id, direccion, velocidad) -> bool:
        peaton = Peaton(id, direccion, velocidad)
        fue_colocado = False
        i = 0
        while not fue_colocado and i < len(self.celdas_generadoras):
            i += 1
            fue_colocado = self.celdas_generadoras[i].set_entidad(peaton)
            i += 1
        if fue_colocado:
            self.peatones.append(peaton)
        return fue_colocado
        
