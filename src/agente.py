class Agente:
    def __init__(self, tablero, posicion):
        self.tablero = tablero
        self.posicion = posicion

        if not self._posicion_valida(self.posicion):
            raise IndexError("La posición inicial del agente está fuera del tablero.")

        self.tablero.poner_agente(self.posicion[0], self.posicion[1])

    def _posicion_valida(self, posicion):
        fila, columna = posicion
        return 0 <= fila < self.tablero.largo and 0 <= columna < self.tablero.ancho

    def mover(self, nueva_posicion):
        if not self._posicion_valida(nueva_posicion):
            raise IndexError("La nueva posición está fuera del tablero.")

        fila_actual, columna_actual = self.posicion
        nueva_fila, nueva_columna = nueva_posicion

        diferencia_fila = abs(nueva_fila - fila_actual)
        diferencia_columna = abs(nueva_columna - columna_actual)

        if diferencia_fila + diferencia_columna != 1:
            raise ValueError("El agente solo puede moverse una casilla arriba, abajo, izquierda o derecha.")

        self.tablero.poner(fila_actual, columna_actual, ".")
        self.tablero.poner_agente(nueva_fila, nueva_columna)
        self.posicion = nueva_posicion

        return self.posicion