import math

def max_puntos_en_circulo(puntos, R):
    n = len(puntos)
    if n == 0:
        return None, 0
    if n == 1:
        return puntos[0], 1

    max_puntos = 1
    mejor_centro = puntos[0]

    for i in range(n):
        pi = puntos[i]
        eventos = []

        for j in range(n):
            if i == j:
                continue
            
            pj = puntos[j]
            dx = pj[0] - pi[0]
            dy = pj[1] - pi[1]
            dist_cuadrada = dx**2 + dy**2
            dist = math.sqrt(dist_cuadrada)

            # Si la distancia es mayor a 2R, no hay intersección
            if dist > 2 * R or dist == 0:
                continue

            # Ángulo del centro de pj respecto a pi
            theta = math.atan2(dy, dx)
            
            # Mitad del ángulo del arco de intersección
            alpha = math.acos(dist / (2 * R))

            # Calcular ángulos de entrada y salida
            # Normalizamos al rango [-pi, pi]
            entrada = theta - alpha
            salida = theta + alpha

            # Manejar el cruce de la discontinuidad en -pi / pi

            # Aseguramos que la entrada esté entre -pi y pi
            if entrada <= -math.pi:
                entrada += 2 * math.pi
                salida += 2 * math.pi
            
            # Si el arco cruza +pi, lo dividimos en dos eventos
            if salida > math.pi:
                eventos.append((entrada, 1))
                eventos.append((math.pi, -1))
                eventos.append((-math.pi, 1))
                eventos.append((salida - 2 * math.pi, -1))
            else:
                eventos.append((entrada, 1))
                eventos.append((salida, -1))

        # Ordenar eventos: primero por ángulo, luego salidas (-1) antes que entradas (1) 
        # en caso de empate para no contar un punto al salir justo cuando entra otro.
        # Para maximizar, priorizamos las entradas.
        eventos.sort(key=lambda e: (e[0], -e[1]))

        conteo_actual = 1 # El círculo siempre cubre al menos al punto pi
        
        for angulo, tipo in eventos:
            conteo_actual += tipo
            
            if conteo_actual > max_puntos:
                max_puntos = conteo_actual
                # Calcular las coordenadas del centro
                cx = pi[0] + R * math.cos(angulo)
                cy = pi[1] + R * math.sin(angulo)
                mejor_centro = (cx, cy)

    return mejor_centro, max_puntos