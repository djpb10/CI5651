import sys
import random
from typing import List, Tuple

def min_costo_libros(N: int, M: int, D: List[int], P: List[List[int]]) -> int:
    """
    Calcula el costo mínimo total (distancia caminada + costo de comprar M libros)
    eligiendo un intervalo óptimo de puestos [A, B] (0 <= A <= B < N).
    
    :param N: Número de puestos de libros.
    :param M: Número de libros a comprar.
    :param D: Lista de N-1 distancias entre puestos consecutivos.
              D[i] es la distancia entre el puesto i e i+1.
    :param P: Matriz N x M donde P[i][j] es el precio del libro j en el puesto i.
    :return: El costo mínimo total.
    
    Complejidad de Tiempo: O(N * M * log N)
    Complejidad de Espacio Adicional: O(N + M)
    """
    if N <= 0 or M <= 0:
        return 0

    if N == 1:
        return sum(P[0])

    # pref_dist[i] es la distancia acumulada desde el puesto 0 hasta el puesto i
    pref_dist = [0] * N
    for i in range(1, N):
        pref_dist[i] = pref_dist[i - 1] + D[i - 1]

    ans_global = sys.maxsize

    def optimizacion_dnc(A_low: int, A_high: int, B_low: int, B_high: int):
        nonlocal ans_global
        if A_low > A_high:
            return

        A_mid = (A_low + A_high) // 2

        # B debe ser al menos A_mid (no se camina hacia atrás) y al menos B_low (monotonía)
        B_start_search = max(A_mid, B_low)
        B_end_search = max(B_start_search, B_high)
        if B_end_search >= N:
            B_end_search = N - 1

        best_cost = sys.maxsize
        best_B = B_start_search

        # Mantenemos los mínimos de los M libros para el subrango [A_mid, B]
        min_p = [sys.maxsize] * M

        # Acumular precios mínimos desde A_mid hasta B_start_search
        for i in range(A_mid, B_start_search + 1):
            for j in range(M):
                if P[i][j] < min_p[j]:
                    min_p[j] = P[i][j]

        # Evaluar el primer candidato B = B_start_search
        distancia = pref_dist[B_start_search] - pref_dist[A_mid]
        costo_libros = sum(min_p)
        best_cost = distancia + costo_libros
        best_B = B_start_search

        # Evaluamos el resto de los candidatos B en el rango [B_start_search + 1, B_end_search]
        for B in range(B_start_search + 1, B_end_search + 1):
            suma_libros = 0
            for j in range(M):
                if P[B][j] < min_p[j]:
                    min_p[j] = P[B][j]
                suma_libros += min_p[j]

            distancia = pref_dist[B] - pref_dist[A_mid]
            current_cost = distancia + suma_libros
            if current_cost < best_cost:
                best_cost = current_cost
                best_B = B

        if best_cost < ans_global:
            ans_global = best_cost

        # Dividir y vencer sobre los rangos de A acotando la búsqueda de B
        optimizacion_dnc(A_low, A_mid - 1, B_low, best_B)
        optimizacion_dnc(A_mid + 1, A_high, best_B, B_high)

    # Iniciar la optimización global sobre todo el rango [0, N-1]
    optimizacion_dnc(0, N - 1, 0, N - 1)

    return ans_global