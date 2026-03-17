"""
main.py
Punto de entrada del proyecto: Misioneros y Canibales.
Ejecuta BFS y DFS midiendo tiempo de ejecucion y memoria utilizada.
"""
from src.state import State
from src.algorithms import breadth_first_search, depth_first_search
from src.utils import measure_execution_performance


def main() -> None:
    # Estado inicial: 3 misioneros, 3 canibales, bote en la izquierda
    initial_state = State(
        missionaries_left=3,
        cannibals_left=3,
        boat_is_on_left_bank=True,
    )

    # Busqueda en Amplitud (BFS)
    measure_execution_performance(
        algorithm_function=breadth_first_search,
        initial_state=initial_state,
        algorithm_name="Busqueda en Amplitud (BFS)",
    )

    # Busqueda en Profundidad (DFS)
    measure_execution_performance(
        algorithm_function=depth_first_search,
        initial_state=initial_state,
        algorithm_name="Busqueda en Profundidad (DFS)",
    )


if __name__ == "__main__":
    main()
