import random

class TreapNode:
    """Nodo del Treap Implícito que representa un evento de entrada o salida."""
    def __init__(self, node_id, weight):
        self.node_id = node_id
        self.w = weight          # +1 para entrada, -1 para salida
        self.sum_w = weight
        self.priority = random.random()
        self.sz = 1
        self.left = self.right = self.parent = None


def update(t):
    """Recalcula el tamaño y la suma acumulada de pesos de un nodo de forma compacta."""
    if t:
        t.sz = 1 + (t.left.sz if t.left else 0) + (t.right.sz if t.right else 0)
        t.sum_w = t.w + (t.left.sum_w if t.left else 0) + (t.right.sum_w if t.right else 0)
        if t.left: t.left.parent = t
        if t.right: t.right.parent = t


def split(t, k):
    """Divide el Treap t en l (primeros k elementos) y r (restantes)."""
    if not t: return None, None
    left_sz = 1 + (t.left.sz if t.left else 0)
    if left_sz <= k:
        l, r = split(t.right, k - left_sz)
        t.right = l
        update(t)
        if r: r.parent = None
        return t, r
    else:
        l, r = split(t.left, k)
        t.left = r
        update(t)
        if l: l.parent = None
        return l, t


def merge(l, r):
    """Fusiona los Treaps l y r preservando el orden relativo de los elementos."""
    if not l or not r: return l or r
    if l.priority > r.priority:
        l.right = merge(l.right, r)
        update(l)
        return l
    else:
        r.left = merge(l, r.left)
        update(r)
        return r


def climb(node, get_index=True):
    """
    Función unificada que asciende desde un nodo hasta la raíz para calcular:
    - El índice implícito (si get_index es True).
    - La suma acumulada de pesos de prefijo (si get_index es False).
    """
    ans = (node.left.sz if node.left else 0) if get_index else (node.left.sum_w if node.left else 0)
    curr = node
    while curr.parent:
        p = curr.parent
        if p.right == curr:
            ans += (1 + (p.left.sz if p.left else 0)) if get_index else (p.w + (p.left.sum_w if p.left else 0))
        curr = p
    return ans


class DynamicTreeManager:
    """Manejador del árbol dinámico mediante recorrido de Euler y Treap Implícito."""
    def __init__(self, adj, root):
        self.nodes = {}  # Mapea nodo -> (in_node, out_node)
        seq = []
        
        # 1. DFS para aplanar el árbol en una secuencia lineal
        def dfs(u):
            in_node, out_node = TreapNode(u, 1), TreapNode(u, -1)
            self.nodes[u] = (in_node, out_node)
            seq.append(in_node)
            for v in adj.get(u, []): dfs(v)
            seq.append(out_node)
        dfs(root)
        
        # 2. Construcción recursiva del Treap balanceado en tiempo lineal O(N)
        def build(l, r):
            if l > r: return None
            mid = (l + r) // 2
            curr = seq[mid]
            curr.left, curr.right = build(l, mid - 1), build(mid + 1, r)
            update(curr)
            return curr
            
        self.root = build(0, len(seq) - 1)

    def profundidad(self, x):
        """Retorna la profundidad del nodo x en el árbol actual en O(log N)."""
        return climb(self.nodes[x][0], get_index=False)

    def intercambiar(self, x, y):
        """Intercambia físicamente los subárboles de x e y en O(log N)."""
        in_x, out_x = self.nodes[x]
        in_y, out_y = self.nodes[y]
        
        L_x, R_x = climb(in_x), climb(out_x)
        L_y, R_y = climb(in_y), climb(out_y)
        
        if L_x > L_y:
            L_x, R_x, L_y, R_y = L_y, R_y, L_x, R_x
            
        # Escalamos para encontrar la raíz actual del Treap antes de hacer split
        curr_root = in_x
        while curr_root.parent: curr_root = curr_root.parent
        
        # Partición en 5 porciones consecutivas
        p1234, p5 = split(curr_root, R_y + 1)
        p123, p4 = split(p1234, L_y)
        p12, p3 = split(p123, R_x + 1)
        p1, p2 = split(p12, L_x)
        
        # Re-ensamblaje fluido alternando los bloques
        self.root = merge(merge(merge(merge(p1, p4), p3), p2), p5)


