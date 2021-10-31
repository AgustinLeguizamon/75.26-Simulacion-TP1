import random as rn
import numpy as np
class Poisson:
    def __init__(self, arribos_por_segundo = 5, muestras_a_generar = 10000):
        self.arribos_por_segundo = arribos_por_segundo
        self.muestras_a_generar = muestras_a_generar
                
        self.lambda_arribo = 1 / arribos_por_segundo
        self.ocurrencias_reportadas = 0
        self.tiempos_entre_arribos = []

        # Generamos una cantidad de muestras de distribución exponencial
        # cada una simboliza tiempos entre arribos
        for i in range(self.muestras_a_generar):
            muestra_uniforme = rn.random()
            muestra_exponencial = (-np.log(1-muestra_uniforme)) / self.lambda_arribo
            self.tiempos_entre_arribos.append(muestra_exponencial)

    def ocurrio_nuevo_evento(self, tiempo_actual):
        ocurrencias = 0
        tiempo_i = 0
        i = 0

        # TODO: remove
        return True

        # Chequeamos cuantos eventos/ocurrencias hubo en el tiempo que nos envian
        while(tiempo_i < tiempo_actual):
            tiempo_i += self.tiempos_entre_arribos[i]
            ocurrencias += 1
            i += 1

        # Si las ocurrencias reportadas son mayores o iguales a los eventos "ocurridos"
        # en ese rango de tiempo, no hay nada que reportar
        if (self.ocurrencias_reportadas >= ocurrencias):
            return False
            
        self.ocurrencias_reportadas += ocurrencias
        return True
