from random import random
from numpy import array
from Entidades.Peaton import Peaton
from enums import Direccion
from .Celda import Celda
from Entidades.Poisson import Poisson
from utils import velocidad_inicial_peaton
from Estadisticas import Estadisticas
from .Constantes import Constantes

class AreaEsperaPeaton:
    def __init__(self, celdas_iniciales: 'list[Celda]', direccion_peatones: Direccion, peatones: 'list[Peaton]'):
        self.celdas_iniciales = celdas_iniciales
        self.direccion_peatones = direccion_peatones
        self.peatones = peatones
        self.peatones_esperando = 0
        self.poisson = Poisson(Constantes.ARRIBO_POR_SEGUNDO_PEATON)
        
    
    # El área de espera chequea si tiene que colocar un peaton
    # en la senda peatonal
    def accionar(self, semaforos, tiempo_transcurrido, segundos_por_paso):
        
        # Si llegamos al tope de peatones esperando, no hacemos nada
        if (self.peatones_esperando == Constantes.MAX_CANTIDAD_PEATONES):
            return

        # Si los semaforos no permiten el paso, no hacemos nada
        se_permite_el_paso = True
        for semaforo in semaforos:
            se_permite_el_paso = se_permite_el_paso and semaforo.permitir_paso()
        
        # Luego chequeo si hay arribo de peaton según poisson 
        # Si no hay, no hago nada
        eventos_ocurridos = self.poisson.eventos_en_rango_de_tiempo(tiempo_transcurrido - segundos_por_paso, tiempo_transcurrido)
        if (eventos_ocurridos == 0):
            return
        
        for i in range(eventos_ocurridos):
            
            if (self.peatones_esperando < Constantes.MAX_CANTIDAD_PEATONES):
                self.peatones_esperando += 1
        
        if se_permite_el_paso:
            self.meter_peatones(segundos_por_paso)


    def meter_peatones(self, segundos_por_paso):
        # Sumamos un peaton a la senda peatonal, esperando para avanzar
        # en una de las celdas iniciales disponible del área de espera
        for celda in self.celdas_iniciales:
            if celda.esta_ocupada():
                continue     
            peaton = Peaton(self.direccion_peatones, velocidad_inicial_peaton(segundos_por_paso))
            celda.agregar_entidad(peaton)
            self.peatones.append(peaton)
            self.peatones_esperando -= 1
            if self.peatones_esperando <= 0:
                return

        

         
