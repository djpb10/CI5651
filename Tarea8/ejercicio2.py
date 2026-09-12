import cmath
from typing import List

def fft(a: List[complex], invert: bool = False):
    """
    Calcula la Transformada Rápida de Fourier (FFT) in-place usando el 
    algoritmo iterativo de Cooley-Tukey en O(N log N).
    
    :param a: Lista de números complejos. Su longitud debe ser potencia de 2.
    :param invert: Si es True, calcula la FFT Inversa (IFFT).
    """
    n = len(a)
    
    # Reordenamiento de bit-reversal (Permutación)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
            
    length = 2
    while length <= n:
        ang = 2 * cmath.pi / length
        if invert:
            ang = -ang
        wlen = cmath.rect(1, ang)
        
        half = length // 2
        for i in range(0, n, length):
            w = 1
            for j in range(half):
                u = a[i + j]
                v = a[i + j + half] * w

                a[i + j] = u + v
                a[i + j + half] = u - v
                w *= wlen
        length *= 2
        
    # Normalización para la IFFT
    if invert:
        for i in range(n):
            a[i] /= n

def decomp(N: int) -> int:
    """
    Halla el máximo valor de decomp(X) para 1 <= X <= N.
    Complejidad de Tiempo: O(N log N)
    Complejidad de Espacio: O(N)
    """
    # Casos base: X=1 nunca tendrá solución puesto que ab+cd requiere al menos 1*1 + 1*1 = 2
    if N < 2:
        return 0
        
    # Criba para contar divisores en O(N log N)
    # divisors[i] almacenará la cantidad de divisores de i (d(i))
    divisors = [0] * (N + 1)
    for i in range(1, N + 1):
        # Cada múltiplo de 'i' recibe a 'i' como divisor.
        # Iteramos saltando de i en i. 
        for j in range(i, N + 1, i):
            divisors[j] += 1
            
    # Encontrar la siguiente potencia de 2 para el arreglo de la FFT.
    # El polinomio resultante tendrá grado hasta 2*N, por lo que el tamaño
    # mínimo del arreglo debe ser > 2*N.
    m = 1
    while m <= 2 * N:
        m *= 2
        
    # Construir el polinomio P(x) de coeficientes complejos
    # P(x) = d(1)x^1 + d(2)x^2 + ... + d(N)x^N
    P = [complex(divisors[i], 0) if i <= N else complex(0, 0) for i in range(m)]
    
    # Llevar el polinomio al dominio de las frecuencias
    fft(P, False)
    
    # Multiplicar el polinomio por sí mismo P(x) * P(x)
    for i in range(m):
        P[i] *= P[i]
        
    # Devolver al dominio de los coeficientes mediante la IFFT
    fft(P, True)
    
    # Buscar el máximo valor para X en el rango [1, N]
    max_val = 0
    

    for X in range(2, N + 1):

        actual_decomp = int(round(P[X].real))
        if actual_decomp > max_val:
            max_val = actual_decomp
            
    return max_val
