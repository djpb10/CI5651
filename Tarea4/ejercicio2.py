def contar_subarreglos_buenos(A):
    """
    Calcula la cantidad de subarreglos "buenos" en A.
    Tiempo: O(n^2) | Memoria: O(n)
    """
    n = len(A)
    
    # dp[j] guardará la cantidad de subarreglos buenos de longitud j
    # Inicializamos con 0, y el tamaño es n + 1
    dp = [0] * (n + 1)
    
    # Caso base: hay 1 forma de tener un subarreglo de tamaño 0
    dp[0] = 1 
    
    # Iteramos sobre cada elemento del arreglo original
    for i in range(n):
        x = A[i]
        
        # Iteramos hacia atrás para no usar 'x' más de una vez en la misma iteración
        # La máxima longitud de un subarreglo usando el i-ésimo elemento (0-indexado) es i + 1
        for j in range(i + 1, 0, -1):
            if x % j == 0:
                # Si x es divisible por su nueva posición j, sumamos
                # las formas que teníamos de hacer un subarreglo de tamaño j-1
                dp[j] += dp[j - 1]
                
    # La respuesta es la suma de todas las combinaciones válidas 
    # de subarreglos de tamaño 1 o mayor.
    return sum(dp[1:])
