"""
Módulo para encontrar el par de puntos más cercano usando divide y conquista.

Este módulo implementa el algoritmo de divide y conquista para encontrar
el par de puntos con la menor distancia euclidiana en un conjunto de puntos
en el plano 2D.

Examples
--------
>>> puntos = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
>>> p1, p2, dist = encontrar_par_mas_cercano(puntos)
>>> print(f"Puntos: {p1}, {p2}, Distancia: {dist:.4f}")
Puntos: (2, 3), (3, 4), Distancia: 1.4142

Notes
-----
El algoritmo tiene complejidad O(n log n) en el caso promedio.

References
----------
.. [1] Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009).
       Introduction to Algorithms (3rd ed.). MIT Press.
.. [2] Shamos, M. I., & Hoey, D. (1975). Closest-point problems.
       Proceedings of the 16th Annual Symposium on Foundations of Computer
       Science, 151-162.
"""

import math
import time


class ContadoresAlgoritmo:
    """
    Clase para mantener contadores de llamadas a funciones.

    Attributes
    ----------
    llamadas : int
        Contador de llamadas recursivas.
    fuerza_bruta : int
        Contador de llamadas a fuerza bruta.
    distancia : int
        Contador de cálculos de distancia.
    franja : int
        Contador de búsquedas en franja.
    """

    def __init__(self):
        """Inicializa todos los contadores en cero."""
        self.llamadas = 0
        self.fuerza_bruta = 0
        self.distancia = 0
        self.franja = 0

    def reiniciar(self):
        """Reinicia todos los contadores a cero."""
        self.llamadas = 0
        self.fuerza_bruta = 0
        self.distancia = 0
        self.franja = 0


# Instancia global de contadores
contadores = ContadoresAlgoritmo()


def leer_puntos_archivo(nombre_archivo):
    """
    Lee puntos desde un archivo de texto.

    Lee coordenadas x e y desde un archivo con formato específico:
    primera línea contiene valores x separados por comas,
    segunda línea contiene valores y separados por comas.

    Parameters
    ----------
    nombre_archivo : str
        Ruta del archivo de texto a leer.

    Returns
    -------
    list of tuple
        Lista de tuplas (x, y) representando los puntos.

    Raises
    ------
    FileNotFoundError
        Si el archivo no existe.
    ValueError
        Si el formato del archivo es incorrecto o los datos no son válidos.

    Notes
    -----
    El archivo debe tener exactamente dos líneas:
    - Línea 1: coordenadas x separadas por comas
    - Línea 2: coordenadas y separadas por comas
    Ambas líneas deben tener la misma cantidad de valores.

    Examples
    --------
    >>> puntos = leer_puntos_archivo('puntos.txt')
    >>> print(puntos[:3])
    [(2.0, 3.0), (12.0, 30.0), (40.0, 50.0)]

    References
    ----------
    .. [1] Python Software Foundation. (2024). Built-in Functions.
           https://docs.python.org/3/library/functions.html
    """
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()

            if len(lineas) < 2:
                raise ValueError("El archivo debe contener al menos 2 líneas")

            coordenadas_x = [float(x.strip()) for x in lineas[0].split(',')]
            coordenadas_y = [float(y.strip()) for y in lineas[1].split(',')]

            if len(coordenadas_x) != len(coordenadas_y):
                raise ValueError("Las coordenadas x e y deben tener la "
                                 "misma cantidad de valores")

            if len(coordenadas_x) < 2:
                raise ValueError("Se necesitan al menos 2 puntos")

            puntos = list(zip(coordenadas_x, coordenadas_y))
            return puntos

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{nombre_archivo}'")
        raise
    except ValueError as error:
        print(f"Error al leer el archivo: {error}")
        raise


def calcular_distancia(punto1, punto2):
    """
    Calcula la distancia euclidiana entre dos puntos.

    Utiliza la fórmula de distancia euclidiana en 2D:
    d = sqrt((x2-x1)^2 + (y2-y1)^2)

    Parameters
    ----------
    punto1 : tuple
        Primer punto como tupla (x, y).
    punto2 : tuple
        Segundo punto como tupla (x, y).

    Returns
    -------
    float
        Distancia euclidiana entre los dos puntos.

    Notes
    -----
    Esta función es fundamental para el algoritmo de par más cercano
    y se llama múltiples veces durante la ejecución.

    Se incrementa un contador cada vez que se invoca
    para análisis de rendimiento.

    Examples
    --------
    >>> d = calcular_distancia((0, 0), (3, 4))
    >>> print(f"{d:.2f}")
    5.00

    >>> d = calcular_distancia((1, 1), (1, 1))
    >>> print(f"{d:.2f}")
    0.00

    References
    ----------
    .. [1] Weisstein, E. W. "Distance." From MathWorld--A Wolfram Web Resource.
           https://mathworld.wolfram.com/Distance.html
    """
    contadores.distancia += 1

    diferencia_x = punto1[0] - punto2[0]
    diferencia_y = punto1[1] - punto2[1]
    return math.sqrt(diferencia_x ** 2 + diferencia_y ** 2)


def fuerza_bruta_par_cercano(puntos):
    """
    Encuentra el par más cercano usando fuerza bruta.

    Compara todos los pares posibles de puntos para encontrar
    el par con la menor distancia. Se usa para conjuntos pequeños.

    Parameters
    ----------
    puntos : list of tuple
        Lista de puntos como tuplas (x, y).

    Returns
    -------
    tuple
        Tupla con tres elementos: (punto1, punto2, distancia_minima)
        donde punto1 y punto2 son los puntos más cercanos y
        distancia_minima es la distancia entre ellos.

    Notes
    -----
    Complejidad temporal: O(n^2)
    Este método se utiliza como caso base en el algoritmo de
    divide y conquista cuando el número de puntos es pequeño (≤ 3).

    Se incrementa un contador cada vez que se invoca
    para análisis de rendimiento.

    Examples
    --------
    >>> puntos = [(0, 0), (1, 1), (5, 5)]
    >>> p1, p2, dist = fuerza_bruta_par_cercano(puntos)
    >>> print(f"Distancia: {dist:.4f}")
    Distancia: 1.4142

    References
    ----------
    .. [1] Sedgewick, R., & Wayne, K. (2011). Algorithms (4th ed.).
           Addison-Wesley.
    """
    contadores.fuerza_bruta += 1

    numero_puntos = len(puntos)
    distancia_minima = float('inf')
    punto_mas_cercano1 = None
    punto_mas_cercano2 = None

    for i in range(numero_puntos):
        for j in range(i + 1, numero_puntos):
            distancia = calcular_distancia(puntos[i], puntos[j])
            if distancia < distancia_minima:
                distancia_minima = distancia
                punto_mas_cercano1 = puntos[i]
                punto_mas_cercano2 = puntos[j]

    return punto_mas_cercano1, punto_mas_cercano2, distancia_minima


def par_cercano_en_franja(franja, delta, mejor_par):
    """
    Encuentra el par más cercano en la franja central.

    Busca pares de puntos en la franja que puedan estar más cerca
    que la distancia delta encontrada en las mitades izquierda y derecha.

    Parameters
    ----------
    franja : list of tuple
        Lista de puntos en la franja, ordenados por coordenada y.
    delta : float
        Distancia mínima encontrada en las mitades.
    mejor_par : tuple
        Tupla (punto1, punto2, distancia) del mejor par actual.

    Returns
    -------
    tuple
        Tupla con tres elementos: (punto1, punto2, distancia_minima)
        representando el mejor par encontrado.

    Notes
    -----
    Este es el paso "conquista" del algoritmo divide y conquista.
    Solo necesita comparar cada punto con un máximo de 7 puntos
    siguientes, lo que mantiene la complejidad en O(n).

    Se incrementa un contador cada vez que se invoca
    para análisis de rendimiento.

    Examples
    --------
    >>> franja = [(2, 1), (3, 2), (2.5, 3)]
    >>> mejor = ((0, 0), (5, 0), 5.0)
    >>> p1, p2, dist = par_cercano_en_franja(franja, 5.0, mejor)

    References
    ----------
    .. [1] Preparata, F. P., & Shamos, M. I. (1985).
           Computational Geometry: An Introduction. Springer-Verlag.
    """
    contadores.franja += 1

    distancia_minima = delta
    punto_mas_cercano1, punto_mas_cercano2 = mejor_par[0], mejor_par[1]
    numero_puntos_franja = len(franja)

    for i in range(numero_puntos_franja):
        j = i + 1
        while j < numero_puntos_franja and \
                (franja[j][1] - franja[i][1]) < distancia_minima:
            distancia = calcular_distancia(franja[i], franja[j])
            if distancia < distancia_minima:
                distancia_minima = distancia
                punto_mas_cercano1 = franja[i]
                punto_mas_cercano2 = franja[j]
            j += 1

    return punto_mas_cercano1, punto_mas_cercano2, distancia_minima


def par_mas_cercano_recursivo(puntos_ordenados_x, puntos_ordenados_y):
    """
    Implementa el algoritmo recursivo de divide y conquista.

    Divide el conjunto de puntos en dos mitades, encuentra el par más
    cercano en cada mitad recursivamente, y luego busca pares que
    crucen la línea divisoria.

    Parameters
    ----------
    puntos_ordenados_x : list of tuple
        Lista de puntos ordenados por coordenada x.
    puntos_ordenados_y : list of tuple
        Lista de puntos ordenados por coordenada y.

    Returns
    -------
    tuple
        Tupla con tres elementos: (punto1, punto2, distancia_minima)
        donde punto1 y punto2 forman el par más cercano.

    Notes
    -----
    Complejidad temporal: O(n log n)
    La función mantiene dos listas ordenadas (por x e y) para
    evitar reordenamientos costosos en cada nivel de recursión.

    La recursión se detiene cuando hay 3 o menos puntos,
    usando fuerza bruta en ese caso.

    Esta función incrementa el contador de llamadas
    recursivas para análisis de rendimiento.

    Examples
    --------
    >>> puntos_x = [(1, 2), (3, 4), (5, 6)]
    >>> puntos_y = [(1, 2), (3, 4), (5, 6)]
    >>> p1, p2, dist = par_mas_cercano_recursivo(puntos_x, puntos_y)

    References
    ----------
    .. [1] Cormen, T. H., et al. (2009). Introduction to Algorithms.
           MIT Press. Chapter 33.4.
    """
    contadores.llamadas += 1

    numero_puntos = len(puntos_ordenados_x)

    # Caso base: usar fuerza bruta para conjuntos pequeños
    if numero_puntos <= 3:
        return fuerza_bruta_par_cercano(puntos_ordenados_x)

    # Dividir el conjunto en dos mitades
    mitad = numero_puntos // 2
    punto_medio = puntos_ordenados_x[mitad]

    # Dividir puntos ordenados por y en mitades izquierda y derecha
    puntos_izq_y = [p for p in puntos_ordenados_y if p[0] <= punto_medio[0]]
    puntos_der_y = [p for p in puntos_ordenados_y if p[0] > punto_medio[0]]

    # Resolver recursivamente para ambas mitades
    izq_p1, izq_p2, dist_izq = par_mas_cercano_recursivo(
        puntos_ordenados_x[:mitad], puntos_izq_y)
    der_p1, der_p2, dist_der = par_mas_cercano_recursivo(
        puntos_ordenados_x[mitad:], puntos_der_y)

    # Encontrar el mínimo de las dos mitades
    if dist_izq < dist_der:
        delta = dist_izq
        mejor_par = (izq_p1, izq_p2, dist_izq)
    else:
        delta = dist_der
        mejor_par = (der_p1, der_p2, dist_der)

    # Construir franja de puntos cercanos a la línea divisoria
    franja = [p for p in puntos_ordenados_y
              if abs(p[0] - punto_medio[0]) < delta]

    # Encontrar el par más cercano en la franja
    franja_p1, franja_p2, dist_franja = par_cercano_en_franja(
        franja, delta, mejor_par)

    # Retornar el mejor par encontrado
    if dist_franja < delta:
        return franja_p1, franja_p2, dist_franja
    return mejor_par[0], mejor_par[1], mejor_par[2]


def encontrar_par_mas_cercano(puntos):
    """
    Encuentra el par de puntos más cercano usando divide y conquista.

    Esta es la función principal que coordina el algoritmo completo.
    Prepara los datos ordenándolos y luego llama a la función recursiva.
    Además, reinicia todos los contadores de funciones.

    Parameters
    ----------
    puntos : list of tuple
        Lista de puntos como tuplas (x, y).

    Returns
    -------
    tuple
        Tupla con tres elementos: (punto1, punto2, distancia_minima)
        donde punto1 y punto2 son los puntos más cercanos.

    Raises
    ------
    ValueError
        Si la lista de puntos tiene menos de 2 elementos.

    Notes
    -----
    Complejidad temporal total: O(n log n)
    La ordenación inicial toma O(n log n) y el algoritmo
    recursivo también es O(n log n).

    Todos los contadores de funciones se reinician
    antes de cada ejecución del algoritmo.

    Examples
    --------
    >>> puntos = [(0, 0), (1, 1), (2, 2), (10, 10)]
    >>> p1, p2, dist = encontrar_par_mas_cercano(puntos)
    >>> print(f"Distancia mínima: {dist:.4f}")
    Distancia mínima: 1.4142

    References
    ----------
    .. [1] Shamos, M. I., & Hoey, D. (1975). Closest-point problems.
           Proceedings of the 16th Annual Symposium on Foundations
           of Computer Science.
    """
    # Reiniciar todos los contadores
    contadores.reiniciar()

    if len(puntos) < 2:
        raise ValueError("Se necesitan al menos 2 puntos")

    # Ordenar puntos por coordenada x y por coordenada y
    puntos_ordenados_x = sorted(puntos, key=lambda p: p[0])
    puntos_ordenados_y = sorted(puntos, key=lambda p: p[1])

    # Llamar a la función recursiva
    return par_mas_cercano_recursivo(puntos_ordenados_x, puntos_ordenados_y)


def mostrar_menu():
    """
    Muestra el menú de opciones para cargar archivos.

    Presenta al usuario las opciones disponibles de archivos
    de prueba o la posibilidad de ingresar un nombre personalizado.

    Notes
    -----
    Esta función facilita la selección de archivos de prueba
    de diferentes tamaños (100, 1000, 10000 puntos).

    Examples
    --------
    >>> mostrar_menu()
    === SELECCIÓN DE ARCHIVO ===
    1. datos_100.txt (100 puntos)
    2. datos_1000.txt (1000 puntos)
    3. datos_10000.txt (10000 puntos)
    4. Ingresar nombre de archivo manualmente
    0. Salir

    References
    ----------
    .. [1] Python Software Foundation. (2024). Input and Output.
           https://docs.python.org/3/tutorial/inputoutput.html
    """
    print("\n" + "=" * 60)
    print("SELECCIÓN DE ARCHIVO")
    print("=" * 60)
    print("1. datos_100.txt (100 puntos)")
    print("2. datos_1000.txt (1000 puntos)")
    print("3. datos_10000.txt (10000 puntos)")
    print("4. Ingresar nombre de archivo manualmente")
    print("0. Salir")
    print("=" * 60)


def obtener_nombre_archivo():
    """
    Obtiene el nombre del archivo a procesar según la elección del usuario.

    Muestra un menú interactivo y retorna el nombre del archivo
    seleccionado por el usuario.

    Returns
    -------
    str or None
        Nombre del archivo seleccionado, o None si el usuario decide salir.

    Notes
    -----
    La función valida la opción ingresada y permite al usuario
    elegir entre archivos predefinidos o ingresar uno personalizado.

    Examples
    --------
    >>> nombre = obtener_nombre_archivo()
    Seleccione una opción: 1
    >>> print(nombre)
    datos_100.txt

    References
    ----------
    .. [1] Python Software Foundation. (2024). Built-in Functions.
           https://docs.python.org/3/library/functions.html
    """
    archivos_predefinidos = {
        '1': 'datos_100.txt',
        '2': 'datos_1000.txt',
        '3': 'datos_10000.txt'
    }

    mostrar_menu()

    while True:
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == '0':
            return None

        if opcion in archivos_predefinidos:
            return archivos_predefinidos[opcion]

        if opcion == '4':
            nombre = input("Ingrese el nombre del archivo: ").strip()
            if nombre:
                return nombre
            print("Error: Debe ingresar un nombre de archivo válido.")
        else:
            print("Error: Opción no válida. Intente nuevamente.")


def imprimir_resultados(nombre_archivo, puntos, resultado, tiempo_ejecucion):
    """
    Imprime los resultados del algoritmo de forma estructurada.

    Parameters
    ----------
    nombre_archivo : str
        Nombre del archivo procesado.
    puntos : list
        Lista de puntos analizados.
    resultado : tuple
        Tupla (punto1, punto2, distancia) con el resultado.
    tiempo_ejecucion : float
        Tiempo de ejecución del algoritmo en segundos.

    Notes
    -----
    Esta función centraliza la impresión de resultados para
    mantener el código más limpio y cumplir con las restricciones
    de complejidad de Pylint.

    Examples
    --------
    >>> resultado = ((1,2), (3,4), 2.82)
    >>> imprimir_resultados("datos.txt", puntos, resultado, 0.001)
    """
    punto1, punto2, distancia = resultado

    print("\n" + "=" * 70)
    print(f"RESULTADOS PARA: {nombre_archivo}")
    print("=" * 70)
    print(f"\nCantidad de puntos analizados: {len(puntos)}")

    print("\nEstadisticas de llamadas a funciones:")
    print(f"   - par_mas_cercano_recursivo(): {contadores.llamadas} veces")
    print(f"   - calcular_distancia(): {contadores.distancia} veces")
    print(f"   - fuerza_bruta_par_cercano(): {contadores.fuerza_bruta} veces")
    print(f"   - par_cercano_en_franja(): {contadores.franja} veces")

    funciones = {
        'calcular_distancia()': contadores.distancia,
        'par_mas_cercano_recursivo()': contadores.llamadas,
        'par_cercano_en_franja()': contadores.franja,
        'fuerza_bruta_par_cercano()': contadores.fuerza_bruta
    }
    funcion_mas_invocada = max(funciones, key=funciones.get)
    max_invocaciones = funciones[funcion_mas_invocada]

    print(f"\nFuncion mas invocada: {funcion_mas_invocada}")
    print(f"   Con {max_invocaciones} llamadas")
    print("\nPar de puntos encontrado:")
    print(f"   Punto 1: ({punto1[0]}, {punto1[1]})")
    print(f"   Punto 2: ({punto2[0]}, {punto2[1]})")
    print(f"\nDistancia euclidiana entre los puntos: {distancia:.6f}")
    print(f"\nTiempo de ejecucion del algoritmo: {tiempo_ejecucion:.6f} segundos")
    print(f"   ({tiempo_ejecucion * 1000:.4f} milisegundos)")
    print("=" * 70)


def main():
    """
    Función principal del programa.

    Lee puntos desde un archivo, encuentra el par más cercano
    y muestra los resultados en la consola. Permite seleccionar
    entre múltiples archivos de prueba.

    Notes
    -----
    El programa presenta un menú interactivo para seleccionar
    archivos de prueba con diferentes tamaños (100, 1000, 10000 puntos)
    o ingresar un archivo personalizado. Mide el tiempo de ejecución
    del algoritmo divide y conquista.

    Examples
    --------
    Ejecución típica del programa:
    $ python closest_pair.py

    === SELECCIÓN DE ARCHIVO ===
    1. datos_100.txt (100 puntos)
    2. datos_1000.txt (1000 puntos)
    ...

    === RESULTADOS ===
    Punto 1: (100.0, 30.0)
    Punto 2: (100.0, 21.0)
    Distancia euclidiana: 9.000000
    Tiempo de ejecución: 0.002345 segundos

    References
    ----------
    .. [1] Python Software Foundation. (2024). The Python Standard Library.
           https://docs.python.org/3/library/
    """
    print("=" * 60)
    print("PAR DE PUNTOS MÁS CERCANO - DIVIDE Y CONQUISTA")
    print("=" * 60)
    print("\nEste programa encuentra el par de puntos más cercano")
    print("utilizando la estrategia de divide y conquista.")

    while True:
        nombre_archivo = obtener_nombre_archivo()

        if nombre_archivo is None:
            print("\nHasta luego!")
            break

        try:
            print(f"\nCargando archivo: {nombre_archivo}")

            puntos = leer_puntos_archivo(nombre_archivo)
            print(f"Se cargaron {len(puntos)} puntos correctamente.")

            print("\nEjecutando algoritmo divide y conquista...")
            tiempo_inicio = time.time()
            resultado = encontrar_par_mas_cercano(puntos)
            tiempo_fin = time.time()
            tiempo_ejecucion = tiempo_fin - tiempo_inicio

            imprimir_resultados(nombre_archivo, puntos, resultado,
                                tiempo_ejecucion)

            continuar = input("\nDesea procesar otro archivo? (s/n): ")
            if continuar.lower() != 's':
                print("\nHasta luego!")
                break

        except FileNotFoundError:
            print(f"\nError: No se encontró el archivo '{nombre_archivo}'")
            print("Verifique que el archivo existe en el directorio actual.")

        except ValueError as error:
            print(f"\nError al procesar el archivo: {error}")
            print("Verifique que el formato del archivo sea correcto.")

        except (IOError, OSError) as error:
            print(f"\nError de entrada/salida: {error}")
            print("El programa no pudo ejecutarse correctamente.")


if __name__ == "__main__":
    main()