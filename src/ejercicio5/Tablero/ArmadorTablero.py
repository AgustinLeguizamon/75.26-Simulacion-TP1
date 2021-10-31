from .AreaEsperaVehiculo import AreaEsperaVehiculo
from .Celda import Celda
from Entidades.Semaforo import Semaforo
from .AreaEsperaPeaton import AreaEsperaPeaton
from enums import TipoDeCelda, Sentido

class ArmadorTablero:
    #                     |      ╎ calle_largo ║██████╎      ╎      |                        
    #                     |      ╎      ╎      ║██████╎      ╎      |                      
    #                     |      ╎      ╎      ║██████╎      ╎      |                       <-- parte_superior_ancho
    #  vereda_izq_largo   |      ╎      ╎      ║◥▆▆▆▆◤╎      ╎      | vereda_der_largo
    #                     |      ╎      ╎      ║      ╎      ╎      |                     
    #                     |🟢======================================🔴|                   
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

        self.celdas_matriz = []
        self.semaforos = []
        self.vehiculos = []
        self.peatones = []
        self.areas_de_espera = []

    def armar_tablero(self):
        ancho_vereda = 10

        # Definimos el largo del tablero (en cantidad de celdas) Largo == Width == lo horizontal
        vereda_izquierda_largo = int(ancho_vereda / self.ancho_celda)
        calle_largo = int(self.calle_largo / self.ancho_celda)
        vereda_derecha_largo = int(ancho_vereda / self.ancho_celda)
        tablero_largo = int(vereda_izquierda_largo + calle_largo + vereda_derecha_largo)

        # Definimos el ancho del tablero (en cantidad de celdas) Ancho == Height == lo vertical
        parte_superior_ancho = int(4 / self.ancho_celda)
        cantidad_separadores = 2
        parte_peatonal_ancho = int(self.paso_peatonal_ancho / self.ancho_celda) + cantidad_separadores # 2 más porque incluye separadores
        parte_inferior_ancho = int(4 / self.ancho_celda)
        tablero_ancho = int(parte_superior_ancho + parte_peatonal_ancho + parte_inferior_ancho)

        # Creamos las celdas columna objetos del tablero
        for fila in range(tablero_ancho):
            celdas_fila = []
            columna = 0

            if (fila < parte_superior_ancho):
                fila, columna, celdas_fila = self.generar_parte_superior(fila, columna, celdas_fila, vereda_izquierda_largo, vereda_derecha_largo, parte_superior_ancho)
                self.celdas_matriz.append(celdas_fila)
                continue

            if (fila < parte_superior_ancho + parte_peatonal_ancho):
                fila, columna, celdas_fila = self.generar_parte_peatonal(fila, columna, celdas_fila, vereda_izquierda_largo, vereda_derecha_largo, calle_largo, parte_superior_ancho, parte_peatonal_ancho)
                self.celdas_matriz.append(celdas_fila)
                continue

            fila, columna, celdas_fila = self.generar_parte_inferior(fila, columna, celdas_fila, vereda_izquierda_largo, vereda_derecha_largo)
            self.celdas_matriz.append(celdas_fila)
        
        # Creamos el área de espera de los peatones a la izquierda (lado oeste, sentido este)
        area_espera_izquierda_fila = parte_superior_ancho + 1
        area_espera_izquierda_columna = vereda_izquierda_largo - 1
        celdas_iniciales_area_izquierda = []

        for i in range(parte_peatonal_ancho - 2):
            celda = self.get_celda(area_espera_izquierda_fila + i, area_espera_izquierda_columna)
            celdas_iniciales_area_izquierda.append(celda)

        area_espera_izquierda = AreaEsperaPeaton(celdas_iniciales_area_izquierda, Sentido.ESTE, self.peatones)
        self.areas_de_espera.append(area_espera_izquierda)

        # Creamos el área de espera de los peatones a la derecha (lado este, sentido oeste)
        area_espera_derecha_fila = parte_superior_ancho + 1
        area_espera_derecha_columna = vereda_izquierda_largo + calle_largo + 1
        celdas_iniciales_area_derecha = []

        for i in range(parte_peatonal_ancho - 2):
            celda = self.get_celda(area_espera_derecha_fila + i, area_espera_derecha_columna)
            celdas_iniciales_area_derecha.append(celda)

        area_espera_derecha = AreaEsperaPeaton(celdas_iniciales_area_derecha, Sentido.OESTE, self.peatones)
        self.areas_de_espera.append(area_espera_derecha)

        # Creamos las áreas de espera de autos
        carril_ancho_celdas = int(self.ancho_carril / self.ancho_celda)
        cantidad_de_carriles_por_sentido = int(self.cantidad_de_carriles / 2)

        fila_inicial_norte = 0
        columna_inicial_norte = vereda_izquierda_largo + 1
        for numero_de_carril in range(cantidad_de_carriles_por_sentido):
            celda_inicial = self.get_celda(fila_inicial_norte, columna_inicial_norte + (numero_de_carril * carril_ancho_celdas))
            area_de_espera = AreaEsperaVehiculo(celda_inicial, Sentido.SUR, self.vehiculos)
            self.areas_de_espera.append(area_de_espera)

        fila_inicial_sur = len(self.celdas_matriz) - 1
        columna_inicial_sur = vereda_izquierda_largo + 1 + int(cantidad_de_carriles_por_sentido * carril_ancho_celdas)
        for numero_de_carril in range(cantidad_de_carriles_por_sentido):
            celda_inicial = self.get_celda(fila_inicial_sur, columna_inicial_sur + (numero_de_carril * carril_ancho_celdas))
            area_de_espera = AreaEsperaVehiculo(celda_inicial, Sentido.NORTE, self.vehiculos)
            self.areas_de_espera.append(area_de_espera)

    def generar_parte_superior(self, fila, columna, celdas_fila, vereda_izquierda_largo, vereda_derecha_largo, parte_superior_ancho):
        # Vereda izquierda: todas celdas normales (espacios vacíos)
        fila, columna, celdas_fila = self.generar_celdas_normales(fila, columna, celdas_fila, vereda_izquierda_largo)

        # Agregamos una celda separadora al final de la vereda
        celdas_fila.append(Celda(fila=fila, columna=columna, tipo=TipoDeCelda.VEREDA_CORDON, tablero=self))
        columna += 1

        fila, columna, celdas_fila = self.generar_carriles(fila, columna, celdas_fila)

        # Vereda derecha: todas celdas normales (espacios vacíos)
        fila, columna, celdas_fila = self.generar_celdas_normales(fila, columna, celdas_fila, vereda_derecha_largo)

        return fila, columna, celdas_fila

    def generar_parte_peatonal(self, fila, columna, celdas_fila, vereda_izquierda_largo, vereda_derecha_largo, calle_largo, parte_superior_ancho, parte_peatonal_ancho):
        # Vereda izquierda: todas celdas normales (espacios vacíos)
        fila, columna, celdas_fila = self.generar_celdas_normales(fila, columna, celdas_fila, vereda_izquierda_largo)

        # Agregamos una celda separadora al final de la vereda
        celdas_fila.append(Celda(fila=fila, columna=columna, tipo=TipoDeCelda.VEREDA_CORDON, tablero=self))
        columna += 1

        # Parte central
        # 1. Si es la primera fila peatonal, va separador con semáforos
        # 2. Si es la última fila peatonal, va separador sin semáforos
        # 3. Sino, va carril
        separador_con_semaforos = fila == int(parte_superior_ancho)
        separador_sin_semaforos = fila == int(parte_superior_ancho + parte_peatonal_ancho - 1)
        
        if (separador_con_semaforos or separador_sin_semaforos):
            fila, columna, celdas_fila = self.generar_separador_peatonal(fila, columna, celdas_fila, calle_largo, separador_con_semaforos)
        else:
            fila, columna, celdas_fila = self.generar_carriles(fila, columna, celdas_fila)

        # Vereda derecha: todas celdas normales (espacios vacíos)
        fila, columna, celdas_fila = self.generar_celdas_normales(fila, columna, celdas_fila, vereda_derecha_largo)

        return fila, columna, celdas_fila

    def generar_parte_inferior(self, fila, columna, celdas_fila, vereda_izquierda_largo, vereda_derecha_largo):
        # Vereda izquierda: todas celdas normales (espacios vacíos)
        fila, columna, celdas_fila = self.generar_celdas_normales(fila, columna, celdas_fila, vereda_izquierda_largo)

        # Agregamos una celda separadora al final de la vereda
        celdas_fila.append(Celda(fila=fila, columna=columna, tipo=TipoDeCelda.VEREDA_CORDON, tablero=self))
        columna += 1

        fila, columna, celdas_fila = self.generar_carriles(fila, columna, celdas_fila)

        # Vereda derecha: todas celdas normales (espacios vacíos)
        fila, columna, celdas_fila = self.generar_celdas_normales(fila, columna, celdas_fila, vereda_derecha_largo)

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

    def generar_separador_peatonal(self, fila, columna, celdas_fila, calle_largo, separador_con_semaforos):

        if (separador_con_semaforos):
            # Agregamos semáforo, celda columna los asociamos
            semaforo = Semaforo(fila=fila, columna=columna)
            celda = Celda(fila=fila, columna=columna, tipo=TipoDeCelda.NORMAL, entidad=semaforo, tablero=self)
            
            self.semaforos.append(semaforo)
            celdas_fila.append(celda)
            columna += 1

        # Agregamos un separador por el largo de la calle
        cantidad_de_separadores = calle_largo - (3 if separador_con_semaforos else 0)
        for i in range(cantidad_de_separadores):
            celdas_fila.append(Celda(fila=fila, columna=columna, tipo=TipoDeCelda.SEPARADOR_PEATONAL, tablero=self))
            columna += 1

        if (separador_con_semaforos):
            # Agregamos semáforo al final
            semaforo = Semaforo(fila=fila, columna=columna)
            celda = Celda(fila=fila, columna=columna, tipo=TipoDeCelda.NORMAL, entidad=semaforo, tablero=self)
            
            self.semaforos.append(semaforo)
            celdas_fila.append(celda)
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