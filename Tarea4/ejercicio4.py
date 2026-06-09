def resolver_recoleccion_equipaje(n, maletas):
	"""
	Resuelve el problema de recoleccion de equipaje con costo d^2.
	
	Parametros:
	n (int): Cantidad de maletas (1 < n < 24)
	maletas (list of tuple): Lista de tuplas (x, y) con las posiciones de cada maleta.
	
	Retorna:
	int: El tiempo minimo necesario para recoger todas las maletas y volver al avion.
	"""
	# El avion esta en la posicion (0, 0)
	origen = (0, 0)

	# 1. Precomputar las distancias al cuadrado para optimizar el tiempo de ejecucion.


	dist_origen = [0] * n
	for i in range(n):
		mx, my = maletas[i]
		dist_origen[i] = mx**2 + my**2

	# dist_parejas[i][j] almacena d^2 entre la maleta i y la maleta j.
	dist_parejas = [[0] * n for _ in range(n)]
	for i in range(n):
		for j in range(i + 1, n):
			x1, y1 = maletas[i]
			x2, y2 = maletas[j]
			d2 = (x1 - x2)**2 + (y1 - y2)**2
			dist_parejas[i][j] = d2
			dist_parejas[j][i] = d2

	# 2. Inicializar la tabla DP para los 2^n estados.
	# Inicialmente, todos los estados tienen un costo "infinito" excepto el caso base DP[0] = 0.
	limite_estados = 1 << n
	dp = [float('inf')] * limite_estados
	dp[0] = 0

	# 3. Iterar sobre todos los estados (Bottom-Up)
	# Al procesar secuencialmente, aseguramos que los estados con menos bits encendidos

	# se calculen antes y sirvan para transicionar a estados con mas bits encendidos.
	for mask in range(limite_estados):
		if dp[mask] == float('inf'):
			continue

		# Buscar la primera maleta 'i' que aun no ha sido recogida (bit i es 0)
		i = -1
		for k in range(n):
			if not (mask & (1 << k)):
				i = k
				break
	
		# Si no encontramos ninguna maleta libre, significa que ya las recogimos todas en este estado.
		if i == -1:
			continue

		# Transicion Opcion 1: Recoger la maleta 'i' sola.
		# El nuevo estado tendra el bit 'i' encendido.
		siguiente_mask_sola = mask | (1 << i)
		costo_sola = dp[mask] + 2 * dist_origen[i]
		if costo_sola < dp[siguiente_mask_sola]:
			dp[siguiente_mask_sola] = costo_sola
		
		# Transicion Opcion 2: Recoger la maleta i emparejada con otra maleta j que tampoco este recogida.
		
		for j in range(i + 1, n):
			if not (mask & (1 << j)):
				siguiente_mask_pareja = mask | (1 << i) | (1 << j)
				costo_pareja = dp[mask] + dist_origen[i] + dist_parejas[i][j] + dist_origen[j]
				if costo_pareja < dp[siguiente_mask_pareja]:
					dp[siguiente_mask_pareja] = costo_pareja

	# El resultado final optimo estara en el estado donde todos los bits estan encendidos (todas recogidas).
	return dp[limite_estados - 1]
