"""
Módulo: utils.py
Descripción: Funciones de apoyo.

Funciones disponibles:
    - reconstruct_solution_path: Reconstruye la lista de acciones desde la meta.
    - print_solution: Imprime en consola la ruta de solución y las métricas.
    - measure_execution_performance: Mide tiempo de ejecución y memoria de un algoritmo.
"""

from __future__ import annotations

import time
import tracemalloc
from collections.abc import Callable

from src.state import State


def reconstruct_solution_path(final_state: State) -> list[str]:
    """
    Reconstruye la secuencia de acciones que llevaron al estado meta.

    Itera hacia atrás siguiendo el atributo parent_state de cada nodo
    hasta llegar al estado raíz (sin padre), recopilando las descripciones
    de cada acción tomada.

    Args:
        final_state: El estado meta devuelto por el algoritmo de búsqueda.

    Returns:
        Lista ordenada de strings describiendo cada paso, del inicio a la meta.
    """
    path: list[str] = []
    current: State | None = final_state

    while current is not None and current.action_taken is not None:
        path.append(current.action_taken)
        current = current.parent_state

    path.reverse()  # El primero en la lista es el primer paso desde el inicio
    return path


def _print_solution(
    algorithm_name: str,
    final_state: State | None,
    nodes_explored: int,
    elapsed_time: float | None = None,
    peak_memory_kb: float | None = None,
) -> None:
    """
    Imprime en consola el resultado de una búsqueda de manera estructurada.

    Muestra:
        - El nombre del algoritmo.
        - Cada paso de la solución (si existe).
        - El número total de nodos explorados.
        - El tiempo de ejecución (si se proporciona).
        - La memoria pico utilizada (si se proporciona).

    Args:
        algorithm_name:  Nombre descriptivo del algoritmo.
        final_state:     Estado meta con su cadena de padres, o None si no hay solución.
        nodes_explored:  Número de nodos procesados por el algoritmo.
        elapsed_time:    Tiempo de ejecución en segundos (opcional).
        peak_memory_kb:  Memoria pico en kilobytes (opcional).
    """
    separator = "-" * 50
    print(f"\n{separator}")
    print(f"  Algoritmo: {algorithm_name}")
    print(separator)

    if final_state is None:
        print("  No se encontro solucion.")
    else:
        solution_path = reconstruct_solution_path(final_state)
        print(f"  Pasos en la solucion: {len(solution_path)}")
        print()
        for index, action in enumerate(solution_path, start=1):
            print(f"  Paso {index:>2}: {action}")

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
) -> None:
    """
    Mide el tiempo de ejecución y la memoria pico de un algoritmo de búsqueda,
    luego imprime un reporte en consola.

    Utiliza:
        - time.perf_counter() para tiempo de CPU.
        - tracemalloc para la memoria pico del proceso en bytes.

    Args:
        algorithm_function: La función de búsqueda a medir.
        initial_state: El estado inicial del problema.
        algorithm_name: Nombre para mostrar en la salida.
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
