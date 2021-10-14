import math

import matplotlib.pyplot as plt
import numpy as np
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

    padrones = [99535]
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


def funcion_densidad_normal_std(x):
    return 2 / (np.sqrt(2 * math.pi)) * math.exp((x ** 2) / 2)


def generar_numeros_va_exp(muestras_uniformes, ratio):
    numeros_distribucion_exp = []
    for muestra_uniforme in muestras_uniformes:
        numeros_distribucion_exp.append(-np.log(muestra_uniforme))
    return numeros_distribucion_exp


def es_aceptada(instancia_uniforme, instancia_exponencial):
    return instancia_uniforme <= math.exp(-(instancia_exponencial-1)**2 / 2)


# Metodo aceptacion y rechazo
def ejercicio_3():
    # Queremos normal N (15, 2**2)
    # la funcion de densidad de una normal es

    n = 100000
    media = 15
    desvio = 2

    nros = []
    muestras_uniformes = rand(n)
    muestras_exp = generar_numeros_va_exp(muestras_uniformes, 1)
    for i in range(n):
        if es_aceptada(muestras_uniformes[i], muestras_exp[i]):
            nros.append(muestras_exp[i])

    plt.hist(nros, align="left", bins=30)
    plt.show()


def app():
    # ejercicio_1()
    # frecuencias_observadas = ejercicio_2()
    # ejercicio_2b(frecuencias_observadas)
    ejercicio_3()


if __name__ == '__main__':
    FRECUENCIAS_ESPERADAS = [0.273, 0.52, 0.137, 0.0480, 0.0220]
    app()
