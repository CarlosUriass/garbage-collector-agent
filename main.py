from src.tablero import Tablero
from src.agente import Agente


ESCENARIOS = [
    [
        ". . . P .",
        ". X . . .",
        "A . . X P",
        ". . P . .",
        ". X . . .",
    ],
    [
        "P . X . .",
        ". . X . P",
        ". . A . .",
        "X . . . .",
        "P . X . .",
    ],
    [
        ". X . . P",
        ". X . X .",
        ". . A . .",
        "P X . X .",
        ". . . . P",
    ],
]


def construir_tablero_desde_escenario(escenario):
    filas = [linea.replace(" ", "") for linea in escenario if linea.strip()]
    if len(filas) != 5 or any(len(fila) != 5 for fila in filas):
        raise ValueError("Cada escenario debe tener 5 filas de 5 columnas.")

    tablero = Tablero(5, 5)
    posicion_agente = None

    for fila_index, fila in enumerate(filas):
        for columna_index, valor in enumerate(fila):
            if valor == "A":
                posicion_agente = (fila_index, columna_index)
            elif valor == "P":
                tablero.poner_paquete(fila_index, columna_index)
            elif valor == "X":
                tablero.poner_obstaculo(fila_index, columna_index)

    if posicion_agente is None:
        raise ValueError("El escenario debe incluir una posición inicial para el agente.")

    return tablero, posicion_agente


def ejecutar_escenario(escenario, numero_escenario):
    tablero, posicion_inicial = construir_tablero_desde_escenario(escenario)
    agente = Agente(tablero, posicion_inicial)

    paquetes_recogidos = 0
    movimientos = 0
    penalizaciones = 0

    print(f"\n=== Escenario {numero_escenario} ===")
    print("Estado inicial:")
    print(tablero)
    print(f"Score inicial: {agente.score.obtener_total()}")

    while True:
        accion = agente.decidir_accion()
        print(f"\nAcción decidida: {accion}")

        if accion == "RECOGER":
            resultado = agente.recoger()
            puntos = 10 if resultado == "RECOGER" else 0
            if resultado == "RECOGER":
                paquetes_recogidos += 1
            print(f"Resultado: {resultado}")
            print(f"Puntos por recoger: +{puntos} | Score actual: {agente.score.obtener_total()}")
        elif accion in ["TERMINAR", "DETENER"]:
            print(f"Fin de la simulación. Score final: {agente.score.obtener_total()}")
            break
        elif accion in ["ARRIBA", "ABAJO", "IZQUIERDA", "DERECHA"]:
            destino = agente._siguiente_posicion(accion)
            paquete_recogido = agente._obtener_celda(destino) == "P"
            if paquete_recogido:
                paquetes_recogidos += 1
            print(f"Moviendo hacia {accion} -> {destino}")
            resultado = agente.ejecutar_decision()
            if resultado in ["DESCARTAR", "BLOQUEAR"]:
                penalizaciones += 1
            else:
                movimientos += 1
            print(f"Resultado: {resultado}")
            if paquete_recogido:
                print(f"Paquete recogido: +10 | Score actual: {agente.score.obtener_total()}")
            else:
                print(f"Puntos por movimiento: -1 | Score actual: {agente.score.obtener_total()}")
        else:
            print(f"Resultado: {accion}")
            break

        print(tablero)

        if agente.acciones_realizadas >= agente.max_acciones:
            print(f"Se alcanzó el límite máximo de acciones. Score final: {agente.score.obtener_total()}")
            break

    print("\nResumen de la simulación:")
    print("-" * 50)
    print(f"Paquetes recogidos: {paquetes_recogidos}")
    print(f"Movimientos: {movimientos}")
    print(f"Penalizaciones: {penalizaciones}")
    if paquetes_recogidos > 0 and not any("P" in fila for fila in tablero.tablero):
        print("Bonus final: +20 por recoger todos los paquetes")
    print(f"Puntuación final: {agente.score.obtener_total()}")
    print("-" * 50)


def ejecutar_agente():
    for indice, escenario in enumerate(ESCENARIOS, start=1):
        ejecutar_escenario(escenario, indice)
        if indice < len(ESCENARIOS):
            input("\nPresiona Enter para continuar con el siguiente escenario...\n")


def main():
    ejecutar_agente()


if __name__ == "__main__":
    main()
