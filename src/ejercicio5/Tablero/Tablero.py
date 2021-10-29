from .Celda import Celda
from enums import TipoDeCelda

class Tablero:
    #                     |      ╎ calle_largo ║██████╎      ╎      |                        
    #                     |      ╎      ╎      ║██████╎      ╎      |                      
    #                     |      ╎      ╎      ║██████╎      ╎      |                       <-- parte_superior_ancho
    #  vereda_izq_largo   |      ╎      ╎      ║◥▆▆▆▆◤╎      ╎      | vereda_der_largo
    #                     |      ╎      ╎      ║      ╎      ╎      |                     
    #                     |🟢======================================🔴|                   
    #                    ◐|◐  ◑ ◑╎ ◑    ╎  ◐   ◐ ◐ ◐◑ ╎◢☗☗☗☗◣╎  ◐   |◑                    
    #                    ◐|  ◐   ╎◢☗☗☗☗◣╎ ◑   ◐║◐ ◑   ◐██████╎ ◐  ◑ |◑                    
    #                    ◐| ◑ ◑◐ ╎██████╎  ◐ ◐ ║  ◑ ◐ |██████╎◐   ◑ |◑                     <-- parte_peatonal_ancho
    #                    ◐| ◐    ◐██████╎   ◐  ║ ◑    ◐██████◐  ◑   |◑                    
    #                    ◐|  ◐  ◐╎██████◐  ◐  ◑║  ◐ ◑ ╎◥▆▆▆▆◤╎ ◑◐   |◑                    
    #                    ◐| ◐  ◑ ╎◥▆▆▆▆◤╎ ◐◑  ◑║◑   ◐◑╎ ◑  ◑ ╎    ◐ |◑                    
    #                     |=====================◢☗☗☗☗◣===============                      
    #                     |◢☗☗☗☗◣╎      ╎      ║██████╎      ╎      |                     
    #                     |██████╎      ╎      ║██████╎      ╎◢☗☗☗☗◣|                     
    #                     |██████╎      ╎      ║██████╎      ╎██████|                     
    #                     |██████╎      ╎      ║◥▆▆▆▆◤╎      ╎██████|                      <-- parte_inferior_ancho
    #                     |◥▆▆▆▆◤╎      ╎      ║      ╎      ╎██████|                     
    #                     |      ╎      ╎      ║      ╎      ╎◥▆▆▆▆◤|                     
    #                     |      ╎      ╎      ║      ╎      ╎      |                     
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
    def __init__(self, calle_largo = 21, paso_peatonal_ancho = 2.5, cantidad_de_carriles = 6, ancho_carril = 3.5, ancho_celda = 0.5):  
        self.calle_largo = calle_largo
        self.paso_peatonal_ancho = paso_peatonal_ancho
        self.cantidad_de_carriles = cantidad_de_carriles
        self.ancho_carril = ancho_carril
        self.ancho_celda = ancho_celda

        self.celdas_matriz = []
        self.vehiculos = []
        self.peatones = []
        self.semaforos = []

        self.armar_tablero()
        
        pass

    def armar_tablero(self):
        # Definimos el largo del tablero (en cantidad de celdas) Largo == Width == lo horizontal
        vereda_izquierda_largo = int(10 / self.ancho_celda)
        calle_largo = int(self.calle_largo / self.ancho_celda)
        vereda_derecha_largo = int(10 / self.ancho_celda)
        tablero_largo = int(vereda_izquierda_largo + calle_largo + vereda_derecha_largo)

        # Definimos el ancho del tablero (en cantidad de celdas) Ancho == Height == lo vertical
        parte_superior_ancho = 4 / self.ancho_celda
        parte_peatonal_ancho = self.paso_peatonal_ancho / self.ancho_celda + 2 # 2 más porque incluye separadores
        parte_inferior_ancho = 4 / self.ancho_celda
        tablero_ancho = int(parte_superior_ancho + parte_peatonal_ancho + parte_inferior_ancho)

        # Creamos las celdas y objetos del tablero
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


    def generar_parte_superior(self, fila, columna, celdas_fila, vereda_izquierda_largo, vereda_derecha_largo, parte_superior_ancho):
        # Vereda izquierda: todas celdas normales (espacios vacíos)
        fila, columna, celdas_fila = self.generar_celdas_normales(fila, columna, celdas_fila, vereda_izquierda_largo)

        # Agregamos una celda separadora al final de la vereda
        celdas_fila.append(Celda(x=fila, y=columna, tipo=TipoDeCelda.VEREDA_CORDON))
        columna += 1

        fila, columna, celdas_fila = self.generar_carriles(fila, columna, celdas_fila)

        # Vereda derecha: todas celdas normales (espacios vacíos)
        fila, columna, celdas_fila = self.generar_celdas_normales(fila, columna, celdas_fila, vereda_derecha_largo)

        return fila, columna, celdas_fila

    def generar_parte_peatonal(self, fila, columna, celdas_fila, vereda_izquierda_largo, vereda_derecha_largo, calle_largo, parte_superior_ancho, parte_peatonal_ancho):
        # Vereda izquierda: todas celdas normales (espacios vacíos)
        fila, columna, celdas_fila = self.generar_celdas_normales(fila, columna, celdas_fila, vereda_izquierda_largo)

        # Agregamos una celda separadora al final de la vereda
        celdas_fila.append(Celda(x=fila, y=columna, tipo=TipoDeCelda.VEREDA_CORDON))
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
        celdas_fila.append(Celda(x=fila, y=columna, tipo=TipoDeCelda.VEREDA_CORDON))
        columna += 1

        fila, columna, celdas_fila = self.generar_carriles(fila, columna, celdas_fila)

        # Vereda derecha: todas celdas normales (espacios vacíos)
        fila, columna, celdas_fila = self.generar_celdas_normales(fila, columna, celdas_fila, vereda_derecha_largo)

        return fila, columna, celdas_fila

    def generar_carriles(self, fila, columna, celdas_fila):
        # Carriles: conformados por celdas normales (espacios vacíos) y un separador al final
        celdas_carril = int(self.ancho_carril / self.ancho_celda)
        for i in range(self.cantidad_de_carriles):
            for j in range(celdas_carril - 1):
                celdas_fila.append(Celda(x=fila, y=columna, tipo=TipoDeCelda.NORMAL))
                columna += 1
            
            if (i != self.cantidad_de_carriles - 1):
                carril_del_medio = int((self.cantidad_de_carriles - 1) / 2)
                tipo_de_carril = TipoDeCelda.CARRIL_SEPARADOR_DEL_MEDIO if carril_del_medio == i else TipoDeCelda.CARRIL_SEPARADOR 
                celdas_fila.append(Celda(x=fila, y=columna, tipo=tipo_de_carril))
                columna += 1

        # Agregamos una celda separadora al final de los carriles
        celdas_fila.append(Celda(x=fila, y=columna, tipo=TipoDeCelda.VEREDA_CORDON))
        columna += 1

        return fila, columna, celdas_fila

    def generar_separador_peatonal(self, fila, columna, celdas_fila, calle_largo, separador_con_semaforos):

        if (separador_con_semaforos):
            # Agregamos semáforo al principio
            celdas_fila.append(Celda(x=fila, y=columna, tipo=TipoDeCelda.SEMAFORO))
            columna += 1

        # Agregamos un separador por el largo de la calle
        cantidad_de_separadores = calle_largo - (3 if separador_con_semaforos else 0)
        for i in range(cantidad_de_separadores):
            celdas_fila.append(Celda(x=fila, y=columna, tipo=TipoDeCelda.SEPARADOR_PEATONAL))
            columna += 1

        if (separador_con_semaforos):
            # Agregamos semáforo al final
            celdas_fila.append(Celda(x=fila, y=columna, tipo=TipoDeCelda.SEMAFORO))
            columna += 1

        return fila, columna, celdas_fila

    def generar_celdas_normales(self, fila, columna, celdas_fila, cantidad):
        for i in range(cantidad):
            celdas_fila.append(Celda(x=fila, y=columna, tipo=TipoDeCelda.NORMAL))
            columna += 1

        return fila, columna, celdas_fila

    def dibujar(self):
        # Dibujamos las celdas
        i = 0
        for celdas_fila in self.celdas_matriz:
            print() # Newline
            for celda_fila in celdas_fila:
                print(celda_fila.get_dibujo(),end =" ")

