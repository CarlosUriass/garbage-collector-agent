class Tablero:
    def __init__(self, ancho, largo):
        if ancho <= 0 or largo <= 0:
            raise ValueError("El ancho y el largo deben ser mayores que cero.")

        self.ancho = ancho
        self.largo = largo
        self.tablero = [[" " for _ in range(ancho)] for _ in range(largo)]

    def mostrar(self):
        print(self)

    def __str__(self):
        return "\n".join(" | ".join(fila) for fila in self.tablero)

    def poner(self, fila, columna, valor):
        if 0 <= fila < self.largo and 0 <= columna < self.ancho:
            self.tablero[fila][columna] = valor
        else:
            raise IndexError("La posición indicada está fuera del tablero.")

    def obtener(self, fila, columna):
        if 0 <= fila < self.largo and 0 <= columna < self.ancho:
            return self.tablero[fila][columna]
        raise IndexError("La posición indicada está fuera del tablero.")
