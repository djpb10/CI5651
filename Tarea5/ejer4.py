from collections import deque

def es_primo(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def resolver_minima_eliminacion(C):
    # Convertimos a conjunto para realizar búsquedas y eliminaciones en O(1)
    conjunto = set(C)
    eliminados_iniciales = 0
    
    # FASE GREEDY: Si el número 1 está en el conjunto, obligatoriamente debemos
    # eliminarlo para romper el ciclo/bucle 1 + 1 = 2 (que es primo).
    if 1 in conjunto:
        conjunto.remove(1)
        eliminados_iniciales = 1
        
    # Clasificamos los elementos restantes en impares y pares.
    # Dado que todos los elementos son mayores o iguales a 2 y distintos,
    # ninguna suma de elementos con la misma paridad puede dar el primo 2.
    # Por lo tanto, el grafo es estrictamente bipartito.
    impares = [x for x in conjunto if x % 2 != 0]
    pares = [x for x in conjunto if x % 2 == 0]
    
    # 1. Construcción de la lista de adyacencia (Impares -> Pares)
    adj = {u: [] for u in impares}
    for u in impares:
        for v in pares:
            if es_primo(u + v):
                adj[u].append(v)
                
    # 2. Inicialización de estructuras para el algoritmo de Hopcroft-Karp
    match_impares = {u: None for u in impares}
    match_pares = {v: None for v in pares}
    dist = {}
    
    def bfs():
        """
        Fase BFS: Encuentra la longitud de los caminos aumentantes más cortos
        y divide el grafo en capas/niveles de distancia.
        """
        queue = deque()
        for u in impares:
            if match_impares[u] is None:
                dist[u] = 0
                queue.append(u)
            else:
                dist[u] = float('inf')
        
        # Nodo ficticio (None) para indicar el final de los caminos aumentantes
        dist[None] = float('inf')
        
        while queue:
            u = queue.popleft()
            if dist[u] < dist[None]:
                for v in adj[u]:
                    u_next = match_pares[v]
                    if dist[u_next] == float('inf'):
                        dist[u_next] = dist[u] + 1
                        if u_next is not None:
                            queue.append(u_next)
                            
        return dist[None] != float('inf')

    def dfs(u):
        """
        Fase DFS: Busca caminos aumentantes de forma recursiva respetando
        los niveles de distancia calculados en el BFS para actualizar el matching.
        """
        for v in adj[u]:
            u_next = match_pares[v]
            if u_next is None or (dist[u_next] == dist[u] + 1 and dfs(u_next)):
                match_pares[v] = u
                match_impares[u] = v
                return True
        dist[u] = float('inf')
        return False

    # 3. Ejecución del algoritmo de Hopcroft-Karp
    matching_maximo = 0
    while bfs():
        for u in impares:
            if match_impares[u] is None:
                if dfs(u):
                    matching_maximo += 1
                    
    # Por el Teorema de König, la Cobertura Mínima de Vértices (Vertex Cover)
    # equivale al Matching Máximo sobre el grafo bipartito resultante.
    return eliminados_iniciales + matching_maximo
