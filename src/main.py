import math
import random as rn
import matplotlib.pyplot as plt
import numpy as np
from scipy import special
from scipy.stats import chi2


def fabricar_gcl(modulo, multiplicador, incremento):
    def gcl(semilla):
        return (multiplicador * semilla + incremento) % modulo

    return gcl


def generar_numeros(generador, n, semilla):
    numeros_aleatorios = []
    numero_aleatorio = semilla
    for i in range(n):
        numero_aleatorio = generador(numero_aleatorio)

        numeros_aleatorios.append(numero_aleatorio)
    return numeros_aleatorios


# Normalizar entre [0,1]
def normalizar(numeros, modulo):
    numeros_normalizados = []
    for numero in numeros:
        numeros_normalizados.append(numero / modulo)
    return numeros_normalizados


def prueba():
    gcl = fabricar_gcl(10, 7, 7)
    n = 100
    semilla = 7
    print("Prueba")
    print(generar_numeros(gcl, n, semilla))


def gcl_ejercicio_1(n):
    modulo = 2 ** 32
    multiplicador = 1013904223
    incremento = 1664525
    gcl = fabricar_gcl(modulo, multiplicador, incremento)

    padrones = [99535, 100855, 98038, 89059]
    suma = 0

    for padron in padrones:
        suma += padron

    promedio = np.int32(suma / len(padrones))
    semilla = promedio
    numeros = generar_numeros(gcl, n, semilla)

    return numeros, modulo


# GCL del ejercicio 1.a
def rand(n):
    numeros, modulo = gcl_ejercicio_1(n)
    numeros_normalizados = normalizar(numeros, modulo)
    return numeros_normalizados


def ejercicio_1():
    n = 10000
    numeros, modulo = gcl_ejercicio_1(n)
    print("GCL ejercicio 1")
    # print(numeros)

    # Parte a
    numeros_normalizados = normalizar(numeros, modulo)
    print("GCL normalizado - ejercicio 1.a")
    # print(numeros_normalizados)

    # Parte b - plots
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.hist(numeros)
    plt.title("GCL \n")
    plt.ylabel("frecuencia")

    plt.subplot(2, 1, 2)
    plt.hist(numeros_normalizados)
    plt.title("\n GCL normalizado [0,1]")
    plt.ylabel("frecuencia")
    plt.xlabel("numeros")
    plt.show()


def ejercicio_2():
    # Ver como lograr el mismo histograma que en la fiugra del ejercicio 2
    print("ejercicio_2")
    n = 10000
    x = rand(n)
    z = np.zeros((5, n))

    probas_acumuladas = []
    for i in range(len(FRECUENCIAS_ESPERADAS)):
        if i == 0:
            probas_acumuladas.append(FRECUENCIAS_ESPERADAS[i])
        else:
            probas_acumuladas.append(probas_acumuladas[i - 1] + FRECUENCIAS_ESPERADAS[i])

    for i in range(n):
        if x[i] < probas_acumuladas[0]:
            z[0][i] = 1
        elif probas_acumuladas[0] < x[i] < probas_acumuladas[1]:
            z[1][i] = 1
        elif probas_acumuladas[1] < x[i] < probas_acumuladas[2]:
            z[2][i] = 1
        elif probas_acumuladas[2] < x[i] < probas_acumuladas[3]:
            z[3][i] = 1
        elif probas_acumuladas[3] < x[i] < probas_acumuladas[4]:
            z[4][i] = 1

    print("Probas acumuladas")
    print(probas_acumuladas)

    plt.figure()
    n_casos = []
    for i in range(len(z)):
        n_casos.append(np.sum(z[i]))
    k = [(i + 2) for i in range(len(z))]
    plt.bar(k, n_casos)
    plt.show()

    return n_casos


def ejercicio_2b(n_casos):
    diferencias = []
    lanzamientos = sum(n_casos)
    for i in range(len(FRECUENCIAS_ESPERADAS)):
        dif = ((n_casos[i] - FRECUENCIAS_ESPERADAS[i] * lanzamientos) ** 2) / (FRECUENCIAS_ESPERADAS[i] * lanzamientos)
        diferencias.append(dif)
    d2 = sum(diferencias)
    limite_superior = chi2.ppf(0.95, df=5)

    print("Estadistico: {:.6f} ".format(d2))
    if d2 <= limite_superior:
        print("El test acepta la hipotesis nula.")
    else:
        print("El test rechaza la hipótesis nula")


def funcion_densidad_normal(x, media, desvio):
    return (1 / (np.sqrt(desvio * 2 * math.pi))) * math.exp(-1 / 2 * (x - media / desvio) ** 2)


def generar_numeros_va_exp(muestras_uniformes, ratio):
    numeros_distribucion_exp = []
    for muestra_uniforme in muestras_uniformes:
        numeros_distribucion_exp.append(-np.log(muestra_uniforme))
    return numeros_distribucion_exp


def es_aceptada(instancia_uniforme, instancia_exponencial):
    # TODO: desharcodear esto creando metodo para calcular la funcion => f(x)/g(x)*c
    return instancia_uniforme <= math.exp(-(instancia_exponencial-1)**2 / 2)


# Metodo aceptacion y rechazo
def ejercicio_3():
    # Queremos normal N (15, 2**2)
    # la funcion de densidad de una normal es

    n = 100000
    media = 15
    desvio = 2
    proba_sea_positivo = 0.5

    muestras_normal_std = []

    # Genero valores uniformes con nuestro GCL
    muestras_uniforme = rand(n)

    # Con los uniformes usando la trnasformada inversa creo valores con distribucion exponencial
    muestras_exp = generar_numeros_va_exp(muestras_uniforme, 1)

    # Metodo aceptacion rechazo
    for i in range(n):
        if es_aceptada(rn.random(), muestras_exp[i]):
            muestra_exp = muestras_exp[i]
            # como quiero una normal que tiene soporte [-inf, +inf] pero exp tiene 0 a inf
            # hago que con proba 0.5 lo vuelvo negativo entonces tengo exp con [-0.5*inf, 0.5*inf]
            if rn.random() > proba_sea_positivo:
                muestra_exp = -muestra_exp
            muestras_normal_std.append(muestra_exp)

    # a cada elemento lo multiplico por desvio y suma la media
    # para obtener la normal buscada

    muestras_normal = []
    for i in range(len(muestras_normal_std)):
        muestras_normal.append(muestras_normal_std[i]*desvio + media)

    plt.hist(muestras_normal, align="left", bins=100)
    plt.show()

    return muestras_normal


def esperanza(muestras):
    sumatoria = 0
    for muestra in muestras:
        sumatoria += muestra
    return sumatoria / len(muestras)


def varianza(muestras, esperanza):
    sumatoria = 0
    for muestra in muestras:
        sumatoria += (muestra - esperanza) ** 2
    return sumatoria / len(muestras)


def probabilidades(numeros):
    frecuencias = {}
    n = len(numeros)

    for numero in numeros:
        if numero in frecuencias:
            frecuencias[numero] += 1
        else:
            frecuencias[numero] = 1
    return {k: frecuencias[k] / n for k, v in frecuencias.items()}


# CDF : Cumulative Distribution Function
def cdf_normal(x, media, desvio):
    return 0.5*(1 + special.erf((x - media)/(desvio * math.sqrt(2))))


def ejercicio_3_c(muestras):
    ocurrencias = {}

    media = 15
    desvio = 2
    n = len(muestras)

    for muestra in muestras:
        piso = math.floor(muestra)
        if piso in ocurrencias:
            ocurrencias[piso] += 1
        else:
            ocurrencias[piso] = 1

    diferencias = []
    for clase, ocurrencias in ocurrencias.items():
        pk = cdf_normal((clase+1 - media) / desvio, 0, 1) - cdf_normal((clase - media) / desvio, 0, 1)
        dif = (((ocurrencias - n * pk) ** 2) / (n * pk))
        diferencias.append(dif)
    d2 = sum(diferencias)
    limite_superior = chi2.ppf(0.95, df=5)

    print("Estadistico: {:.6f} ".format(d2))
    if d2 <= limite_superior:
        print("El test acepta la hipotesis nula.")
    else:
        print("El test rechaza la hipótesis nula")


def app():
    # ejercicio_1()
    # frecuencias_observadas = ejercicio_2()
    # ejercicio_2b(frecuencias_observadas)
    muestras_normal = ejercicio_3()
    ejercicio_3_c(muestras_normal)


if __name__ == '__main__':
    FRECUENCIAS_ESPERADAS = [0.273, 0.52, 0.137, 0.0480, 0.0220]
    app()
