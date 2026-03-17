"""
Módulo: state.py
Descripción: Define la clase State que representa una configuración
             del problema de Misioneros y Caníbales.

Representación del Estado:
    - missionaries_left: número de misioneros en la orilla izquierda (0-3)
    - cannibals_left:   número de caníbales en la orilla izquierda (0-3)
    - boat_is_on_left_bank: True si el bote está en la orilla izquierda
"""

from __future__ import annotations

# Todas las combinaciones posibles de (misioneros, caníbales) que pueden viajar en el bote.
BOAT_MOVES: list[tuple[int, int]] = [
    (1, 0), # 1 misionero
    (0, 1), # 1 caníbal
    (2, 0), # 2 misioneros
    (0, 2), # 2 caníbales
    (1, 1), # 1 misionero y 1 caníbal
]

TOTAL_MISSIONARIES: int = 3
TOTAL_CANNIBALS: int = 3


class State:
    """
    Representa una única configuración (nodo) en el espacio de búsqueda
    del problema.
    """

    def __init__(
        self,
        missionaries_left: int,
        cannibals_left: int,
        boat_is_on_left_bank: bool,
        parent_state: State | None = None,
        action_taken: str | None = None,
    ) -> None:
        """
        Inicializa un nuevo estado.

        Args:
            missionaries_left: Número de misioneros en la orilla izquierda.
            cannibals_left: Número de caníbales en la orilla izquierda.
            boat_is_on_left_bank: True si el bote está actualmente en la orilla izquierda.
            parent_state: El estado que generó este (para reconstrucción de ruta).
            action_taken: Descripción legible de cómo se llegó a este estado.
        """
        self.missionaries_left: int = missionaries_left
        self.cannibals_left: int = cannibals_left
        self.boat_is_on_left_bank: bool = boat_is_on_left_bank
        self.parent_state: State | None = parent_state
        self.action_taken: str | None = action_taken

    @property
    def missionaries_right(self) -> int:
        """Número de misioneros en la orilla derecha."""
        return TOTAL_MISSIONARIES - self.missionaries_left

    @property
    def cannibals_right(self) -> int:
        """Número de caníbales en la orilla derecha."""
        return TOTAL_CANNIBALS - self.cannibals_left

    def is_valid_state(self) -> bool:
        """
        Retorna True si este estado satisface todas las restricciones del problema:
          - Los conteos deben estar dentro de los límites [0, TOTAL].
          - En la orilla izquierda: misioneros >= caníbales (a menos que no haya misioneros).
          - En la orilla derecha: misioneros >= caníbales (a menos que no haya misioneros).
        """
        # Verificación de límites
        if not (0 <= self.missionaries_left <= TOTAL_MISSIONARIES):
            return False
        if not (0 <= self.cannibals_left <= TOTAL_CANNIBALS):
            return False

        # Orilla izquierda
        if self.missionaries_left > 0 and self.cannibals_left > self.missionaries_left:
            return False

        # Orilla derecha
        if self.missionaries_right > 0 and self.cannibals_right > self.missionaries_right:
            return False

        return True

    def is_goal_state(self) -> bool:
        """
        Retorna True cuando todos los misioneros y caníbales han cruzado
        a la orilla derecha y el bote también está en la orilla derecha.
        """
        return (
            self.missionaries_left == 0
            and self.cannibals_left == 0
            and not self.boat_is_on_left_bank
        )

    def generate_successors(self) -> list[State]:
        """
        Genera todos los estados sucesores válidos desde el estado actual.

        Para cada movimiento posible del bote, el bote cruza desde su orilla
        actual a la opuesta llevando a los pasajeros.
        Solo se retornan los estados que pasan is_valid_state().

        Returns:
            Una lista de objetos State válidos alcanzables desde este estado.
        """
        successors: list[State] = []

        for missionaries_on_boat, cannibals_on_boat in BOAT_MOVES:

            if self.boat_is_on_left_bank:
                # Moviéndose de izquierda a derecha
                new_missionaries_left = self.missionaries_left - missionaries_on_boat
                new_cannibals_left = self.cannibals_left - cannibals_on_boat
                direction = "→ Derecha"
            else:
                # Moviéndose de derecha a izquierda
                new_missionaries_left = self.missionaries_left + missionaries_on_boat
                new_cannibals_left = self.cannibals_left + cannibals_on_boat
                direction = "← Izquierda"

            action_description = (
                f"Mover {missionaries_on_boat} MISIONEROS y {cannibals_on_boat} CANIBALES {direction}"
            )

            candidate = State(
                missionaries_left=new_missionaries_left,
                cannibals_left=new_cannibals_left,
                boat_is_on_left_bank=not self.boat_is_on_left_bank,
                parent_state=self,
                action_taken=action_description,
            )

            if candidate.is_valid_state():
                successors.append(candidate)

        return successors

    # Métodos dunder para hashing e igualdad
    # Requeridos para almacenar objetos State en conjuntos (explored_states).

    def __eq__(self, other: object) -> bool:
        """Dos estados son iguales cuando comparten la misma configuración física."""
        if not isinstance(other, State):
            return False
        return (
            self.missionaries_left == other.missionaries_left
            and self.cannibals_left == other.cannibals_left
            and self.boat_is_on_left_bank == other.boat_is_on_left_bank
        )

    def __hash__(self) -> int:
        """Hash basado únicamente en la configuración física."""
        return hash((self.missionaries_left, self.cannibals_left, self.boat_is_on_left_bank))

    def __repr__(self) -> str:
        """Representación legible para depuración."""
        side = "Izquierda" if self.boat_is_on_left_bank else "Derecha"
        return (
            f"State(izq=[{self.missionaries_left} M, {self.cannibals_left} C], "
            f"      der=[{self.missionaries_right} M, {self.cannibals_right} C], "
            f"      bote={side})"
        )
