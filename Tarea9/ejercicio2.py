import numpy as np
import random

def verify_matrix_inverse(A, B, k):
    """
    Verifica si B es la inversa de A utilizando un algoritmo de Monte Carlo (inspirado en Freivalds).
    
    Argumentos:
        A: Un arreglo cuadrado de numpy de tamaño n x n.
        B: Un arreglo cuadrado de numpy de tamaño n x n.
        k: El número de iteraciones para alcanzar la probabilidad de error deseada.
           Probabilidad de error <= (1/2)^k.
           
    Retorna:
        True si es altamente probable que B sea la inversa de A, False en caso contrario.
    """
    n = A.shape[0]
    
    # Queremos comprobar si AB = I. 
    # Para hacer esto eficientemente, comprobamos si ABx = Ix = x para vectores aleatorios x.
    # Podemos reescribir esto como A(Bx) = x para evitar la multiplicación matriz-matriz.
    
    for _ in range(k):
        # Generar un vector aleatorio x con elementos de {0, 1}
        x = np.random.randint(0, 2, size=(n, 1))
        
        # Calcular Bx
        # Esto toma tiempo O(n^2)
        Bx = np.dot(B, x)
        
        # Calcular A(Bx)
        # Esto también toma tiempo O(n^2)
        ABx = np.dot(A, Bx)
        
        # Comprobar si A(Bx) == x
        # Usamos np.allclose para manejar posibles inexactitudes de punto flotante
        # si las matrices contienen números reales.
        if not np.allclose(ABx, x):
            return False # Se encontró un vector donde ABx != x, por lo tanto AB != I
            
    return True 
