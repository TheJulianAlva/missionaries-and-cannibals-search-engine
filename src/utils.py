"""Funciones de apoyo y utilidades para el problema.

Este módulo contiene funciones auxiliares para reconstruir rutas de solución,
visualizar estados en ASCII, imprimir resultados y medir el rendimiento
de los algoritmos de búsqueda.
"""

from __future__ import annotations

import time
import tracemalloc
from collections.abc import Callable
from typing import Any

from src.state import State


def reconstruct_solution_path(final_state: State) -> list[State]:
    """Reconstruye la secuencia de estados desde el inicio hasta la meta.

    Args:
        final_state (State): El estado meta devuelto por el algoritmo de búsqueda.

    Returns:
        list[State]: Lista ordenada de objetos State, del inicio a la meta.
    """
    path: list[State] = []
    current: State | None = final_state

    while current is not None:
        path.append(current)
        current = current.parent_state

    path.reverse()
    return path


def _render_state_ascii(state: State) -> str:
    """Genera una representación visual ASCII del estado actual del río.

    Args:
        state (State): El estado del problema a visualizar.

    Returns:
        str: Cadena de texto con la representación ASCII del estado.
    """
    left_m = "m " * state.missionaries_left
    left_c = "c " * state.cannibals_left
    right_m = "m " * state.missionaries_right
    right_c = "c " * state.cannibals_right

    boat_left  = "B " if state.boat_is_on_left_bank else "  "
    boat_right = "B " if not state.boat_is_on_left_bank else "  "

    left_bank  = f"[ {left_m}{left_c}{boat_left}]"
    right_bank = f"[ {right_m}{right_c}{boat_right}]"
    river      = "~~~rio~~~"

    _width = 17 # Ancho fijo
    left_bank  = left_bank.rjust(_width)
    right_bank = right_bank.ljust(_width)

    return f"  {left_bank}   {river}   {right_bank}"

def _print_solution(
    algorithm_name: str,
    final_state: State | None,
    nodes_explored: int,
    elapsed_time: float | None = None,
    peak_memory_kb: float | None = None,
) -> None:
    """Imprime en consola el resultado de una búsqueda de manera estructurada.

    Incluye la visualización ASCII de cada paso de la solución.

    Args:
        algorithm_name (str): Nombre descriptivo del algoritmo.
        final_state (State | None): Estado meta con su cadena de padres, o None si no hay solución.
        nodes_explored (int): Número de nodos procesados por el algoritmo.
        elapsed_time (float | None, optional): Tiempo de ejecución en segundos. Defaults to None.
        peak_memory_kb (float | None, optional): Memoria pico en kilobytes. Defaults to None.
    """
    separator = "-" * 60
    print(f"\n{separator}")
    print(f"  Algoritmo: {algorithm_name}")
    print(separator)

    if final_state is None:
        print("  No se encontro solucion.")
    else:
        states_path = reconstruct_solution_path(final_state)
        print(f"  Pasos en la solucion: {len(states_path) - 1}")
        print()

        # Estado inicial
        print(f"  Inicio: {_render_state_ascii(states_path[0])}")
        print()

        # Estados siguientes
        for index, state in enumerate(states_path[1:], start=1):
            print(f"  Paso {index:>2}: {state.action_taken}")
            print(_render_state_ascii(state))
            print()

    print(f"  Nodos explorados:     {nodes_explored}")

    if elapsed_time is not None:
        print(f"  Tiempo de ejecucion:  {elapsed_time:.6f} segundos")

    if peak_memory_kb is not None:
        print(f"  Memoria utilizada:    {peak_memory_kb:.4f} KB")

    print(separator)

def measure_execution_performance(
    algorithm_function: Callable[[State], tuple[State | None, int]],
    initial_state: State,
    algorithm_name: str,
) -> dict[str, Any]:
    """Mide el tiempo de ejecución y la memoria pico de un algoritmo de búsqueda.

    Imprime un reporte en consola utilizando time.perf_counter() para el tiempo de CPU,
    y tracemalloc para el registro de la memoria pico.

    Args:
        algorithm_function (Callable): La función de búsqueda a medir.
        initial_state (State): El estado inicial del problema.
        algorithm_name (str): Nombre descriptivo del algoritmo.

    Returns:
        dict[str, Any]: Diccionario con métricas de la ejecución, incluyendo estado final,
            tiempo transcurrido, nodos explorados y uso de memoria pico.
    """
    tracemalloc.start()
    start_time = time.perf_counter()

    final_state, nodes_explored = algorithm_function(initial_state)

    elapsed_time = time.perf_counter() - start_time

    _, peak_memory_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Convertir bytes a kilobytes
    peak_memory_kb = peak_memory_bytes / 1024

    _print_solution(
        algorithm_name=algorithm_name,
        final_state=final_state,
        nodes_explored=nodes_explored,
        elapsed_time=elapsed_time,
        peak_memory_kb=peak_memory_kb,
    )

    return {
        "algorithm_name": algorithm_name,
        "final_state": final_state,
        "nodes_explored": nodes_explored,
        "elapsed_time": elapsed_time,
        "peak_memory_kb": peak_memory_kb,
    }
