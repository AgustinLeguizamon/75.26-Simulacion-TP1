import random as rn
import numpy as np
class Poisson:
    def __init__(self, arribos_por_segundo = 5, muestras_a_generar = 10000):
        self.muestras_a_generar = muestras_a_generar
        self.lambda_arribo = arribos_por_segundo
        self.ocurrencias_reportadas = 0
        self.tiempos_entre_arribos = []

        # Generamos una cantidad de muestras de distribución exponencial
        # cada una simboliza tiempos entre arribos
        for i in range(self.muestras_a_generar):
            muestra_uniforme = rn.random()
            muestra_exponencial = (-np.log(1-muestra_uniforme)) / self.lambda_arribo
            self.tiempos_entre_arribos.append(muestra_exponencial)

            
    def cantidad_eventos_hasta(self, tiempo_maximo):
        if (tiempo_maximo <= 0):
            return 0
        tiempo_acumulado = 0
        cantidad_eventos = 0
        while (tiempo_acumulado <= tiempo_maximo):
            tiempo_acumulado = tiempo_acumulado + self.tiempos_entre_arribos[cantidad_eventos];
            cantidad_eventos = cantidad_eventos + 1
        return cantidad_eventos

    def eventos_en_rango_de_tiempo(self, tiempo_anterior, tiempo_actual) -> int:
        eventos_tiempo_anterior = self.cantidad_eventos_hasta(tiempo_anterior)
        eventos_tiempo_actual = self.cantidad_eventos_hasta(tiempo_actual)
        return abs(eventos_tiempo_actual-eventos_tiempo_anterior)
