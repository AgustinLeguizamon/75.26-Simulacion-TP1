import csv

def singleton(cls):
    instances = dict()
    def wrap(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs) 
        return instances[cls]
    return wrap

@singleton
class Estadisticas:
    def __init__(self):
        self.encabezados_arrivos = ['tiempo','tiempo_arribo']
        self.encabezados_cruce_completos = ['tiempo', 'completado']
        self.encabezados_conflictos = ['tiempo','conflicto']
        self.guardar_arrivos(self.encabezados_arrivos)
        self.guardar_cruce_completos(self.encabezados_cruce_completos)
        self.guardar_conflicto(self.encabezados_conflictos)

    
    def guardar_arrivos(self, datos):
        self.guarda_datos('_arribos.csv',datos)
    def guardar_cruce_completos(self, datos):
        self.guarda_datos('_cruce.csv',datos)
    def guardar_conflicto(self, datos):
        self.guarda_datos('_conflictos.csv',datos)
    def guarda_datos(self,archivo, datos):
        with open(archivo, 'a',newline='') as f:
            writer = csv.writer(f)
            writer.writerow(datos)