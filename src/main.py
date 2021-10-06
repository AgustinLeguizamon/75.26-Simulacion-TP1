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


if __name__ == '__main__':
    gcl = fabricar_gcl(10, 7, 7)
    N = 10
    SEMILLA = 7
    print(generar_numeros(gcl, N, SEMILLA))
