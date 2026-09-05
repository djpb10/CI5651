def find_longest_prefix_suffix(S):
    n = len(S)
    if n == 0:
        return ""

    # pi[i] almacenará la longitud del prefijo propio más largo 
    pi = [0] * n
    
    length = 0
    i = 1

    # Construcción del arreglo pi
    while i < n:
        if S[i] == S[length]:
            length += 1
            pi[i] = length
            i += 1
        else:
            if length > 0:
                # Retroceso usando valores previos calculados
                length = pi[length - 1]
            else:
                pi[i] = 0
                i += 1

    # El último valor del arreglo pi nos da la longitud de la subcadena buscada
    L = pi[-1]
    
    if L > 0:
        return S[:L]
    else:
        return "" # cadena vacia 
