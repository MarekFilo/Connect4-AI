class InvalidMoveError(Exception):
    """Custom exception for an invalid move in Connect4."""

    def __init__(self, column: int):
        self.column = column
        super().__init__(f"Invalid move: Column {column + 1} is already full.")


class GameEndError(Exception):
    """Custom exception for the end of a Connect4 game."""

    def __init__(self, message: str):
        super().__init__(message)
