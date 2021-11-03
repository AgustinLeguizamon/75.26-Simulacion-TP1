from .AreaEsperaVehiculo import AreaEsperaVehiculo
from .Celda import Celda
from Entidades.Semaforo import Semaforo
from .AreaEsperaPeaton import AreaEsperaPeaton
from enums import TipoDeCelda, Direccion
from Entidades.Poisson import Poisson
from .Constantes import Constantes

class ArmadorTablero:
    #                     |      ╎ calle_largo ║██████╎      ╎      |                        
    #                     |      ╎      ╎      ║██████╎      ╎      |                      
    #                     |      ╎      ╎      ║██████╎      ╎      |                       <-- parte_superior_ancho
    #  vereda_izq_largo   |      ╎      ╎      ║◥▆▆▆▆◤╎      ╎      | vereda_der_largo
    #                     |      ╎      ╎      ║      ╎      ╎      |                     
    #                   🟢|=========================================|🔴                   
    #                    ◐|◐  ◑ ◑╎ ◑    ╎  ◐   ◐ ◐ ◐◑ ╎◢____◣╎  ◐   |◑x9                    
    #                    ◐|  ◐   ╎◢____◣╎ ◑   ◐║◐ ◑   ◐██████╎ ◐  ◑ |                    
    #                    ◐| ◑ ◑◐ ╎██████╎  ◐ ◐ ║  ◑ ◐ |██████╎◐   ◑ |                     <-- parte_peatonal_ancho
    #                    ◐| ◐    ◐██████╎   ◐  ║ ◑    ◐██████◐  ◑   |◑                    
    #                    ◐|  ◐  ◐╎██████◐  ◐  ◑║  ◐ ◑ ╎◥▆▆▆▆◤╎ ◑◐   |◑                    
    #                    ◐| ◐  ◑ ╎◥▆▆▆▆◤╎ ◐◑  ◑║◑   ◐◑╎ ◑  ◑ ╎    ◐ |◑                    
    #                     |=====================◢____◣===============                      
    #                     |◢____◣╎      ╎      ║██████╎      ╎      |                     
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
        # Definimos el largo del tablero (en cantidad de celdas) Largo == Width == lo horizontal
        self.vereda_izquierda_largo = int(Constantes.ANCHO_VEREDA_METROS / Constantes.ANCHO_CELDA_METROS)
        self.calle_largo = int(Constantes.CALLE_LARGO_METROS / Constantes.ANCHO_CELDA_METROS)
        self.vereda_derecha_largo = int(Constantes.ANCHO_VEREDA_METROS / Constantes.ANCHO_CELDA_METROS)
        tablero_largo = int(self.vereda_izquierda_largo + self.calle_largo + self.vereda_derecha_largo)

        # Definimos el ancho del tablero (en cantidad de celdas) Ancho == Height == lo vertical
        self.parte_superior_ancho = int(Constantes.ANCHO_PARTE_SUPERIOR_METROS / Constantes.ANCHO_CELDA_METROS)
        self.parte_peatonal_ancho = int(Constantes.PASO_PEATONAL_ANCHO_METROS / Constantes.ANCHO_CELDA_METROS) + 2 # 2 más porque incluye separadores
        self.parte_inferior_ancho = int(Constantes.ANCHO_PARTE_INFERIOR_METROS / Constantes.ANCHO_CELDA_METROS)
        self.tablero_ancho = int(self.parte_superior_ancho + self.parte_peatonal_ancho + self.parte_inferior_ancho)

        self.celdas_matriz = []
        self.semaforos = []
        self.vehiculos = {}
        self.peatones = []
        self.areas_de_espera = []

    def armar_tablero(self, generar_area_peaton_izquierda, generar_area_peaton_derecha):
        
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
        
        if generar_area_peaton_izquierda:
            self.generar_area_de_espera_izquierda()

        if generar_area_peaton_derecha:
            self.generar_area_de_espera_derecha()

        # Creamos las áreas de espera de autos
        carril_ancho_celdas = int(Constantes.ANCHO_CARRIL_METROS / Constantes.ANCHO_CELDA_METROS)
        cantidad_de_carriles_por_sentido = int(Constantes.CANTIDAD_DE_CARRILES / 2)
        largo_auto = 5

        fila_inicial_norte = largo_auto - 1
        columna_inicial_norte = self.vereda_izquierda_largo + 1

        for numero_de_carril in range(cantidad_de_carriles_por_sentido):
            celda_inicial = self.get_celda(fila_inicial_norte, columna_inicial_norte + (numero_de_carril * carril_ancho_celdas))
            area_de_espera = AreaEsperaVehiculo(celda_inicial, self.celdas_matriz, Direccion.SUR, self.vehiculos)
            self.areas_de_espera.append(area_de_espera)

        fila_inicial_sur = len(self.celdas_matriz) - largo_auto
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
        carril_ancho_celdas = int(Constantes.ANCHO_CARRIL_METROS / Constantes.ANCHO_CELDA_METROS)

        for i in range(Constantes.CANTIDAD_DE_CARRILES):
            for j in range(carril_ancho_celdas - 1):
                celdas_fila.append(Celda(fila=fila, columna=columna, tipo=TipoDeCelda.NORMAL, tablero=self))
                columna += 1
            
            if (i != Constantes.CANTIDAD_DE_CARRILES - 1):
                carril_del_medio = int((Constantes.CANTIDAD_DE_CARRILES - 1) / 2)
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
    
    def generar_area_de_espera_izquierda(self):
    # Creamos el área de espera de los peatones a la izquierda (lado oeste, sentido este)
        area_espera_izquierda_fila = self.parte_superior_ancho + 1
        area_espera_izquierda_columna = self.vereda_izquierda_largo - 1
        celdas_iniciales_area_izquierda = []

        for i in range(self.parte_peatonal_ancho - 2):
            celda = self.get_celda(area_espera_izquierda_fila + i, area_espera_izquierda_columna)
            celdas_iniciales_area_izquierda.append(celda)

        area_espera_izquierda = AreaEsperaPeaton(celdas_iniciales_area_izquierda, Direccion.ESTE, self.peatones)
        self.areas_de_espera.append(area_espera_izquierda)

    def generar_area_de_espera_derecha(self):
        area_espera_derecha_fila = self.parte_superior_ancho + 1
        area_espera_derecha_columna = self.vereda_izquierda_largo + self.calle_largo + 1
        celdas_iniciales_area_derecha = []

        for i in range(self.parte_peatonal_ancho - 2):
            celda = self.get_celda(area_espera_derecha_fila + i, area_espera_derecha_columna)
            celdas_iniciales_area_derecha.append(celda)

        area_espera_derecha = AreaEsperaPeaton(celdas_iniciales_area_derecha, Direccion.OESTE, self.peatones)
        self.areas_de_espera.append(area_espera_derecha)


    def get_celda(self, fila, columna) -> Celda:
        if (fila < 0 or fila >= len(self.celdas_matriz)) or (columna < 0 or columna >= len(self.celdas_matriz[0])):
            return None

        return self.celdas_matriz[fila][columna]
