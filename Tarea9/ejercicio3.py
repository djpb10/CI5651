import networkx as nx

def min_cover_aproximado(grafo):
    """
    Algoritmo de aproximación con factor 2 para el problema MIN-COVER.
    Encuentra un cubrimiento de vértices cuyo tamaño es a lo sumo el doble del óptimo.

    Argumentos:
        grafo: Un objeto grafo no dirigido de la librería networkx.

    Retorna:
        Un conjunto (set) de vértices que forman el cubrimiento aproximado.
    """
    # Inicializar el conjunto de vértices de la solución
    v_aprox = set()

    # Inicializar el conjunto de aristas no cubiertas.
    #    Hacemos una copia de las aristas originales para poder iterar y eliminar libremente.
    aristas_restantes = set(grafo.edges())

    # Bucle principal: mientras queden aristas sin cubrir
    while aristas_restantes:
        # Tomar una arista cualquiera del conjunto de restantes
        u, v = aristas_restantes.pop()

        # Añadir AMBOS extremos de la arista al cubrimiento
        v_aprox.add(u)
        v_aprox.add(v)

        # Buscar todas las otras aristas que ya han sido cubiertas por u o v
        # y eliminarlas de aristas_restantes.
        aristas_a_eliminar = set()
        for arista in aristas_restantes:
            if u in arista or v in arista:
                aristas_a_eliminar.add(arista)

        # Actualizar el conjunto de aristas restantes restando las que acabamos de cubrir
        aristas_restantes -= aristas_a_eliminar

    # Devolver la solución aproximada
    return v_aprox
