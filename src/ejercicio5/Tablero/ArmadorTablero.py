from .AreaEsperaVehiculo import AreaEsperaVehiculo
from .Celda import Celda
from Entidades.Semaforo import Semaforo
from .AreaEsperaPeaton import AreaEsperaPeaton
from enums import TipoDeCelda, Direccion

class ArmadorTablero:
    #                     |      ╎ calle_largo ║██████╎      ╎      |                        
    #                     |      ╎      ╎      ║██████╎      ╎      |                      
    #                     |      ╎      ╎      ║██████╎      ╎      |                       <-- parte_superior_ancho
    #  vereda_izq_largo   |      ╎      ╎      ║◥▆▆▆▆◤╎      ╎      | vereda_der_largo
    #                     |      ╎      ╎      ║      ╎      ╎      |                     
    #                   🟢|=========================================|🔴                   
    #                    ◐|◐  ◑ ◑╎ ◑    ╎  ◐   ◐ ◐ ◐◑ ╎◢☗☗☗☗◣╎  ◐   |◑x9                    
    #                    ◐|  ◐   ╎◢☗☗☗☗◣╎ ◑   ◐║◐ ◑   ◐██████╎ ◐  ◑ |                    
    #                    ◐| ◑ ◑◐ ╎██████╎  ◐ ◐ ║  ◑ ◐ |██████╎◐   ◑ |                     <-- parte_peatonal_ancho
    #                    ◐| ◐    ◐██████╎   ◐  ║ ◑    ◐██████◐  ◑   |◑                    
    #                    ◐|  ◐  ◐╎██████◐  ◐  ◑║  ◐ ◑ ╎◥▆▆▆▆◤╎ ◑◐   |◑                    
    #                    ◐| ◐  ◑ ╎◥▆▆▆▆◤╎ ◐◑  ◑║◑   ◐◑╎ ◑  ◑ ╎    ◐ |◑                    
    #                     |=====================◢☗☗☗☗◣===============                      
    #                     |◢☗☗☗☗◣╎      ╎      ║██████╎      ╎      |                     
    #                     |██████╎      ╎      ║██████╎      |                     
    # ____________________|      ╎      ╎      ║      ╎      ╎      |______________________
    # Road segment: two-way six-vehicle lanes (3x2)
    # Each lane’s width is 3.5 meters (3.5m per lane)
    # Cells: 0.5 × 0.5 m2 square cells. Each cell is either occupied by one pedestrian or empty.
    # Crosswalk: 
    #  - Width: 21 m crossing length -> 42 cells (crossing length == street length)
    #  - Height 2.5 m (5 cells), 3 m, 3.5 m, 4 m, 4.5 m and 5 m (10 cells) --> 6 classes
    # Vehicle: 
    #  - Each vehicle is assumed to occupy 6×5 cells
    #  - Horizontal: 6*0,5m = 3m
    #  - Vertical:   5*0,5m = 2,5m
   

    def __init__(self, tablero):  
        self.calle_largo = tablero.calle_largo
        self.paso_peatonal_ancho = tablero.paso_peatonal_ancho
        self.cantidad_de_carriles = tablero.cantidad_de_carriles
        self.ancho_carril = tablero.ancho_carril
        self.ancho_celda = tablero.ancho_celda

        self.ancho_vereda = 10

        # Definimos el largo del tablero (en cantidad de celdas) Largo == Width == lo horizontal
        self.vereda_izquierda_largo = int(self.ancho_vereda / self.ancho_celda)
        self.calle_largo = int(self.calle_largo / self.ancho_celda)
        self.vereda_derecha_largo = int(self.ancho_vereda / self.ancho_celda)
        tablero_largo = int(self.vereda_izquierda_largo + self.calle_largo + self.vereda_derecha_largo)

        # Definimos el ancho del tablero (en cantidad de celdas) Ancho == Height == lo vertical
        self.parte_superior_ancho = int(4 / self.ancho_celda)
        self.cantidad_separadores = 2
        self.parte_peatonal_ancho = int(self.paso_peatonal_ancho / self.ancho_celda) + self.cantidad_separadores # 2 más porque incluye separadores
        self.parte_inferior_ancho = int(4 / self.ancho_celda)
        self.tablero_ancho = int(self.parte_superior_ancho + self.parte_peatonal_ancho + self.parte_inferior_ancho)

        self.celdas_matriz = []
        self.semaforos = []
        self.vehiculos = []
        self.peatones = []
        self.areas_de_espera = []

    def armar_tablero(self):
        

        # Creamos las celdas columna objetos del tablero
        for fila in range(self.tablero_ancho):
            celdas_fila = []
            columna = 0

            if (fila < self.parte_superior_ancho):
                fila, columna, celdas_fila = self.generar_parte_superior(fila, columna, celdas_fila, self.vereda_izquierda_largo, self.vereda_derecha_largo, self.parte_superior_ancho)
                self.celdas_matriz.append(celdas_fila)
                continue

            if (fila < self.parte_superior_ancho + self.parte_peatonal_ancho):
                fila, columna, celdas_fila = self.generar_parte_peatonal(fila, columna, celdas_fila, self.vereda_izquierda_largo, self.vereda_derecha_largo, self.calle_largo, self.parte_superior_ancho, self.parte_peatonal_ancho)
                self.celdas_matriz.append(celdas_fila)
                continue

            fila, columna, celdas_fila = self.generar_parte_inferior(fila, columna, celdas_fila, self.vereda_izquierda_largo, self.vereda_derecha_largo)
            self.celdas_matriz.append(celdas_fila)
        
        # Creamos el área de espera de los peatones a la izquierda (lado oeste, sentido este)
        area_espera_izquierda_fila = self.parte_superior_ancho + 1
        area_espera_izquierda_columna = self.vereda_izquierda_largo - 1
        celdas_iniciales_area_izquierda = []

        for i in range(self.parte_peatonal_ancho - 2):
            celda = self.get_celda(area_espera_izquierda_fila + i, area_espera_izquierda_columna)
            celdas_iniciales_area_izquierda.append(celda)

        area_espera_izquierda = AreaEsperaPeaton(celdas_iniciales_area_izquierda, Direccion.ESTE, self.peatones)
        self.areas_de_espera.append(area_espera_izquierda)

        # Creamos el área de espera de los peatones a la derecha (lado este, sentido oeste)
        area_espera_derecha_fila = self.parte_superior_ancho + 1
        area_espera_derecha_columna = self.vereda_izquierda_largo + self.calle_largo + 1
        celdas_iniciales_area_derecha = []

        for i in range(self.parte_peatonal_ancho - 2):
            celda = self.get_celda(area_espera_derecha_fila + i, area_espera_derecha_columna)
            celdas_iniciales_area_derecha.append(celda)

        area_espera_derecha = AreaEsperaPeaton(celdas_iniciales_area_derecha, Direccion.OESTE, self.peatones)
        self.areas_de_espera.append(area_espera_derecha)

        # Creamos las áreas de espera de autos
        carril_ancho_celdas = int(self.ancho_carril / self.ancho_celda)
        cantidad_de_carriles_por_sentido = int(self.cantidad_de_carriles / 2)

        fila_inicial_norte = 0
        columna_inicial_norte = self.vereda_izquierda_largo + 1
        for numero_de_carril in range(cantidad_de_carriles_por_sentido):
            celda_inicial = self.get_celda(fila_inicial_norte, columna_inicial_norte + (numero_de_carril * carril_ancho_celdas))
            area_de_espera = AreaEsperaVehiculo(celda_inicial, self.celdas_matriz, Direccion.SUR, self.vehiculos)
            self.areas_de_espera.append(area_de_espera)

        fila_inicial_sur = len(self.celdas_matriz) - 1
        columna_inicial_sur = self.vereda_izquierda_largo + 1 + int(cantidad_de_carriles_por_sentido * carril_ancho_celdas)
        for numero_de_carril in range(cantidad_de_carriles_por_sentido):
            celda_inicial = self.get_celda(fila_inicial_sur, columna_inicial_sur + (numero_de_carril * carril_ancho_celdas))
            area_de_espera = AreaEsperaVehiculo(celda_inicial, self.celdas_matriz, Direccion.NORTE, self.vehiculos)
            self.areas_de_espera.append(area_de_espera)

        # Agregamos los semáforos en las celdas de la verda donde arranca la senda peatonal
        semaforo_izquierdo_fila = self.parte_superior_ancho
        semaforo_izquierdo_columna = self.vereda_izquierda_largo - 1
        semaforo_izquierdo = Semaforo()
        self.celdas_matriz[semaforo_izquierdo_fila][semaforo_izquierdo_columna].agregar_entidad(semaforo_izquierdo)
        self.semaforos.append(semaforo_izquierdo)

        semaforo_derecho_fila = self.parte_superior_ancho
        semaforo_derecho_columna = self.vereda_izquierda_largo + self.calle_largo + 1
        semaforo_derecho = Semaforo()
        self.celdas_matriz[semaforo_derecho_fila][semaforo_derecho_columna].agregar_entidad(semaforo_derecho)
        self.semaforos.append(semaforo_derecho)

    def generar_parte_superior(self, fila, columna, celdas_fila, vereda_izquierda_largo, vereda_derecha_largo, parte_superior_ancho):
        # Vereda izquierda: todas celdas normales (espacios vacíos)
        fila, columna, celdas_fila = self.generar_celdas_normales(fila, columna, celdas_fila, self.vereda_izquierda_largo)

        # Agregamos una celda separadora al final de la vereda
        celdas_fila.append(Celda(fila=fila, columna=columna, tipo=TipoDeCelda.VEREDA_CORDON, tablero=self))
        columna += 1

        fila, columna, celdas_fila = self.generar_carriles(fila, columna, celdas_fila)

        # Vereda derecha: todas celdas normales (espacios vacíos)
        fila, columna, celdas_fila = self.generar_celdas_normales(fila, columna, celdas_fila, self.vereda_derecha_largo)

        return fila, columna, celdas_fila

    def generar_parte_peatonal(self, fila, columna, celdas_fila, vereda_izquierda_largo, vereda_derecha_largo, calle_largo, parte_superior_ancho, parte_peatonal_ancho):
        # Vereda izquierda: todas celdas normales (espacios vacíos)
        fila, columna, celdas_fila = self.generar_celdas_normales(fila, columna, celdas_fila, self.vereda_izquierda_largo)

        # Agregamos una celda separadora al final de la vereda
        celdas_fila.append(Celda(fila=fila, columna=columna, tipo=TipoDeCelda.VEREDA_CORDON, tablero=self))
        columna += 1

        # Parte central
        # - Si es la primera o la última fila, va separador peatonal
        # - Sino va carril
        es_primera_fila = fila == int(parte_superior_ancho)
        es_ultima_fila = fila == int(parte_superior_ancho + parte_peatonal_ancho - 1)
        
        if (es_primera_fila or es_ultima_fila):
            fila, columna, celdas_fila = self.generar_separador_peatonal(fila, columna, celdas_fila, calle_largo)
        else:
            fila, columna, celdas_fila = self.generar_carriles(fila, columna, celdas_fila)

        # Vereda derecha: todas celdas normales (espacios vacíos)
        fila, columna, celdas_fila = self.generar_celdas_normales(fila, columna, celdas_fila, self.vereda_derecha_largo)

        return fila, columna, celdas_fila

    def generar_parte_inferior(self, fila, columna, celdas_fila, vereda_izquierda_largo, vereda_derecha_largo):
        # Vereda izquierda: todas celdas normales (espacios vacíos)
        fila, columna, celdas_fila = self.generar_celdas_normales(fila, columna, celdas_fila, self.vereda_izquierda_largo)

        # Agregamos una celda separadora al final de la vereda
        celdas_fila.append(Celda(fila=fila, columna=columna, tipo=TipoDeCelda.VEREDA_CORDON, tablero=self))
        columna += 1

        fila, columna, celdas_fila = self.generar_carriles(fila, columna, celdas_fila)

        # Vereda derecha: todas celdas normales (espacios vacíos)
        fila, columna, celdas_fila = self.generar_celdas_normales(fila, columna, celdas_fila, self.vereda_derecha_largo)

        return fila, columna, celdas_fila

    def generar_carriles(self, fila, columna, celdas_fila):
        # Carriles: conformados por celdas normales (espacios vacíos) columna un separador al final
        carril_ancho_celdas = int(self.ancho_carril / self.ancho_celda)

        for i in range(self.cantidad_de_carriles):
            for j in range(carril_ancho_celdas - 1):
                celdas_fila.append(Celda(fila=fila, columna=columna, tipo=TipoDeCelda.NORMAL, tablero=self))
                columna += 1
            
            if (i != self.cantidad_de_carriles - 1):
                carril_del_medio = int((self.cantidad_de_carriles - 1) / 2)
                tipo_de_carril = TipoDeCelda.CARRIL_SEPARADOR_DEL_MEDIO if carril_del_medio == i else TipoDeCelda.CARRIL_SEPARADOR 
                celdas_fila.append(Celda(fila=fila, columna=columna, tipo=tipo_de_carril, tablero=self))
                columna += 1

        # Agregamos una celda separadora al final de los carriles
        celdas_fila.append(Celda(fila=fila, columna=columna, tipo=TipoDeCelda.VEREDA_CORDON, tablero=self))
        columna += 1

        return fila, columna, celdas_fila

    def generar_separador_peatonal(self, fila, columna, celdas_fila, calle_largo):
        # Agregamos un separador por el largo de la calle
        cantidad_de_separadores = calle_largo - 1
        for i in range(cantidad_de_separadores):
            celdas_fila.append(Celda(fila=fila, columna=columna, tipo=TipoDeCelda.SEPARADOR_PEATONAL, tablero=self))
            columna += 1

        # Agregamos una celda al final para la vereda
        celdas_fila.append(Celda(fila=fila, columna=columna, tipo=TipoDeCelda.VEREDA_CORDON, tablero=self))
        columna += 1

        return fila, columna, celdas_fila

    def generar_celdas_normales(self, fila, columna, celdas_fila, cantidad):
        for i in range(cantidad):
            celdas_fila.append(Celda(fila=fila, columna=columna, tipo=TipoDeCelda.NORMAL, tablero=self))
            columna += 1

        return fila, columna, celdas_fila

    def get_celda(self, fila, columna) -> Celda:
        if (fila < 0 or fila >= len(self.celdas_matriz)) or (columna < 0 or columna >= len(self.celdas_matriz[0])):
            return None

        return self.celdas_matriz[fila][columna]
