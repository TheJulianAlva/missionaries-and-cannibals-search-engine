"""Define la clase State que representa una configuración del problema.

Representación del Estado:
    missionaries_left (int): Número de misioneros en la orilla izquierda (0-3).
    cannibals_left (int): Número de caníbales en la orilla izquierda (0-3).
    boat_is_on_left_bank (bool): True si el bote está en la orilla izquierda.
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
    """Representa una configuración (nodo) en el espacio de búsqueda.

    Attributes:
        missionaries_left (int): Número de misioneros en la orilla izquierda.
        cannibals_left (int): Número de caníbales en la orilla izquierda.
        boat_is_on_left_bank (bool): True si el bote está en la orilla izquierda.
        parent_state (State | None): Estado que generó este, o None si es el inicial.
        action_taken (str | None): Descripción de la acción que llevó a este estado.
    """

    def __init__(
        self,
        missionaries_left: int,
        cannibals_left: int,
        boat_is_on_left_bank: bool,
        parent_state: State | None = None,
        action_taken: str | None = None,
    ) -> None:
        """Inicializa un nuevo estado.

        Args:
            missionaries_left (int): Número de misioneros en la orilla izquierda.
            cannibals_left (int): Número de caníbales en la orilla izquierda.
            boat_is_on_left_bank (bool): True si el bote está en la orilla izquierda.
            parent_state (State | None, optional): El estado que generó este (para
                reconstrucción de ruta). Defaults to None.
            action_taken (str | None, optional): Descripción legible de cómo se llegó
                a este estado. Defaults to None.
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
        """Verifica si este estado satisface las restricciones del problema.

        Las restricciones son:
        - Los conteos deben estar dentro de los límites [0, TOTAL].
        - En la orilla izquierda: misioneros >= caníbales (si hay misioneros).
        - En la orilla derecha: misioneros >= caníbales (si hay misioneros).

        Returns:
            bool: True si el estado es válido, False en caso contrario.
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
        """Verifica si este estado es el estado meta.

        Returns:
            bool: True si todos cruzaron a la orilla derecha, False en caso contrario.
        """
        return (
            self.missionaries_left == 0
            and self.cannibals_left == 0
            and not self.boat_is_on_left_bank
        )

    def generate_successors(self) -> list[State]:
        """Genera todos los estados sucesores válidos desde el estado actual.

        Returns:
            list[State]: Una lista de objetos State válidos alcanzables desde
                este estado.
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
