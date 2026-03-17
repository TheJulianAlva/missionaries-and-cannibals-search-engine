"""
main.py
Punto de entrada del proyecto: Misioneros y Canibales.
Ejecuta BFS y DFS y muestra los resultados en consola.
"""

from src.state import State
from src.algorithms import breadth_first_search, depth_first_search
from src.utils import print_solution


def main() -> None:
    # Estado inicial: 3 misioneros, 3 canibales, bote en la izquierda
    initial_state = State(
        missionaries_left=3,
        cannibals_left=3,
        boat_is_on_left_bank=True,
    )

    # --- Busqueda en Amplitud (BFS) ---
    goal_bfs, nodes_bfs = breadth_first_search(initial_state)
    print_solution(
        algorithm_name="Busqueda en Amplitud (BFS)",
        final_state=goal_bfs,
        nodes_explored=nodes_bfs,
    )

    # --- Busqueda en Profundidad (DFS) ---
    goal_dfs, nodes_dfs = depth_first_search(initial_state)
    print_solution(
        algorithm_name="Busqueda en Profundidad (DFS)",
        final_state=goal_dfs,
        nodes_explored=nodes_dfs,
    )


if __name__ == "__main__":
    main()
