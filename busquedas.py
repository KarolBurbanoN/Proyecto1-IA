import heapq

def heuristica(pos, meta):
    """Distancia Manhattan entre dos puntos."""
    return abs(pos[0] - meta[0]) + abs(pos[1] - meta[1])

def vecinos(pos, matriz):
    """Devuelve las posiciones vecinas válidas (sin salir de la matriz ni pasar por veneno)."""
    filas, columnas = len(matriz), len(matriz[0])
    x, y = pos
    posibles = [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]  # arriba, abajo, izq, der
    validos = []
    for nx, ny in posibles:
        if 0 <= nx < filas and 0 <= ny < columnas and matriz[nx][ny] != "V":
            validos.append((nx, ny))
    return validos

def reconstruir_camino(padres, actual):
    """Reconstruye el camino desde la meta hasta el inicio."""
    camino = [actual]
    while actual in padres:
        actual = padres[actual]
        camino.append(actual)
    return list(reversed(camino))

def beam_search(matriz, inicio, meta, beta=3):
    """
    Implementa la búsqueda Beam Search.
    - matriz: entorno del problema
    - inicio: posición de la hormiga
    - meta: posición del hongo
    - beta: ancho del haz (beam width)
    """
    # [f, posición]
    # 'f' es el costo estimado total: f = g + h
    # Cola de prioridad con tuplas (heurística, posición)
    frontera = [(heuristica(inicio, meta), inicio)]
    padres = {}
    g_costos = {inicio: 0}#Almacena el costo real (g) desde el inicio
    visitados = set()

    while frontera:
        # Seleccionar los beta nodos más prometedores
        frontera = sorted(frontera, key=lambda x: x[0])[:beta]
        nuevos = []

        for _, actual in frontera:
            if actual == meta:
                return reconstruir_camino(padres, actual)

            visitados.add(actual)

            for vecino in vecinos(actual, matriz):
                nuevo_g = g_costos[actual] + 1 # cada movimiento cuesta 1

                # Usamos la lógica de A*: si es un camino mejor, actualizamos
                if vecino not in g_costos or nuevo_g < g_costos[vecino]:
                    
                    g_costos[vecino] = nuevo_g
                    
                    h = heuristica(vecino, meta)
                    f = nuevo_g + h  # Usamos f = g + h para la evaluación
                    padres[vecino] = actual
                    # Usamos heapq para mantener ordenados los nodos de la nueva frontera
                    heapq.heappush(nuevos, (f, vecino))
        
        
        frontera = sorted(nuevos, key=lambda x: x[0])[:beta]

    return None  # No se encontró camino

def dynamic_weighted_a_star(matriz, inicio, meta, epsilon=1.0):
    """
    Dynamic Weighted A*:
    - matriz: entorno del problema
    - inicio: posición inicial (hormiga)
    - meta: posición objetivo (hongo)
    - epsilon: factor de ajuste dinámico
    """
    filas, columnas = len(matriz), len(matriz[0])
    N = filas * columnas  # profundidad máxima aproximada

    frontera = []
    heapq.heappush(frontera, (0, inicio, 0))  # (f, posición, profundidad)
    padres = {}
    g_costos = {inicio: 0}

    while frontera:
        f_actual, actual, profundidad = heapq.heappop(frontera)

        if actual == meta:
            return reconstruir_camino(padres, actual)

        for vecino in vecinos(actual, matriz):
            nuevo_g = g_costos[actual] + 1
            if vecino not in g_costos or nuevo_g < g_costos[vecino]:
                g_costos[vecino] = nuevo_g
                d = profundidad + 1
                h = heuristica(vecino, meta)
                peso = 1 + epsilon * (1 - d / N)
                f = nuevo_g + peso * h
                padres[vecino] = actual
                heapq.heappush(frontera, (f, vecino, d))

    return None  # no se encontró camino