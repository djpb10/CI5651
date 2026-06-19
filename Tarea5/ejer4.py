from collections import deque

def es_primo(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

def resolver_minima_eliminacion(C):
    # Particionamos en impares y pares (Grafo Bipartito Perfecto)
    impares = [x for x in C if x % 2 != 0]
    pares = [x for x in C if x % 2 == 0]
    
    # 1. Construir la lista de adyacencia: impares -> pares
    adj = {u: [] for u in impares}
    for u in impares:
        for v in pares:
            if es_primo(u + v):
                adj[u].append(v)
                
    # 2. Inicialización de estructuras para Hopcroft-Karp
    match_impares = {u: None for u in impares}
    match_pares = {v: None for v in pares}
    dist = {}
    
    def bfs():
        queue = deque()
        for u in impares:
            if match_impares[u] is None:
                dist[u] = 0
                queue.append(u)
            else:
                dist[u] = float('inf')
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
        for v in adj[u]:
            u_next = match_pares[v]
            if u_next is None or (dist[u_next] == dist[u] + 1 and dfs(u_next)):
                match_pares[v] = u
                match_impares[u] = v
                return True
        dist[u] = float('inf')
        return False

    # 3. Bucle principal de Hopcroft-Karp: O(E * sqrt(V))
    matching_maximo = 0
    while bfs():
        for u in impares:
            if match_impares[u] is None:
                if dfs(u):
                    matching_maximo += 1
                    
    # Por el Teorema de König, el Vertex Cover mínimo es igual al Matching Máximo
    return matching_maximo