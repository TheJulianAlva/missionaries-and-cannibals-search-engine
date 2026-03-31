"""Módulo principal del proyecto Misioneros y Caníbales.

Este módulo sirve como punto de entrada para ejecutar los algoritmos
de Búsqueda en Amplitud (BFS) y Búsqueda en Profundidad (DFS) sobre
el problema de los Misioneros y Caníbales, midiendo y mostrando
su rendimiento.
"""
import tkinter as tk

from src.state import State
from src.algorithms import breadth_first_search, depth_first_search
from src.utils import measure_execution_performance
from src.gui import ResultsGUI


def main() -> None:
    """Ejecuta el programa principal.

    Inicializa el estado inicial, ejecuta los algoritmos de búsqueda BFS y DFS,
    mide su rendimiento y finalmente muestra los resultados en una interfaz gráfica
    de usuario (GUI).
    """
    # Estado inicial: 3 misioneros, 3 canibales, bote en la izquierda
    initial_state = State(
        missionaries_left=3,
        cannibals_left=3,
        boat_is_on_left_bank=True,
    )

    # Busqueda en Amplitud (BFS)
    bfs_result = measure_execution_performance(
        algorithm_function=breadth_first_search,
        initial_state=initial_state,
        algorithm_name="Busqueda en Amplitud (BFS)",
    )

    # Busqueda en Profundidad (DFS)
    dfs_result = measure_execution_performance(
        algorithm_function=depth_first_search,
        initial_state=initial_state,
        algorithm_name="Busqueda en Profundidad (DFS)",
    )

    # Iniciar GUI para mostrar ambos resultados
    root = tk.Tk()
    app = ResultsGUI(root, [bfs_result, dfs_result])
    
    # Manejar eventos de resize para que el Canvas redibuje correctamente
    # Hacemos que un pequeño retraso despues de mostrar la venta redibuje la vista actual.
    root.update()
    for tab_name in app.tabs_state:
        # Llamar a navigate con 0 de offset re-dibuja el estado actua usando el ancho/alto real
        app.navigate(tab_name, 0)

    root.mainloop()


if __name__ == "__main__":
    main()
