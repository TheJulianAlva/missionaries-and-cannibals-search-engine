# Reglas del Juego: Misioneros y Caníbales

## Descripción del Problema
El problema de los Misioneros y Caníbales es un clásico problema de búsqueda en Inteligencia Artificial que involucra cruzar un río bajo ciertas restricciones.

### Escenario
Tres misioneros y tres caníbales se encuentran en la orilla izquierda de un río. Tienen un bote que puede transportar como máximo a dos personas a la vez y como mínimo a una. El objetivo es que las seis personas crucen a la orilla derecha del río.

### Restricción Principal
En ningún momento, en ninguna de las orillas del río, el número de caníbales puede superar al número de misioneros a menos que no haya misioneros presentes en esa orilla (si hay cero misioneros, están a salvo). Si en una orilla los caníbales superan en número a los misioneros, se los comerán y el estado será inválido (fin del juego). El bote en tránsito se cuenta junto con la orilla de la que partió hasta que llegue a la otra.

### Movimientos Posibles
El bote no puede cruzar el río vacío; debe llevar al menos a una persona para operarlo.
Las combinaciones válidas de pasajeros para cruzar en el bote son:
- 1 Misionero
- 1 Caníbal
- 2 Misioneros
- 2 Caníbales
- 1 Misionero y 1 Caníbal

### Estado Inicial
- **Orilla Izquierda**: 3 Misioneros, 3 Caníbales, 1 Bote.
- **Orilla Derecha**: 0 Misioneros, 0 Caníbales, 0 Botes.

### Estado Objetivo (Meta)
- **Orilla Izquierda**: 0 Misioneros, 0 Caníbales, 0 Botes.
- **Orilla Derecha**: 3 Misioneros, 3 Caníbales, 1 Bote.
