# Plan de Implementación

## 1. Módulos y Estructura de Archivos
- `src/state.py`: Módulo autónomo para definir un estado del juego y la lógica de validación.
- `src/algorithms.py`: Módulo enfocado únicamente en la lógica de las búsquedas (BFS y DFS).
- `src/utils.py`: Funciones de apoyo para medir rendimiento y formatear la salida en pantalla.
- `main.py`: Punto principal de ejecución donde se orquestarán los componentes anteriores.

## 2. Definición Detallada de Clases y Funciones

### 2.1 Módulo `state.py`
**Clase:** `State`
- **Atributos:**
  - `missionaries_left` (int): Misioneros en la orilla izquierda (0 a 3).
  - `cannibals_left` (int): Caníbales en la orilla izquierda (0 a 3).
  - `boat_is_on_left_bank` (bool): `True` si el bote está en la izquierda, `False` si está a la derecha.
  - `parent_state` (State | None): Apuntador al estado previo que generó el actual (útil para retroceder y sacar la ruta de solución).
  - `action_taken` (str): Descripción de la acción que se tomó para llegar aquí (ej: "Move 2 Missionaries to the Right").

- **Métodos:**
  - `__init__(self, missionaries_left, cannibals_left, boat_is_on_left_bank, parent_state=None, action_taken=None)`: Constructor para inicializar.
  - `is_valid_state(self) -> bool`: Comprueba las siguientes reglas críticas:
      - 0 <= `missionaries_left` <= 3 y 0 <= `cannibals_left` <= 3.
      - En la orilla izquierda: Si `missionaries_left` > 0, `missionaries_left >= cannibals_left`.
      - En la orilla derecha: Si `missionaries_right` > 0, `missionaries_right >= cannibals_right` (donde `missionaries_right = 3 - missionaries_left` y `cannibals_right = 3 - cannibals_left`).
  - `is_goal_state(self) -> bool`: Retorna `True` si `missionaries_left == 0`, `cannibals_left == 0` y `boat_is_on_left_bank == False`.
  - `generate_successors(self) -> list[State]`: Evalúa los 5 movimientos posibles de embarcación (1M, 1C, 2M, 2C, 1M1C) considerando en qué orilla está el bote. Retorna una lista de nuevos objetos `State` que sean completamente válidos (`is_valid_state() == True`).
  - Métodos especiales (dunder methods) para comparación y hashing (fundamental para evitar ciclos en las búsquedas):
    - `__eq__(self, other)`: Compara el estado físico sin importar la profundidad (`missionaries_left`, `cannibals_left`, `boat_is_on_left_bank`).
    - `__hash__(self)`: Genera un hash del estado `(self.missionaries_left, self.cannibals_left, self.boat_is_on_left_bank)`.

### 2.2 Módulo `algorithms.py`
Se sugiere desacoplar la lógica de búsqueda para que retorne dos valores: El objeto `State` final que llegó a la meta (a partir del cual rastreamos el path usando su apuntador `parent_state`) o `None` en caso de fallar, y en segundo lugar la cuenta de nodos visitados.

**Funciones:**
- `breadth_first_search(initial_state: State) -> tuple[State | None, int]`:
  - Utilizará `collections.deque` como frontera o estructura de datos tipo cola (QUEUE) (FIFO).
  - Extrae el primer elemento en espera; si es meta procede a salir; si no, obtiene sus sucesores válidos y los inserta al final.
  - Requiere utilizar un `set()` llamado `explored_states` para no repetir estados.

- `depth_first_search(initial_state: State) -> tuple[State | None, int]`:
  - Utilizará una lista estándar nativa de Python `[]` como estructura de datos tipo pila (LIFO).
  - Extrae el último elemento apilado (usando `.pop()`), revisa si es meta, en caso negativo obtiene sucesores y los mete a la lista.
  - Igualmente, requiere un `set()` llamado `explored_states`.

### 2.3 Módulo `utils.py`
- `reconstruct_solution_path(final_state: State) -> list[str]`: Itera hacia atrás a través del atributo `parent_state` recopilando los strings en `action_taken` y reordenando la lista para imprimir los pasos con un formato desde el inicio hasta la victoria.
- `measure_execution_performance(algorithm_function, initial_state)`: Un "wrapper" programático que:
  - Inicializa `tracemalloc.start()` y `start_time = time.perf_counter()`.
  - Corre el algoritmo inyectado: `algorithm_function(initial_state)`.
  - Finaliza los contadores, calcula diferencias de tiempo y procesador para imprimir un resumen estructurado y detallado para la consola del usuario.

## 3. Patrones de Diseño Empleados
- **Representación Inmutable y Limpia**: Los estados (`State`) generarán nuevos clones con las variaciones alteradas, impidiendo estropear un padre procesado por una modificación accidental.
- **Separación de Responsabilidades (SoC)**: El programa divide drásticamente las responsabilidades asegurando que el estado propio no sabe sobre tipos de búsqueda (BFS), y los algoritmos no necesitan saber imprimir resultados.

## 4. Orquestación Principal (`main.py`)
El punto de entrada constará de:
1. Instanciar el estado base `initial_state = State(missionaries_left=3, cannibals_left=3, boat_is_on_left_bank=True)`.
2. Lanzar en consola: `"--- Ejecutando Búsqueda en Amplitud (BFS) ---"`.
3. Invocar al utilitario analítico: `measure_execution_performance(breadth_first_search, initial_state)`.
4. Lanzar en consola: `"--- Ejecutando Búsqueda en Profundidad (DFS) ---"`.
5. Invocar al utilitario analítico: `measure_execution_performance(depth_first_search, initial_state)`.
