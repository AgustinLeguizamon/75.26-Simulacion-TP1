from random import random
from numpy import array
from Entidades.Peaton import Peaton
from enums import Sentido
from .Celda import Celda
from Entidades.Poisson import Poisson
from utils import velocidad_inicial_peaton

class AreaEsperaPeaton:
    # Cuenta cuantos peatones tiene
    # Cuenta cuantos peatones cruzaron
    MAX_CANTIDAD_PEATONES = 100

    def __init__(self, celdas_iniciales: list[Celda], sentido_peatones: Sentido, peatones: list[Peaton]):
        self.celdas_iniciales = celdas_iniciales
        self.sentido_peatones = sentido_peatones
        self.peatones = peatones
        self.peatones_esperando = 0
        self.poisson = Poisson()
            
   # El área de espera chequea si tiene que colocar un peaton
    # en la senda peatonal
    def accionar(self, semaforos, tiempo):
        
        # Si llegamos al tope de peatones esperando, no hacemos nada
        if (self.peatones_esperando >= self.MAX_CANTIDAD_PEATONES):
            return

        # Si los semaforos no permiten el paso, no hacemos nada
        primer_semaforo = semaforos[0]
        segundo_semaforo = semaforos[1]
        if (not primer_semaforo.permitir_paso() or not segundo_semaforo.permitir_paso()):
            # No hacemos nada
            return

        # Si no hay una ocurrencia de evento de Poisson, no hacemos nada
        ocurre_evento = self.poisson.ocurrio_nuevo_evento(tiempo)
        if (not ocurre_evento):
            return
        
        # Sumamos un peaton a la senda peatonal, esperando para avanzar
        # en una de las celdas iniciales disponible del área de espera
        agregamos_peaton_en_senda = False
        for celda in self.celdas_iniciales:
            if celda.esta_ocupada():
                continue

            # La celda no está ocupada, sumamos al peaton a la senda peatonal
            # y a la colección de peatones
            peaton = Peaton(self.sentido_peatones, velocidad_inicial_peaton())
            celda.agregar_entidad(peaton)
            self.peatones.append(peaton)
            agregamos_peaton_en_senda = True
            break

        # Si el peatón fue agregado a una celda, listo
        # sino, sumamos 1 al contador de "peatones esperando" (ser agregados a la senda peatonal)
        if (not agregamos_peaton_en_senda):
            self.peatones_esperando += 1


