import math

def producto_cruz(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

def distancia_cuadrada(p1, p2):
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

def graham_scan(puntos):
    n = len(puntos)
    if n <= 3:
        return puntos

    # Asegurar uso de tuplas para evitar errores con set()
    puntos = [tuple(p) for p in puntos]
    p0 = min(puntos, key=lambda p: (p[1], p[0]))

    def orden(p):
        if p == p0:
            return (-math.pi, 0)
        angulo = math.atan2(p[1] - p0[1], p[0] - p0[0])
        dist = distancia_cuadrada(p0, p)
        return (angulo, dist)
    
    puntos_ordenados = sorted(puntos, key=orden)

    # Invertir el orden de los puntos colineales con el ángulo máximo
    # para evitar que el barrido genere giros a la derecha al retornar a p0
    max_angulo = orden(puntos_ordenados[-1])[0]
    i = n - 1
    while i >= 0 and orden(puntos_ordenados[i])[0] == max_angulo:
        i -= 1
    puntos_ordenados[i + 1:] = reversed(puntos_ordenados[i + 1:])

    pila = [puntos_ordenados[0], puntos_ordenados[1]]
    
    for i in range(2, n):
        pi = puntos_ordenados[i]
        # Permitir colineales (solo descarta si el giro es estrictamente a la derecha < 0)
        while len(pila) >= 2 and producto_cruz(pila[-2], pila[-1], pi) < 0:
            pila.pop()
        pila.append(pi)
        
    return pila

def contar_capas(puntos):
    # Convertir a lista de tuplas
    puntos_actuales = [tuple(p) for p in puntos]
    num_capas = 0
    
    while puntos_actuales:
        if len(puntos_actuales) <= 3:
            num_capas += 1
            break
            
        capa = graham_scan(puntos_actuales)
        num_capas += 1
        
        set_capa = set(capa)
        puntos_actuales = [p for p in puntos_actuales if p not in set_capa]
        
    return num_capas