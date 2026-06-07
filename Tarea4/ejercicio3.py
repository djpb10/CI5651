import sys

class ArregloVirtual:
    def __init__(self, size):
        self.size = size
        # Arreglo principal que guarda los valores
        self.A = [0] * size
        # Arreglo auxiliar que guarda las posiciones en la pila (top)
        self.P = [0] * size
        # Pila que registra el orden de inicialización
        self.S = [0] * size
        # Tope de la pila, indica cuántos elementos han sido inicializados
        self.top = 0

    def es_valida(self, pos):
        """Verifica si la posición está dentro de los límites del arreglo."""
        return 0 <= pos < self.size

    def esta_inicializada(self, pos):
        """
        Verifica si la posición pos ha sido inicializada según el proceso
        de inicialización virtual.
        Debe cumplir: 0 <= P[pos] < top y S[P[pos]] == pos
        """
        p_val = self.P[pos]
        if 0 <= p_val < self.top and self.S[p_val] == pos:
            return True
        return False

    def asignar(self, pos, val):
        """
        Asigna el valor val a la posición pos.
        Si la posición no estaba inicializada, actualiza la pila S y el arreglo P.
        """
        if not self.es_valida(pos):
            print(f"Error: La posición {pos} no es válida. Debe estar entre 0 y {self.size - 1}.")
            return

        if not self.esta_inicializada(pos):
            # Registrar en la pila S la nueva posición inicializada
            self.S[self.top] = pos
            # Registrar en P el índice en la pila donde se guardó pos
            self.P[pos] = self.top
            # Incrementar el tope de la pila
            self.top += 1

        # Asignar el valor en el arreglo principal
        self.A[pos] = val
        print(f"Valor {val} asignado correctamente en la posición {pos}.")

    def consultar(self, pos):
        """
        Consulta si la posición pos está inicializada.
        Si lo está, devuelve el valor. Si no, o si la posición es inválida, reporta error.
        """
        if not self.es_valida(pos):
            print(f"Error: La posición {pos} no es válida. Debe estar entre 0 y {self.size - 1}.")
            return

        if self.esta_inicializada(pos):
            print(f"La posición {pos} ESTÁ inicializada. Valor asociado: {self.A[pos]}")
        else:
            print(f"La posición {pos} NO está inicializada.")

    def limpiar(self):
        """
        Limpia virtualmente la tabla restableciendo el tope de la pila a 0.
        """
        self.top = 0
        print("La tabla ha sido limpiada exitosamente. Todas las posiciones están sin inicializar.")


def main():
    # El programa debe recibir el tamaño del arreglo como argumento del sistema.
    if len(sys.argv) != 2:
        print("Uso: python inicializacion_virtual.py <tamaño_del_arreglo>")
        print("Ejemplo: python inicializacion_virtual.py 100")
        sys.exit(1)

    try:
        size = int(sys.argv[1])
        if size <= 0:
            print("El tamaño del arreglo debe ser un entero positivo.")
            sys.exit(1)
    except ValueError:
        print("Error: El tamaño del arreglo debe ser un número entero.")
        sys.exit(1)

    # Inicializar la estructura
    arreglo_virtual = ArregloVirtual(size)
    print(f"Arreglo virtual de tamaño {size} creado exitosamente.")

    # Ciclo principal del cliente
    while True: 
        print("\nOpciones:") 
        print("1. ASIGNAR POS VAL") 
        print("2. CONSULTAR POS") 
        print("3. LIMPIAR") 
        print("4. SALIR") 
        opcion = input("Ingrese su comando: ").strip().upper() 
 
        if opcion.startswith("ASIGNAR"): 
            try: 
                _, pos_str, val_str = opcion.split() 
                pos = int(pos_str) 
                val = int(val_str) 
                arreglo_virtual.asignar(pos, val) 
            except ValueError: 
                print("Error: Formato incorrecto. Use: ASIGNAR POS VAL") 
 
        elif opcion.startswith("CONSULTAR"): 
            try: 
                _, pos_str = opcion.split() 
                pos = int(pos_str) 
                arreglo_virtual.consultar(pos) 
            except ValueError: 
                print("Error: Formato incorrecto. Use: CONSULTAR POS") 
 
        elif opcion == "LIMPIAR": 
            arreglo_virtual.limpiar() 
 
        elif opcion == "SALIR": 
            print("Saliendo...") 
            break 
 
        else: 
            print("Opción no válida")

if __name__ == "__main__":
    main()
