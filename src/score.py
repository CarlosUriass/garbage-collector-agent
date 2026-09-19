class Score:
    def __init__(self, total=0):
        self.total = total

    def recoger_paquete(self):
        self.total += 10
        return self.total

    def mover(self):
        self.total -= 1
        return self.total

    def intentar_salir_tablero(self):
        self.total -= 5
        return self.total

    def intentar_chocar_obstaculo(self):
        self.total -= 5
        return self.total

    def recoger_todos_los_paquetes(self):
        self.total += 20
        return self.total

    def obtener_total(self):
        return self.total
