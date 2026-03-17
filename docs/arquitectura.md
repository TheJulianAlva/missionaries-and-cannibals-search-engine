# Arquitectura del Proyecto

## Patrones de Diseño
Para este proyecto se utilizará una aproximación orientada a objetos sumado a un enfoque modular.
1. **Representación de Datos Oculta (Encapsulamiento)**: Se creará una abstracción `State` que maneja su propia validación (si es un estado válido donde no se comen a nadie) y provee métodos para ser comparado (para set/dict en Python).
2. **Strategy Pattern para Búsquedas (Implícito)**: Los algoritmos BFS y DFS se abstraerán bajo firmas de funciones idénticas en el módulo de `algorithms.py`, lo que permitirá intercambiarlos, correrlos y medirlos fácilmente dentro de una función iteradora genérica.

## Estructura de Archivos (Propuesta)
Se propone dividir el proyecto en los siguientes directorios y archivos para maximizar la legibilidad y mantenibilidad:

```text
motor-busqueda-misioneros-y-canibales/
│
├── docs/                      # Carpeta de documentación
│   ├── reglas_juego.md        # Funcionamiento del problema
│   ├── requisitos_software.md # Exigencias técnicas a cumplir
│   └── arquitectura.md        # Estructura del código
│
├── src/                       # Código fuente del sistema
│   ├── __init__.py            # Marca la carpeta modular 
│   ├── state.py               # Contiene la clase State (validación/movimiento)
│   ├── algorithms.py          # Implementaciones puras de BFS y DFS
│   └── utils.py               # Lógica de benchmarking de tiempo y memoria
│
├── main.py                    # Punto de Entrada. Ejecuta algoritmos y muestra salidas.
└── documento.md               # Documento escrito final para la entrega (Introducción, Desarrollo, Conclusión).
```

### Descripción de Componentes Clave
1. **Clase `State` (`src/state.py`)**:
   - Atributos por orilla: `missionaries_left`, `cannibals_left`, `boat_is_on_left_bank`. Los derechos se calculan con respecto al total global (3 M, 3 C).
   - Métodos: `is_valid_state()` (para checar la restricción), `is_goal_state()` (orilla derecha llena), `generate_successors()` (genera siguientes estados tras un viaje en bote).
   - Necesita implementar `__eq__` y `__hash__` para detectar estados repetidos en colecciones y no ciclar la búsqueda.
2. **Algoritmos (`src/algorithms.py`)**:
   - `breadth_first_search(initial_state)`: Hará uso de la estructura FIFO `collections.deque`.
   - `depth_first_search(initial_state)`: Hará uso de la estructura LIFO estandar de Python `list` en forma iterativa para evitar límites de recursión (aunque el espacio sea de 16 estados válidos aprox.).
3. **Herramientas de Medición (`src/utils.py`)**:
   - Contendrá una función que envolverá las llamadas a algoritmos, importando `time` (para el tiempo de CPU) y `tracemalloc` (para la memoria pico en Bytes).
