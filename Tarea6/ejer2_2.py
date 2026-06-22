class SegmentTree:
    """
    Árbol de Segmentos optimizado con intervalos semiabiertos [l, r).
    Almacena estados forward y backward para paréntesis direccionales.
    Soporta Lazy Propagation para inversiones de rango en O(log N).
    """
    def __init__(self, size, initial_chars):
        self.size = size
        self.tree_fw = [(0, 0)] * (4 * size)
        self.tree_bw = [(0, 0)] * (4 * size)
        self.lazy = [False] * (4 * size)
        self.initial_chars = initial_chars
        self._build(1, 0, size - 1)

    def _merge(self, left, right):
        """Fusiona el estado izquierdo con el derecho de forma asociativa."""
        open_l, close_l = left
        open_r, close_r = right
        matched = min(open_l, close_r)
        return (open_l + open_r - matched, close_l + close_r - matched)

    def _build(self, node, start, end):
        if start == end:
            char = self.initial_chars[start]
            state = (1, 0) if char == '(' else (0, 1)
            self.tree_fw[node] = self.tree_bw[node] = state
            return
        mid = (start + end) // 2
        self._build(2 * node, start, mid)
        self._build(2 * node + 1, mid + 1, end)
        self._pull(node)

    def _pull(self, node):
        self.tree_fw[node] = self._merge(self.tree_fw[2 * node], self.tree_fw[2 * node + 1])
        self.tree_bw[node] = self._merge(self.tree_bw[2 * node + 1], self.tree_bw[2 * node])

    def _apply_lazy(self, node):
        of, cf = self.tree_fw[node]
        self.tree_fw[node] = (cf, of)
        ob, cb = self.tree_bw[node]
        self.tree_bw[node] = (cb, ob)
        self.lazy[node] = not self.lazy[node]

    def _push(self, node):
        if self.lazy[node]:
            self._apply_lazy(2 * node)
            self._apply_lazy(2 * node + 1)
            self.lazy[node] = False

    def update_range(self, node, start, end, l, r):
        """Invierte los paréntesis en el rango semiabierto [l, r) en O(log N)."""
        if l <= start and end < r:
            self._apply_lazy(node)
            return
        self._push(node)
        mid = (start + end) // 2
        if l <= mid:
            self.update_range(2 * node, start, mid, l, r)
        if r > mid + 1:
            self.update_range(2 * node + 1, mid + 1, end, l, r)
        self._pull(node)

    def query_range(self, node, start, end, l, r):
        """Retorna (estado_fw, estado_bw) del segmento [l, r) en O(log N)."""
        if l <= start and end < r:
            return self.tree_fw[node], self.tree_bw[node]
        self._push(node)
        mid = (start + end) // 2
        if r <= mid + 1:
            return self.query_range(2 * node, start, mid, l, r)
        elif l > mid:
            return self.query_range(2 * node + 1, mid + 1, end, l, r)
        else:
            left_fw, left_bw = self.query_range(2 * node, start, mid, l, r)
            right_fw, right_bw = self.query_range(2 * node + 1, mid + 1, end, l, r)
            return self._merge(left_fw, right_fw), self._merge(right_bw, left_bw)


class HeavyLightDecomposition:
    """
    HLD compacta y simplificada basada en intervalos semiabiertos.
    Mapea el árbol a un arreglo secuencial para consultas de caminos en O(log^2 N).
    """
    def __init__(self, adj, edges_par, root=0):
        self.adj = adj
        self.size = len(adj)
        self.parent = [0] * self.size
        self.depth = [0] * self.size
        self.heavy = [-1] * self.size
        self.head = [0] * self.size
        self.pos = [0] * self.size
        self.curr_pos = 0

        # 1. DFS para calcular tamaños, profundidades e hijos pesados
        def dfs(u, p, d):
            self.parent[u] = p
            self.depth[u] = d
            size, max_size = 1, 0
            for v in adj[u]:
                if v != p:
                    child_size = dfs(v, u, d + 1)
                    size += child_size
                    if child_size > max_size:
                        max_size = child_size
                        self.heavy[u] = v
            return size

        dfs(root, -1, 0)

        # 2. Descomposición recursiva simplificada en cadenas pesadas
        initial_chars = [''] * self.size
        def decompose(u, h):
            self.head[u] = h
            self.pos[u] = self.curr_pos
            self.curr_pos += 1
            if u != root:
                p = self.parent[u]
                edge = (min(u, p), max(u, p))
                initial_chars[self.pos[u]] = edges_par[edge]
            
            if self.heavy[u] != -1:
                decompose(self.heavy[u], h)
            for v in adj[u]:
                if v != self.parent[u] and v != self.heavy[u]:
                    decompose(v, v)

        decompose(root, root)
        self.segtree = SegmentTree(self.size, initial_chars)

    def inv(self, x, y):
        """Invierte el tipo de paréntesis en el camino x - y en O(log^2 N)."""
        while self.head[x] != self.head[y]:
            if self.depth[self.head[x]] > self.depth[self.head[y]]:
                x, y = y, x
            self.segtree.update_range(1, 0, self.size - 1, self.pos[self.head[y]], self.pos[y] + 1)
            y = self.parent[self.head[y]]
        if self.depth[x] > self.depth[y]:
            x, y = y, x
        if x != y:
            self.segtree.update_range(1, 0, self.size - 1, self.pos[x] + 1, self.pos[y] + 1)

    def bp(self, x, y):
        """Consulta si el camino x - y está bien parentizado en O(log^2 N)."""
        up_segments = []
        down_segments = []
        while self.head[x] != self.head[y]:
            if self.depth[self.head[x]] > self.depth[self.head[y]]:
                fw, bw = self.segtree.query_range(1, 0, self.size - 1, self.pos[self.head[x]], self.pos[x] + 1)
                up_segments.append(bw)
                x = self.parent[self.head[x]]
            else:
                fw, bw = self.segtree.query_range(1, 0, self.size - 1, self.pos[self.head[y]], self.pos[y] + 1)
                down_segments.append(fw)
                y = self.parent[self.head[y]]

        if self.depth[x] > self.depth[y]:
            fw, bw = self.segtree.query_range(1, 0, self.size - 1, self.pos[y] + 1, self.pos[x] + 1)
            up_segments.append(bw)
        elif self.depth[x] < self.depth[y]:
            fw, bw = self.segtree.query_range(1, 0, self.size - 1, self.pos[x] + 1, self.pos[y] + 1)
            down_segments.append(fw)

        # Unificar la subida (up_segments) y la bajada invertida (down_segments)
        total_state = (0, 0)
        for state in up_segments:
            total_state = self.segtree._merge(total_state, state)
        for state in reversed(down_segments):
            total_state = self.segtree._merge(total_state, state)
            
        return total_state == (0, 0)
