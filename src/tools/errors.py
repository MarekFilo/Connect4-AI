class InvalidMoveError(Exception):
    """Custom exception for an invalid move in Connect4."""

    def __init__(self, column: int):
        self.column = column
        super().__init__(f"Invalid move: Column {column} is already full.")
