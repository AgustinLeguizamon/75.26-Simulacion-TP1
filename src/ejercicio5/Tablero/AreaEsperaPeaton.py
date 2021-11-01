from random import random
from numpy import array
from Entidades.Peaton import Peaton
from enums import Direccion
from .Celda import Celda
from Entidades.Poisson import Poisson
from utils import velocidad_inicial_peaton

class AreaEsperaPeaton:
    # Cuenta cuantos peatones tiene
    # Cuenta cuantos peatones cruzaron
    MAX_CANTIDAD_PEATONES = 100

    def __init__(self, celdas_iniciales: list[Celda], direccion_peatones: Direccion, peatones: list[Peaton]):
        self.celdas_iniciales = celdas_iniciales
        self.direccion_peatones = direccion_peatones
        self.peatones = peatones
        self.peatones_esperando = 0
        self.poisson = Poisson()
            
   # El área de espera chequea si tiene que colocar un peaton
    # en la senda peatonal
    def accionar(self, semaforos, tiempo):
        
        # Si llegamos al tope de peatones esperando, no hacemos nada
        if (self.peatones_esperando == self.MAX_CANTIDAD_PEATONES):
            return

        # Si los semaforos no permiten el paso, no hacemos nada
        se_permite_el_paso = True
        for semaforo in semaforos:
            se_permite_el_paso = se_permite_el_paso and semaforo.permitir_paso()
       
        if (not se_permite_el_paso):
            # No hacemos nada
            return
        
        # Luego chequeo si hay arribo de peaton según poisson 
        # Si no hay, no hago nada
        eventos_ocurridos = self.poisson.eventos_en_rango_de_tiempo(tiempo-1, tiempo)
        if (eventos_ocurridos == 0):
            return
        
        for i in range(eventos_ocurridos):
            # Sumamos un peaton a la senda peatonal, esperando para avanzar
            # en una de las celdas iniciales disponible del área de espera
            agregamos_peaton_en_senda = False
            for celda in self.celdas_iniciales:
                if celda.esta_ocupada():
                    continue

                # La celda no está ocupada, sumamos al peaton a la senda peatonal
                # y a la colección de peatones
                peaton = Peaton(self.direccion_peatones, velocidad_inicial_peaton())
                celda.agregar_entidad(peaton)
                self.peatones.append(peaton)
                agregamos_peaton_en_senda = True
                break

            # Si el peatón fue agregado a una celda, listo
            # sino, sumamos 1 al contador de "peatones esperando" (ser agregados a la senda peatonal)
            if (not agregamos_peaton_en_senda and self.peatones_esperando < self.MAX_CANTIDAD_PEATONES):
                self.peatones_esperando += 1


