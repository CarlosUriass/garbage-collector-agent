import random

from src.score import Score


class Agente:
    DIRECCIONES = {
        "ARRIBA": (-1, 0),
        "ABAJO": (1, 0),
        "IZQUIERDA": (0, -1),
        "DERECHA": (0, 1),
    }

    ORDEN_HORARIO = ["ARRIBA", "DERECHA", "ABAJO", "IZQUIERDA"]

    def __init__(self, tablero, posicion):
        self.tablero = tablero
        self.posicion = posicion
        self.score = Score()
        self.ultima_accion = None
        self.direccion_actual = "DERECHA"
        self.historial_posiciones = [self.posicion]
        self.acciones_realizadas = 0
        self.max_acciones = 50

        if not self._posicion_valida(self.posicion):
            raise IndexError("La posición inicial del agente está fuera del tablero.")

        self.tablero.poner_agente(self.posicion[0], self.posicion[1])

    def _posicion_valida(self, posicion):
        fila, columna = posicion
        return 0 <= fila < self.tablero.largo and 0 <= columna < self.tablero.ancho

    def _obtener_celda(self, posicion):
        if not self._posicion_valida(posicion):
            return "FUERA_DEL_TABLERO"
        return self.tablero.obtener(posicion[0], posicion[1])

    def _es_transitable(self, posicion):
        valor = self._obtener_celda(posicion)
        return valor not in ["FUERA_DEL_TABLERO", "X"]

    def _siguiente_posicion(self, direccion):
        if direccion not in self.DIRECCIONES:
            raise ValueError(f"Dirección no válida: {direccion}")

        fila, columna = self.posicion
        delta_fila, delta_columna = self.DIRECCIONES[direccion]
        return (fila + delta_fila, columna + delta_columna)

    def _hay_paquetes_restantes(self):
        for fila in self.tablero.tablero:
            if "P" in fila:
                return True
        return False

    def recoger(self):
        fila, columna = self.posicion
        if self.tablero.obtener(fila, columna) == "P":
            self.tablero.poner(fila, columna, ".")
            self.score.recoger_paquete()
            if not self._hay_paquetes_restantes():
                self.score.recoger_todos_los_paquetes()
            return "RECOGER"
        return "SIN_PAQUETE"

    def mover(self, nueva_posicion):
        if not self._posicion_valida(nueva_posicion):
            raise IndexError("La nueva posición está fuera del tablero.")

        fila_actual, columna_actual = self.posicion
        nueva_fila, nueva_columna = nueva_posicion

        diferencia_fila = abs(nueva_fila - fila_actual)
        diferencia_columna = abs(nueva_columna - columna_actual)

        if diferencia_fila + diferencia_columna != 1:
            raise ValueError("El agente solo puede moverse una casilla arriba, abajo, izquierda o derecha.")

        valor_destino = self.tablero.obtener(nueva_fila, nueva_columna)
        if valor_destino == "X":
            raise ValueError("No puedes moverte hacia un obstáculo.")

        self.tablero.poner(fila_actual, columna_actual, ".")
        if valor_destino == "P":
            self.score.recoger_paquete()
        self.tablero.poner_agente(nueva_fila, nueva_columna)
        self.posicion = nueva_posicion
        self.ultima_accion = self._direccion_entre(self.posicion, (fila_actual, columna_actual))
        self.direccion_actual = self.ultima_accion
        self.acciones_realizadas += 1
        self.historial_posiciones.append(self.posicion)
        if len(self.historial_posiciones) > 6:
            self.historial_posiciones.pop(0)

        return self.posicion

    def _direccion_entre(self, actual, anterior):
        delta_fila = actual[0] - anterior[0]
        delta_columna = actual[1] - anterior[1]

        if delta_fila == -1 and delta_columna == 0:
            return "ARRIBA"
        if delta_fila == 1 and delta_columna == 0:
            return "ABAJO"
        if delta_fila == 0 and delta_columna == -1:
            return "IZQUIERDA"
        if delta_fila == 0 and delta_columna == 1:
            return "DERECHA"
        return self.ultima_accion

    def _bloqueada(self, direccion):
        posicion = self._siguiente_posicion(direccion)
        return not self._es_transitable(posicion)

    def _siguiente_direccion_horaria(self, direccion_actual):
        indice = self.ORDEN_HORARIO.index(direccion_actual)
        orden = self.ORDEN_HORARIO[indice:] + self.ORDEN_HORARIO[:indice]
        return orden[1:] + [orden[0]]

    def _direcciones_transitables(self):
        disponibles = []
        for direccion in self.ORDEN_HORARIO:
            destino = self._siguiente_posicion(direccion)
            if self._es_transitable(destino):
                disponibles.append(direccion)
        return disponibles

    def _direccion_aleatoria_no_visitada(self):
        recientes = self.historial_posiciones[-2:]
        opciones = []
        for direccion in self.ORDEN_HORARIO:
            destino = self._siguiente_posicion(direccion)
            if self._es_transitable(destino) and destino not in recientes:
                opciones.append(direccion)
        if not opciones:
            return None
        return random.choice(opciones)

    def decidir_accion(self):
        if self.acciones_realizadas >= self.max_acciones:
            return "DETENER"

        if not self._hay_paquetes_restantes():
            return "TERMINAR"

        if self.tablero.obtener(self.posicion[0], self.posicion[1]) == "P":
            return "RECOGER"

        for direccion in self.ORDEN_HORARIO:
            destino = self._siguiente_posicion(direccion)
            if self._obtener_celda(destino) == "P" and self._es_transitable(destino):
                return direccion

        if self.ultima_accion == "DERECHA":
            destino = self._siguiente_posicion("DERECHA")
            if self._es_transitable(destino):
                return "DERECHA"

        if self._bloqueada(self.direccion_actual):
            for direccion in self._siguiente_direccion_horaria(self.direccion_actual):
                destino = self._siguiente_posicion(direccion)
                if self._es_transitable(destino):
                    return direccion

        if len(self.historial_posiciones) >= 3:
            direccion = self._direccion_aleatoria_no_visitada()
            if direccion:
                return direccion

        opciones = self._direcciones_transitables()
        if opciones:
            return random.choice(opciones)

        return "DETENER"

    def ejecutar_decision(self):
        accion = self.decidir_accion()

        if accion == "RECOGER":
            return self.recoger()

        if accion in ["DETENER", "TERMINAR"]:
            return accion

        destino = self._siguiente_posicion(accion)
        if self._obtener_celda(destino) == "X":
            self.score.intentar_chocar_obstaculo()
            return "DESCARTAR"

        if self._obtener_celda(destino) == "FUERA_DEL_TABLERO":
            self.score.intentar_salir_tablero()
            return "BLOQUEAR"

        self.mover(destino)
        self.score.mover()
        return accion
