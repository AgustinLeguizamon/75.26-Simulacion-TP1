
def metros_a_celdas(metros):
    celdas_por_metro = 2
    return metros * celdas_por_metro


def probabilidad(proba):
    p = random.random()
    return p < proba


def velocidad_inicial():
    p = random.random()
    velocidad = 2
    if p > 0.978:
        velocidad = 6
        return velocidad
    if p > 0.93:
        velocidad = 5
        return velocidad
    if p > 0.793:
        velocidad = 4
        return velocidad
    if p > 0.273:
        velocidad = 3
        return velocidad
    return velocidad

class PasoPeatonal:
    def __init__(self, ancho):
        self.largo = metros_a_celdas(21)
        self.ancho = metros_a_celdas(ancho)
        self.paso_peatonal = [[Celda(x, y, self) for x in range(self.ancho)] for y in range(self.largo)]
        self.peatones = []
        self.sig_id = 0
        self.calle_norte = AreaEspera(Sentido.NORTE)
        self.calle_sur = AreaEspera(Sentido.SUR)
        self.vehiculos = []

    def peaton_arriba(self, sentido):
        # TODO: evento de poisson
        self.calle_sur.peaton_arriba(sentido)
        self.calle_norte.peaton_arriba(sentido)

    # TODO: una vez que termino de testear, los peatones van a empezar siempre en el extremo de cada paso peatonal
    def agregar_peaton(self, inicial_x, inicial_y, sentido, velocidad=-1):
        _velocidad = velocidad
        if velocidad == -1:
            _velocidad = velocidad_inicial()
        peaton = Peaton(self.sig_id, sentido, _velocidad)
        self.sig_id = self.sig_id + 1
        self.peatones.append(peaton)
        self.poner_peaton(peaton, inicial_x, inicial_y)

    def poner_vehiculo(self, inicial_x, inicial_y, vehiculo):
        vehiculo.set_posicion(inicial_x, inicial_y)
        # veo si la posicion del auto termina fuera del paso peatonal y lo elimino
        if inicial_x + vehiculo.LARGO < 0 or inicial_x > self.ancho:
            vehiculo.estas_afuera()
        else:
            for x in range(Vehiculo.LARGO):
                for y in range(Vehiculo.ANCHO):
                    # Si se va del paso peatonal simplemente no le asigna una celda
                    # es decir queda un cacho del vehiculo
                    if 0 <= inicial_y + y < self.largo and 0 <= inicial_x + x < self.ancho:
                        vehiculo.asignar_celda(x, y, self.paso_peatonal[inicial_y + y][inicial_x + x])

    def agregar_vehiculo(self, inicial_x, inicial_y, sentido):
        vehiculo = Vehiculo(sentido)
        self.vehiculos.append(vehiculo)
        self.poner_vehiculo(inicial_x, inicial_y, vehiculo)

    def poner_peaton(self, peaton, x, y):
        if x < 0 or x >= self.ancho:
            raise PeatonNoPuedeSalirPorLosLateralesExcepcion
        # si se fue del tablero no lo coloco
        if y < 0 or y > self.largo - 1:
            peaton.setear_celda(None)
            return
        self.paso_peatonal[y][x].poner_movible(peaton)

    def quitar_movible(self, x, y):
        peaton = self.paso_peatonal[y][x].quitar_movible()
        return peaton

    def mover_peaton(self, x, y, velocidad, sentido):
        d = self.distancia_al_prox_peaton(x, y, sentido)
        # print("sentido: " + str(sentido) + " - distancia:" + str(d))
        peaton = self.quitar_movible(x, y)
        regla = self.cambio_de_linea(x, y, velocidad, sentido)
        if regla == Regla.AMBOS:
            # muevo movible
            x += 1 if probabilidad(0.5) else -1
        elif regla == Regla.DER:
            x += -sentido.value
        elif regla == Regla.IZQ:
            x += sentido.value
        if regla != Regla.NINGUNA:
            # Recalculo distancia despues de resolver conflicto
            d = self.distancia_al_prox_peaton(x, y, sentido)
        # el peaton en este turno no se mueve si no puedo resolver el conflicto, pero mantiene la velocidad
        velocidad = 0
        if regla != Regla.NO_RESUELTO:
            # si resulta que no hubo conflicto actualizo la velocidad
            velocidad = peaton.actualizar_velocidad(d)
        self.poner_peaton(peaton, x, y + velocidad * sentido.value)

    def puede_moverse(self, inicial_x, inicial_y):
        for offset_x in range(Vehiculo.LARGO):
            for offset_y in range(Vehiculo.ANCHO):
                x = inicial_x + offset_x
                y = inicial_y + offset_y
                # si esta dentro del paso_peatonal y esta ocupada entonces no se puede mover
                if 0 <= x < self.ancho and 0 <= y < self.largo and self.paso_peatonal[y][x].ocupada:
                    return False
        return True

    def mover_vehiculo(self, vehiculo, paso_x, paso_y):
        self.poner_vehiculo(vehiculo.x + vehiculo.velocidad * paso_x, vehiculo.y + paso_y, vehiculo)

    def pasar_un_segundo(self):
        # TODO: peaton_arriba()
        # TODO: peaton_entra_paso_peatonal()
        for peaton in self.peatones:
            peaton.dar_paso()
        for vehiculo in self.vehiculos:
            vehiculo.dar_paso(self)
        # Todos aquellos peatones que esten fuera del tablero son eliminados
        self.peatones = [peaton for peaton in self.peatones if peaton.celda is not None]
        self.vehiculos = [vehiculo for vehiculo in self.vehiculos if not vehiculo.esta_afuera]

    def distancia_al_prox_peaton(self, x, y, sentido):
        d = 0
        limite = self.largo
        hay_peaton_adelante = False
        if sentido == Sentido.NORTE:
            limite = -1
        for j in range(y + sentido.value, limite, sentido.value):
            if self.paso_peatonal[j][x].ocupada:
                hay_peaton_adelante = True
                break
            d += 1
        # si resulta que no hay nadie adelante, la distancia es inf
        if not hay_peaton_adelante:
            d = INF
        return d

    def cambio_de_linea(self, x, y, velocidad, sentido):
        # si su velocidad es 0, break
        # TODO: para optimizar, si no se meuve no tiene sentido cambiar de linea
        if velocidad == 0:
            return Regla.NINGUNA
        # si tiene uno adelante:
        # condicion1 = Celda(x,y-1).ocupada
        condicion1 = self.distancia_al_prox_peaton(x, y, sentido) == 0

        # si no se cumple la condicion de conflicto, break
        if not condicion1:
            return Regla.NINGUNA

        # defino que es derecha e izquierda segun el sentido
        derecha = 1
        if sentido == Sentido.SUR:
            derecha = -1
        izquierda = -derecha
        # a la derecha y a la izquierda esta vacio:
        # condicion2 = not Celda(x-1,y).ocupada and not Celda(x+1,y).ocupada
        tiene_carril_der = 0 <= (x + derecha) < self.ancho
        tiene_carril_izq = 0 <= (x + izquierda) < self.ancho
        tiene_vecino_der = tiene_carril_der and self.paso_peatonal[y][x + derecha].ocupada
        tiene_vecino_izq = tiene_carril_izq and self.paso_peatonal[y][x + izquierda].ocupada

        if tiene_vecino_izq and tiene_vecino_der:
            return Regla.NO_RESUELTO
        # la distancia al vecino lateral mas cercano es mayor a su velocidad actual
        # condicion3 = distancia_al_prox_vecino_izq_adelante() > mi_velocidad
        # condicion4 = distancia_al_prox_vecino_der_adelante() > mi_velocidad
        condicion3 = tiene_carril_izq and self.distancia_al_prox_peaton(x + izquierda, y, sentido) > velocidad
        condicion4 = tiene_carril_der and self.distancia_al_prox_peaton(x + derecha, y, sentido) > velocidad

        # 'velocidad de los primeros vecinos laterales que estan n celdas mas atras' es
        # menor a mi velocidad actual
        # distancia_al_prox_vecino_der_atras() > mi_velocidad
        # distancia_al_prox_vecino_izq_atras() > mi_velocidad
        condicion5 = True
        condicion6 = True
        sentido_contrario = Sentido.NORTE
        if sentido == Sentido.NORTE:
            sentido_contrario = Sentido.SUR

        if tiene_carril_izq:
            condicion5 = self.mi_velocidad_mayor_vecino_lateral_atras(izquierda, sentido_contrario, x, y, velocidad)

        if tiene_carril_der:
            condicion6 = self.mi_velocidad_mayor_vecino_lateral_atras(derecha, sentido_contrario, x, y, velocidad)

        if condicion1 and not tiene_vecino_der and not tiene_vecino_izq and condicion3 and condicion4 and condicion5 and condicion6:
            return Regla.AMBOS
        if condicion1 and not tiene_vecino_der and condicion4 and condicion6:
            return Regla.DER
        if condicion1 and not tiene_vecino_izq and condicion3 and condicion5:
            return Regla.IZQ
        return Regla.NO_RESUELTO

    def mi_velocidad_mayor_vecino_lateral_atras(self, lateral, sentido_contrario, x, y, velocidad):
        distancia_lateral_atras = self.distancia_al_prox_peaton(x + lateral, y, sentido_contrario)
        vecino_lateral_atras = None
        if distancia_lateral_atras != INF:
            vecino_lateral_atras = self.paso_peatonal[y + distancia_lateral_atras * sentido_contrario.value +
                                                      sentido_contrario.value][x + lateral]
        return not vecino_lateral_atras or velocidad > vecino_lateral_atras.movible.velocidad
