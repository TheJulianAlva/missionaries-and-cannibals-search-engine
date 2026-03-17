"""
main.py
Punto de entrada temporal para validar la Iteración 2 (BFS).
Se ampliará en las iteraciones 3 y 4.
"""

from src.state import State
from src.algorithms import breadth_first_search
from src.utils import print_solution


def main() -> None:
    initial_state = State(
        missionaries_left=3,
        cannibals_left=3,
        boat_is_on_left_bank=True,
    )

    goal_state, nodes_explored = breadth_first_search(initial_state)
    print_solution(
        algorithm_name="Busqueda en Amplitud (BFS)",
        final_state=goal_state,
        nodes_explored=nodes_explored,
    )


if __name__ == "__main__":
    main()
