from collections import Counter
import random
import statistics
import time


def ordenar_por_mezcla(numeros):
    if len(numeros) <= 1:
        return numeros.copy()

    medio = len(numeros) // 2
    izquierda = ordenar_por_mezcla(numeros[:medio])
    derecha = ordenar_por_mezcla(numeros[medio:])
    resultado = []
    i = j = 0

    while i < len(izquierda) and j < len(derecha):
        if izquierda[i] <= derecha[j]:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1

    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])
    return resultado


def ordenar_por_monticulo(numeros):
    resultado = numeros.copy()
    cantidad = len(resultado)

    def bajar_monticulo(raiz, limite):
        mayor = raiz
        hijo_izquierdo = 2 * raiz + 1
        hijo_derecho = 2 * raiz + 2

        if hijo_izquierdo < limite and resultado[hijo_izquierdo] > resultado[mayor]:
            mayor = hijo_izquierdo
        if hijo_derecho < limite and resultado[hijo_derecho] > resultado[mayor]:
            mayor = hijo_derecho
        if mayor != raiz:
            resultado[raiz], resultado[mayor] = resultado[mayor], resultado[raiz]
            bajar_monticulo(mayor, limite)

    for raiz in range(cantidad // 2 - 1, -1, -1):
        bajar_monticulo(raiz, cantidad)

    for ultimo in range(cantidad - 1, 0, -1):
        resultado[0], resultado[ultimo] = resultado[ultimo], resultado[0]
        bajar_monticulo(0, ultimo)

    return resultado


def calcular_estadisticas(numeros):
    frecuencias = Counter(numeros)
    frecuencia_maxima = max(frecuencias.values())
    modas = (
        [numero for numero, frecuencia in frecuencias.items() if frecuencia == frecuencia_maxima]
        if frecuencia_maxima > 1
        else []
    )

    return statistics.mean(numeros), statistics.median(numeros), sorted(modas)


def pedir_cantidad():
    while True:
        try:
            cantidad = int(input("¿Cuántos números aleatorios quieres generar? "))
            if cantidad > 0:
                return cantidad
            print("La cantidad debe ser mayor que cero.")
        except ValueError:
            print("Escribe un número entero válido.")


def main():
    algoritmos = {
        "1": ("Timsort de Python (sorted)", sorted),
        "2": ("Ordenamiento por mezcla", ordenar_por_mezcla),
        "3": ("Ordenamiento por montículo", ordenar_por_monticulo),
    }

    cantidad = pedir_cantidad()
    numeros = [random.randint(1, 100) for _ in range(cantidad)]
    print(f"\nLista generada: {numeros}")

    print("\nElige el algoritmo para ordenar la lista:")
    for opcion, (nombre, _) in algoritmos.items():
        print(f"{opcion}. {nombre}")

    while True:
        opcion = input("Opción: ").strip()
        if opcion in algoritmos:
            break
        print("Opción no válida. Elige 1, 2 o 3.")

    nombre_elegido, algoritmo_elegido = algoritmos[opcion]
    lista_ordenada = algoritmo_elegido(numeros)
    print(f"\nLista ordenada con {nombre_elegido}: {lista_ordenada}")

    print("\nComparación de tiempos (la misma lista para cada algoritmo):")
    for nombre, algoritmo in algoritmos.values():
        inicio = time.perf_counter()
        resultado = algoritmo(numeros)
        duracion = time.perf_counter() - inicio
        if resultado != sorted(numeros):
            raise RuntimeError(f"El algoritmo «{nombre}» produjo un orden incorrecto.")
        print(f"- {nombre}: {duracion:.6f} segundos")

    media, mediana, modas = calcular_estadisticas(lista_ordenada)
    print("\nEstadísticas:")
    print(f"- Media: {media:.2f}")
    print(f"- Mediana: {mediana}")
    print(f"- Moda(s): {modas if modas else 'no hay (ningún número se repite)'}")


if __name__ == "__main__":
    main()
