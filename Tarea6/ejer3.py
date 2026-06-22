class Node:
    """
    Representa un nodo en el Árbol de Segmentos Persistente.
    'count' almacena cuántos números en el rango de este nodo han sido insertados.
    'L' y 'R' son punteros a los hijos izquierdo y derecho de esta versión.
    """
    def __init__(self):
        self.count = 0
        self.L = None
        self.R = None


def build(l, r):
    """Construye el árbol de segmentos inicial (versión 0) lleno de ceros."""
    node = Node()
    if l < r:
        mid = (l + r) // 2
        node.L = build(l, mid)
        node.R = build(mid + 1, r)
    return node


def update(prev_node, l, r, val):
    """
    Crea una nueva versión del camino del árbol insertando 'val'.
    Reutiliza las ramas que no cambian apuntando a 'prev_node'.
    Retorna la raíz de la nueva versión.
    """
    new_node = Node()
    if l == r:
        new_node.count = prev_node.count + 1
        return new_node
        
    mid = (l + r) // 2
    if val <= mid:
        new_node.L = update(prev_node.L, l, mid, val)
        new_node.R = prev_node.R  # Reutilizamos el subárbol derecho intacto
    else:
        new_node.L = prev_node.L  # Reutilizamos el subárbol izquierdo intacto
        new_node.R = update(prev_node.R, mid + 1, r, val)
        
    new_node.count = new_node.L.count + new_node.R.count
    return new_node


def query(node_i, node_j, l, r, k):
    """
    Encuentra el k-ésimo elemento en el subarreglo usando la resta de prefijos
    entre la versión j (prefijo A[1..j]) y la versión i-1 (prefijo A[1..i-1]).
    """
    if l == r:
        return l
        
    mid = (l + r) // 2
    # Elementos en el rango A[i..j] que caen en el subárbol izquierdo (valores <= mid)
    count_left = node_j.L.count - node_i.L.count
    
    if k <= count_left:
        return query(node_i.L, node_j.L, l, mid, k)
    else:
        return query(node_i.R, node_j.R, mid + 1, r, k - count_left)


class PersistentSegmentTreeManager:
    """Clase interfaz que maneja el arreglo y las consultas del problema."""
    def __init__(self, arr):
        self.arr = arr
        self.n = len(arr)
        
        # Como es una permutación de 1 a N, el rango de valores es [1, N]
        self.min_val = 1
        self.max_val = self.n
        
        # Historial de raíces de cada versión (roots[t] almacena el prefijo A[1..t])
        self.roots = [None] * (self.n + 1)
        self.roots[0] = build(self.min_val, self.max_val)
        
        for t in range(1, self.n + 1):
            val_to_insert = self.arr[t - 1]
            self.roots[t] = update(self.roots[t - 1], self.min_val, self.max_val, val_to_insert)

    def seleccion(self, i, j, k):
        """
        Responde la consulta seleccion(i, j, k) basada en índices 1-indexed.
        Retorna el k-ésimo menor elemento en el rango A[i..j].
        """
        # La versión de prefijo izquierda para A[i..j] es i - 1
        return query(self.roots[i - 1], self.roots[j], self.min_val, self.max_val, k)
