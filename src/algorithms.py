"""Implementaciones de los algoritmos de búsqueda no informada.

Este módulo contiene los algoritmos de Búsqueda en Amplitud (BFS)
y Búsqueda en Profundidad (DFS) para resolver el problema.
"""

from __future__ import annotations

from collections import deque

from src.state import State


def breadth_first_search(initial_state: State) -> tuple[State | None, int]:
    """Aplica la Búsqueda en Amplitud (BFS) para encontrar la solución óptima.

    Utiliza una cola FIFO (collections.deque) como frontera.
    Explora primero todos los estados a profundidad N antes de pasar a N+1.
    Garantiza encontrar el camino más corto si existe solución.

    Args:
        initial_state (State): El estado de inicio del problema.

    Returns:
        tuple[State | None, int]: Una tupla que contiene:
            - estado_meta (State | None): Objeto State en la meta, o None si no hay solución.
            - nodos_explorados (int): Número total de nodos procesados.
    """
    # Cola FIFO: almacena los estados por explorar
    frontier: deque[State] = deque([initial_state])

    # Conjunto de estados ya visitados
    explored_states: set[State] = set()
    explored_states.add(initial_state)

    nodes_explored: int = 0

    while frontier:
        current_state = frontier.popleft()
        nodes_explored += 1

        # Verificar si llegamos a la meta
        if current_state.is_goal_state():
            return current_state, nodes_explored

        # Expandir sucesores válidos no visitados
        for successor in current_state.generate_successors():
            if successor not in explored_states:
                explored_states.add(successor)
                frontier.append(successor)

    # Sin solución
    return None, nodes_explored










def depth_first_search(initial_state: State) -> tuple[State | None, int]:
    """Aplica la Búsqueda en Profundidad (DFS) para encontrar una solución.

    Utiliza una pila LIFO (lista de Python) como frontera.
    Explora cada rama hasta su mayor profundidad antes de retroceder.
    No garantiza el camino más corto, pero usa menos memoria que BFS.

    Args:
        initial_state (State): El estado de inicio del problema.

    Returns:
        tuple[State | None, int]: Una tupla que contiene:
            - estado_meta (State | None): Objeto State en la meta, o None si no hay solución.
            - nodos_explorados (int): Número total de nodos procesados.
    """
    # Pila LIFO: almacena los estados por explorar
    frontier: list[State] = [initial_state]

    # Conjunto de estados ya visitados
    explored_states: set[State] = set()
    explored_states.add(initial_state)

    nodes_explored: int = 0

    while frontier:
        current_state = frontier.pop()
        nodes_explored += 1

        # Verificar si llegamos a la meta
        if current_state.is_goal_state():
            return current_state, nodes_explored

        # Expandir sucesores válidos no visitados
        for successor in current_state.generate_successors():
            if successor not in explored_states:
                explored_states.add(successor)
                frontier.append(successor)

    # Sin solución
    return None, nodes_explored
