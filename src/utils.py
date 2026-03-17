"""
Módulo: utils.py
Descripción: Funciones de apoyo.

Funciones disponibles:
    - reconstruct_solution_path: Reconstruye la lista de acciones desde la meta.
    - print_solution: Imprime en consola la ruta de solución y las métricas.
"""

from __future__ import annotations

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


def print_solution(
    algorithm_name: str,
    final_state: State | None,
    nodes_explored: int,
) -> None:
    """
    Imprime en consola el resultado de una búsqueda de manera estructurada.

    Muestra:
        - El nombre del algoritmo.
        - Cada paso de la solución (si existe).
        - El número total de nodos explorados.

    Args:
        algorithm_name: Nombre descriptivo del algoritmo.
        final_state:    Estado meta con su cadena de padres, o None si no hay solución.
        nodes_explored: Número de nodos procesados por el algoritmo.
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
    print(f"  Nodos explorados: {nodes_explored}")
    print(separator)
