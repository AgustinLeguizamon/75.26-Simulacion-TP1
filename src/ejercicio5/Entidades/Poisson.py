import random as rn
import numpy as np
class Poisson:
    _PARAMETRO_ARRIBO_PEATON = 1/120
    def generar (self):
        muestra_uniforme = rn.random()
        return (-np.log(1-muestra_uniforme))/self._PARAMETRO_ARRIBO_PEATON