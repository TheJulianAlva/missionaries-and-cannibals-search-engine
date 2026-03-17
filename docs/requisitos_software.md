# Requisitos del Software

## Requisitos Funcionales
1. **Representación del Espacio de Estados**: El sistema debe proveer una estructura de datos o clase que modele con precisión la cantidad de misioneros, caníbales y la posición del bote en cualquiera de las orillas del río en un momento dado.
2. **Generación de Sucesores**: El sistema debe calcular todos los movimientos válidos desde un estado particular, comprobando que se cumpla la restricción principal (los caníbales no deben superar en número a los misioneros en ninguna orilla).
3. **Búsqueda en Amplitud (BFS)**: El sistema debe implementar un algoritmo de Búsqueda en Amplitud para encontrar la ruta óptima desde el estado inicial hasta el estado meta.
4. **Búsqueda en Profundidad (DFS)**: El sistema debe implementar un algoritmo de Búsqueda en Profundidad para encontrar una solución desde el estado inicial hasta la meta.
5. **Reporte de Resultados**: Al finalizar las búsquedas, el sistema debe imprimir en pantalla las siguientes métricas comparativas para cada algoritmo:
   - **Camino de Solución**: La secuencia completa de acciones ejecutadas para llegar desde el inicio hasta el objetivo.
   - **Nodos Explorados**: La cantidad total de nodos visitados antes de encontrar la solución.
   - **Tiempo de Ejecución**: El tiempo en segundos (aproximado) que tardó cada algoritmo.
   - **Memoria Utilizada**: La memoria reservada (aproximada) que requirió el proceso de búsqueda en cada caso.

## Requisitos No Funcionales
1. **Lenguaje Comercial**: El programa deberá ser codificado enteramente en Python.
2. **Arquitectura Limpia**: El código debe estar organizado en diferentes módulos (`state.py`, `algorithms.py`, etc.) respetando buenas prácticas de Ingeniería de Software.
3. **Mantenibilidad y Legibilidad**: Se deben incluir docstrings, tipado dinámico y comentarios claros que faciliten la lectura y el seguimiento de la lógica del código.
4. **Eficiencia**: Los algoritmos deben implementar mecanismos de control de estados visitados (como un conjunto `explored_states`) para prevenir ciclos infinitos y el re-análisis de nodos repetidos.
