from collections import deque
import sys

def min_lejania_particion(n, puntos):
    """
    Halla la suma mínima de lejanías para particionar un conjunto de puntos.
    Complejidad de Tiempo: O(n log n)
    Complejidad de Espacio: O(n)
    """
    if n == 0:
        return 0

    # Transformar todo al primer cuadrante
    # y evitar modificar la lista original.
    puntos_positivos = [(abs(x), abs(y)) for x, y in puntos]

    # Ordenar los puntos
    # Primero por X ascendente. En caso de empate, por Y ascendente.
    # Esto ayuda en el siguiente paso para descartar eficientemente.
    puntos_positivos.sort()

    # Filtrar puntos redundantes (los que están dentro del rectángulo de otro)
    # Recorremos de derecha a izquierda para mantener el Y máximo visto.
    # Si un punto tiene un Y <= max_y, significa que un punto más a la derecha (mayor X)
    # ya lo "domina" (cubre en ambas coordenadas), por lo que es redundante.
    puntos_utiles = []
    max_y = -1
    for i in range(n - 1, -1, -1):
        x, y = puntos_positivos[i]
        if y > max_y:
            puntos_utiles.append((x, y))
            max_y = y
    
    # Dado que insertamos de derecha a izquierda, revertimos para tener
    # el orden natural (X estrictamente creciente, Y estrictamente decreciente)
    puntos_utiles.reverse()
    k = len(puntos_utiles)

    # Si por algún motivo nos quedamos sin puntos
    if k == 0:
        return 0

    # Programación Dinámica con la optimizacion Convex Hull
    # dp[i] almacena el costo mínimo para los primeros i puntos (índices 1 a k).
    dp = [0] * (k + 1)
    
    # Cada elemento de la Deque será una tupla representando una línea: (pendiente, interseccion)
    # La ecuación es: cost = m * X + c
    # Donde para un estado j: m = y_{j+1} y c = dp[j]
    cola = deque()

    def interseccion_x(linea1, linea2):
        """
        Retorna la coordenada X donde se cruzan dos líneas.
        linea1: (m1, c1), linea2: (m2, c2)
        m1 * x + c1 = m2 * x + c2 => x = (c2 - c1) / (m1 - m2)
        """
        m1, c1 = linea1
        m2, c2 = linea2
        # Dado que las pendientes son estrictamente decrecientes, m1 != m2
        return (c2 - c1) / (m1 - m2)

    # Insertamos la línea base para j = 0
    # Pendiente = y_1, intersección = dp[0] = 0
    cola.append((puntos_utiles[0][1], 0))

    # Para cada i desde 1 hasta k, calculamos dp[i]
    for i in range(1, k + 1):
        xi = puntos_utiles[i - 1][0]
        
        # Evaluar: como los valores xi siempre son crecientes, la mejor línea
        # podría estar avanzando. Descartamos del frente de la cola las líneas
        # que ya han sido "superadas" por la siguiente línea para este valor de xi.
        while len(cola) >= 2:
            l1 = cola[0]
            l2 = cola[1]
            # Si evaluar l1 en xi >= evaluar l2 en xi, l1 ya no es óptima y la descartamos
            if l1[0] * xi + l1[1] >= l2[0] * xi + l2[1]:
                cola.popleft()
            else:
                break
        
        # El frente de la cola ahora tiene la línea que provee el mínimo para xi
        mejor_linea = cola[0]
        dp[i] = int(mejor_linea[0] * xi + mejor_linea[1])

        # Preparar la nueva línea para insertar
        # Si no hemos llegado al final, la próxima pendiente es y_{i+1}
        if i < k:
            nueva_m = puntos_utiles[i][1]
            nueva_c = dp[i]
            nueva_linea = (nueva_m, nueva_c)
            
            # Mantener la convexidad en el final de la cola
            while len(cola) >= 2:
                # l_ult es la última línea, l_penult es la penúltima
                l_ult = cola[-1]
                l_penult = cola[-2]
                
                # Si la intersección entre (nueva_linea y l_penult) ocurre antes
                # que la intersección entre (l_ult y l_penult), entonces l_ult
                # nunca formará parte de la frontera óptima inferior y es redundante.
                if interseccion_x(nueva_linea, l_penult) <= interseccion_x(l_ult, l_penult):
                    cola.pop()
                else:
                    break
            
            cola.append(nueva_linea)

    return dp[k]