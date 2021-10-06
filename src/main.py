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
    print(generar_numeros(gcl, n, semilla))


def ejercicio_1():
    gcl = fabricar_gcl(2**32, 1013904223, 1664525)
    n = 100
    padrones = [99535]
    suma = 0
    for padron in padrones:
        suma += padron

    promedio = np.int32(suma / len(padrones))
    semilla = promedio

    numeros = generar_numeros(gcl, n, semilla)
    print(numeros)
    # Hacer grafico
    plt.hist(numeros)
    plt.show()
    # Normalizado entre [0,1]


if __name__ == '__main__':
    prueba()
    ejercicio_1()
