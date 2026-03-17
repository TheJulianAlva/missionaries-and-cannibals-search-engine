# 🛶 Misioneros y Caníbales - Búsqueda en Inteligencia Artificial

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Este repositorio contiene una implementación eficiente en Python para resolver el clásico problema de Inteligencia Artificial de ***"Misioneros y Caníbales"***. El proyecto emplea algoritmos de búsqueda no informada **(Amplitud y Profundidad)** para explorar el espacio de estados de forma óptima y visual.

---

## 📖 Descripción del Problema

Tres **misioneros** y tres **caníbales** se encuentran en la orilla izquierda de un río. Tienen un bote que puede transportar como máximo a dos personas a la vez y como mínimo a una. 
El objetivo es que las seis personas crucen a la orilla derecha del río.

### ⚠️ Restricción Principal
En ningún momento, en ninguna de las orillas del río, el número de caníbales puede superar al número de misioneros a menos que no haya misioneros presentes en esa orilla (si hay cero misioneros, están a salvo). Si en una orilla los caníbales superan en número a los misioneros, se los comerán y el estado será inválido (fin del juego). 
> **Nota:** El bote en tránsito se cuenta junto con la orilla de la que partió hasta que llegue a la otra.

---

## 🚀 Características del Proyecto

1. **Representación Estricta Orientada a Objetos:** El problema entero está modelado usando una clase `State` aislada e inmutable que se valida a sí misma basándose en el encapsulamiento.
2. **Búsqueda en Amplitud (BFS):** Encuentra la ruta más corta garantizada (óptima) explorando nivel por nivel mediante una cola FIFO (`collections.deque`).
3. **Búsqueda en Profundidad (DFS):** Encuentra una ruta válida utilizando un enfoque iterativo basado en una pila LIFO (usando arrays `list` nativos) para conservar memoria y evitar el límite de recursión.
4. **Visualización ASCII:** Incluye un renderizador en consola que dibuja cada paso del cruce del río de manera intuitiva y amigable.
5. **Métricas de Rendimiento en Tiempo Real:** Analiza el número de nodos explorados, el tiempo real de ejecución de la CPU (`time.perf_counter()`) y el consumo máximo de memoria RAM (`tracemalloc`).

---

## ⚙️ Arquitectura del Software

```text
motor-busqueda-misioneros-y-canibales/
│
├── src/                       # Código fuente del sistema
│   ├── __init__.py            
│   ├── state.py               # Clase State (atributos físicos, cálculo de movimientos y validación)
│   ├── algorithms.py          # Implementación matemática del DFS y BFS
│   └── utils.py               # Lógica de impresión ASCII y benchmarking (patrón Decorador adaptado)
│
└── main.py                    # Punto de Entrada. Ejecuta algoritmos e imprime resultados comparativos.
```

---

## 📊 Análisis Comparativo: BFS vs DFS

Dado que las fuertes restricciones del juego descartan la mayoría de las permutaciones numéricas, el espacio de estados reales matemáticos es bastante reducido. 

Tras las pruebas de ejecución iterando desde el nodo inicial (3M, 3C, Bote en Izquierda) hasta la meta (0M, 0C, Bote en Derecha), se obtienen las siguientes métricas promedio:

| Algoritmo           | Optimidad Garantizada | Nodos Explorados | Pasos en la Solución | Memoria Max (KB) | Tiempo (ms) |
| :------------------ | :-------------------: | :--------------: | :------------------: | :--------------: | :---------: |
| **BFS (Cola FIFO)** |         ✅ Sí          |       ~15        |          11          |      ~6.48       |    ~0.32    |
| **DFS (Pila LIFO)** |         ❌ No          |       ~12        |          11          |      ~5.11       |    ~0.28    |

### Conclusiones de Rendimiento
- **Búsqueda en Amplitud (BFS):** Ocupa ligeramente más memoria porque la "Frontera" debe mantener simultáneamente todas las "ramas" abiertas del nivel actual antes de pasar al siguiente. Sin embargo, su uso es estrictamente necesario en este problema si se desea encontrar la **ruta perfecta y matemática** (11 pasos).
- **Búsqueda en Profundidad (DFS):** Resulta usar menos memoria ya que una pila LIFO solo necesita recordar su linaje directo hacia abajo y sus nodos hermanos inmediatos. Exploró menos nodos de forma casual por la dirección del diseño de expansión, pero en espacios de estados más grandes (sin límite), DFS podría perderse en rutas infinitas no óptimas.

En resumen: **BFS** es la mejor opción para la arquitectura cerrada del problema Misioneros y Caníbales.

---

## 💻 Instalación y Uso

### Prerrequisitos
*   Python 3.9 o superior instalado en el sistema.

### Pasos de Ejecución
1. Clona este repositorio o descarga la carpeta a tu sistema local.
2. Abre tu terminal.
3. Navega al directorio raíz del proyecto:
   ```bash
   cd motor-busqueda-misioneros-y-canibales
   ```
4. Ejecuta el script principal:
   ```bash
   python main.py
   ```
