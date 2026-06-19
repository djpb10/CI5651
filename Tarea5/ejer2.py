def asignar_direcciones(lugares, calles):

    if not lugares:
        return []
        
    # 1. Construir lista de adyacencias
    adj = {u: [] for u in lugares}
    for u, v in calles:
        adj[u].append(v)
        adj[v].append(u)
        
    # Variables de estado para el DFS
    prenum = {}
    highest = {}
    timer = 0
    visitados = set()
    
    calles_orientadas = []
    puentes = []
    
    # 2. Función DFS anidada
    def dfs(u, padre):
        nonlocal timer
        timer += 1
        prenum[u] = highest[u] = timer
        visitados.add(u)
        
        for v in adj[u]:
            # Evitar regresar inmediatamente por la calle de la que vinimos
            if v == padre:
                continue
                
            if v not in visitados:
                # Conexión de árbol: Orientamos hacia adelante (u -> v)
                calles_orientadas.append((u, v))
                
                # Llamada recursiva
                dfs(v, u)
                
                # Actualizar el valor de retroceso (highest)
                highest[u] = min(highest[u], highest[v])
                
                if highest[v] > prenum[u]:
                    puentes.append((u, v))
                    
            elif prenum[v] < prenum[u]:
                # Conexión de retroceso: Orientamos de vuelta al ancestro (u -> v)
                # Solo procesamos cuando prenum[v] < prenum[u] para no 
                # duplicar la asignación de la arista cuando la vemos desde el otro lado.
                calles_orientadas.append((u, v))
                
                # Actualizamos el valor de retroceso (highest) usando prenum[v]
                highest[u] = min(highest[u], prenum[v])

    # 3. Iniciar el DFS desde cualquier lugar (tomamos uno al azar)
    nodo_inicial = next(iter(lugares))
    dfs(nodo_inicial, None)
    
    # 4. Verificaciones de Imposibilidad
    # Si no se visitaron todos los lugares, la ciudad estaba desconectada originalmente
    if len(visitados) < len(lugares):
        return None
        
    # Si encontramos al menos un puente, es imposible garantizar conexión fuerte
    if puentes:
        return None
        
    # Si pasa las pruebas, el plan es válido
    return calles_orientadas
