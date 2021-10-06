import matplotlib.pyplot as plt
import numpy as np


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


def prueba():
    gcl = fabricar_gcl(10, 7, 7)
    n = 100
    semilla = 7
    print("Prueba")
    print(generar_numeros(gcl, n, semilla))


def gcl_ejercicio_1():
    modulo = 2 ** 32
    gcl = fabricar_gcl(modulo, 1013904223, 1664525)
    n = 100
    padrones = [99535]
    suma = 0
    for padron in padrones:
        suma += padron
    promedio = np.int32(suma / len(padrones))
    semilla = promedio
    numeros = generar_numeros(gcl, n, semilla)

    return numeros, modulo


def ejercicio_1():
    numeros, modulo = gcl_ejercicio_1()
    print(numeros)

    # Normalizado entre [0,1]
    numeros_normalizados = []
    for numero in numeros:
        numeros_normalizados.append(numero / modulo)

    print("GCL normalizado")
    print(numeros_normalizados)

    # plots
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


if __name__ == '__main__':
    prueba()
    ejercicio_1()

    