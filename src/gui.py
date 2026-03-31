import tkinter as tk
from tkinter import ttk
from typing import Any

from src.state import State
from src.utils import reconstruct_solution_path


class ResultsGUI:
    """Muestra la interfaz gráfica de resultados de Misioneros y Caníbales.

    Attributes:
        root (tk.Tk): La ventana raíz de la interfaz gráfica.
        style (ttk.Style): Estilos configurados para los widgets.
        notebook (ttk.Notebook): Pestañas para cada resultado de algoritmo.
        tabs_state (dict): Diccionario que mantiene el estado interno de cada pestaña.
    """

    def __init__(self, root: tk.Tk, results: list[dict[str, Any]]) -> None:
        """Inicializa la interfaz ResultsGUI.

        Args:
            root (tk.Tk): La ventana raíz de la interfaz gráfica.
            results (list[dict[str, Any]]): Lista de diccionarios con métricas de resultados.
        """
        self.root = root
        self.root.title("Resultados - Misioneros y Canibales")
        self.root.geometry("900x650")
        self.root.configure(bg="#2d2d2d")

        # Configurar estilos
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TNotebook", background="#2d2d2d", borderwidth=0)
        self.style.configure("TNotebook.Tab", background="#3d3d3d", foreground="white", padding=[10, 5], font=("Segoe UI", 10))
        self.style.map("TNotebook.Tab", background=[("selected", "#007acc")])
        self.style.configure("TFrame", background="#2d2d2d")
        self.style.configure("TLabel", background="#2d2d2d", foreground="white", font=("Segoe UI", 11))
        self.style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground="#007acc")
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"), background="#007acc", foreground="white")
        self.style.map("TButton", background=[("active", "#005999")])

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Para mantener el estado de cada pestaña
        self.tabs_state = {}

        for result in results:
            self.create_tab(result)

    def create_tab(self, result_data: dict[str, Any]) -> None:
        """Crea una nueva pestaña para visualizar el resultado de un algoritmo.

        Args:
            result_data (dict[str, Any]): Diccionario con el nombre del algoritmo,
                nodos explorados, tiempo, memoria y estado final (meta).
        """
        tab_frame = ttk.Frame(self.notebook, padding=10)
        algo_name = result_data["algorithm_name"]
        self.notebook.add(tab_frame, text=algo_name)

        # Extraer métricas
        nodes = result_data["nodes_explored"]
        time_elapsed = result_data["elapsed_time"]
        memory = result_data["peak_memory_kb"]
        final_state = result_data["final_state"]

        # Panel superior (Métricas)
        metrics_frame = ttk.Frame(tab_frame)
        metrics_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(metrics_frame, text=algo_name, style="Header.TLabel").pack(anchor=tk.W)
        metrics_text = f"Nodos explorados: {nodes}   |   Tiempo: {time_elapsed:.6f} s   |   Memoria peak: {memory:.4f} KB"
        ttk.Label(metrics_frame, text=metrics_text).pack(anchor=tk.W, pady=5)

        # Obtener pasos
        steps = []
        if final_state is not None:
            steps = reconstruct_solution_path(final_state)
        
        # Panel central (Dibujo Canvas)
        canvas_frame = ttk.Frame(tab_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(canvas_frame, bg="#1e1e1e", highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Panel inferior (Controles y texto descriptivo)
        controls_frame = ttk.Frame(tab_frame)
        controls_frame.pack(fill=tk.X, pady=(10, 0))

        step_label_var = tk.StringVar(value="--")
        action_label_var = tk.StringVar(value="No se encontró solución" if not steps else "Estado Inicial")

        ttk.Label(controls_frame, textvariable=action_label_var, font=("Segoe UI", 11, "italic")).pack(pady=(0, 10))

        btn_container = ttk.Frame(controls_frame)
        btn_container.pack()

        btn_prev = ttk.Button(btn_container, text="◀ Anterior", width=15)
        btn_prev.pack(side=tk.LEFT, padx=5)
        
        lbl_step = ttk.Label(btn_container, textvariable=step_label_var, font=("Segoe UI", 12, "bold"))
        lbl_step.pack(side=tk.LEFT, padx=15)

        btn_next = ttk.Button(btn_container, text="Siguiente ▶", width=15)
        btn_next.pack(side=tk.LEFT, padx=5)

        # Estado de la pestaña para la navegación
        state_info = {
            "steps": steps,
            "current_index": 0,
            "canvas": canvas,
            "step_label_var": step_label_var,
            "action_label_var": action_label_var,
            "btn_prev": btn_prev,
            "btn_next": btn_next
        }
        self.tabs_state[algo_name] = state_info

        # Bind events
        btn_prev.configure(command=lambda: self.navigate(algo_name, -1))
        btn_next.configure(command=lambda: self.navigate(algo_name, 1))

        # Dibujar estado inicial
        if steps:
            self.update_canvas(algo_name)
        else:
            self.draw_no_solution(canvas)

    def navigate(self, algo_name: str, direction: int) -> None:
        """Navega entre los pasos de la solución dibujados en la interfaz.

        Args:
            algo_name (str): Nombre del algoritmo (clave en tabs_state).
            direction (int): Cantidad de pasos a mover (-1 para anterior, 1 para siguiente).
        """
        state_info = self.tabs_state[algo_name]
        steps = state_info["steps"]
        new_index = state_info["current_index"] + direction

        if 0 <= new_index < len(steps):
            state_info["current_index"] = new_index
            self.update_canvas(algo_name)

    def update_canvas(self, algo_name: str) -> None:
        """Dibuja el estado actual en el canvas correspondiente a la pestaña.

        Args:
            algo_name (str): Nombre del algoritmo cuyos pasos se van a visualizar.
        """
        state_info = self.tabs_state[algo_name]
        steps = state_info["steps"]
        idx = state_info["current_index"]
        canvas: tk.Canvas = state_info["canvas"]
        current_state: State = steps[idx]

        # Actualizar labels
        total_steps = len(steps) - 1
        state_info["step_label_var"].set(f"Paso {idx} / {total_steps}")
        
        action_text = current_state.action_taken if current_state.action_taken else "Inicio del problema"
        if idx == len(steps) - 1 and len(steps) > 1:
            action_text += " ¡META ALCANZADA!"
        state_info["action_label_var"].set(action_text)

        # Actualizar botones
        state_info["btn_prev"].state(["!disabled"] if idx > 0 else ["disabled"])
        state_info["btn_next"].state(["!disabled"] if idx < len(steps) - 1 else ["disabled"])

        # Dibujar el entorno
        canvas.delete("all")
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        
        # En caso de que no se haya renderizado aún
        if width <= 1:
            width = 800
            height = 400

        # Zonas
        bank_width = width * 0.25
        river_width = width * 0.5

        # Colores
        color_bank = "#4caf50"  # Verde orilla
        color_river = "#2196f3" # Azul rio
        color_missionary = "#ffc107" # Amarillo
        color_cannibal = "#f44336"   # Rojo
        color_boat = "#795548"       # Café bote

        # Dibujar orillas y rio
        canvas.create_rectangle(0, 0, bank_width, height, fill=color_bank, outline="")
        canvas.create_rectangle(bank_width, 0, bank_width + river_width, height, fill=color_river, outline="")
        canvas.create_rectangle(bank_width + river_width, 0, width, height, fill=color_bank, outline="")

        # Dibujar elementos
        y_center = height / 2
        element_spacing = 40

        # Función auxiliar para dibujar personajes
        def draw_characters(count_m, count_c, x_start, is_left):
            # Misioneros
            for i in range(count_m):
                x = x_start - (i * element_spacing) if is_left else x_start + (i * element_spacing)
                y = y_center - 50
                canvas.create_oval(x-15, y-15, x+15, y+15, fill=color_missionary, outline="#333", width=2)
                canvas.create_text(x, y, text="M", font=("Segoe UI", 12, "bold"))

            # Canibales
            for i in range(count_c):
                x = x_start - (i * element_spacing) if is_left else x_start + (i * element_spacing)
                y = y_center + 50
                canvas.create_oval(x-15, y-15, x+15, y+15, fill=color_cannibal, outline="#333", width=2)
                canvas.create_text(x, y, text="C", font=("Segoe UI", 12, "bold"), fill="white")

        # Dibujar orilla izquierda (personajes desde el borde del rio hacia la izq)
        draw_characters(current_state.missionaries_left, current_state.cannibals_left, bank_width - 30, True)

        # Dibujar orilla derecha (personajes desde el borde del rio hacia la der)
        draw_characters(current_state.missionaries_right, current_state.cannibals_right, bank_width + river_width + 30, False)

        # Dibujar bote
        boat_width = 100
        boat_height = 40
        if current_state.boat_is_on_left_bank:
            boat_x = bank_width + 20
        else:
            boat_x = bank_width + river_width - boat_width - 20
        
        boat_y = y_center - (boat_height / 2)
        
        # Forma del bote (poligono simple)
        canvas.create_polygon(
            boat_x, boat_y,
            boat_x + boat_width, boat_y,
            boat_x + boat_width - 15, boat_y + boat_height,
            boat_x + 15, boat_y + boat_height,
            fill=color_boat, outline="#333", width=2
        )
        canvas.create_text(boat_x + boat_width/2, boat_y + boat_height/2, text="B", font=("Segoe UI", 12, "bold"), fill="white")

    def draw_no_solution(self, canvas: tk.Canvas) -> None:
        """Dibuja un mensaje indicando que el algoritmo no encontró solución.

        Args:
            canvas (tk.Canvas): El lienzo sobre el cual se mostrará el mensaje de error.
        """
        canvas.delete("all")
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        canvas.create_text(
            width/2, height/2,
            text="No se encontró solución",
            font=("Segoe UI", 24, "bold"),
            fill="#f44336"
        )
