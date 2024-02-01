class InvalidMoveError(Exception):
    """Custom exception for an invalid move in Connect4."""

    def __init__(self, column: int):
        self.column = column
        super().__init__(f"Invalid move: Column {column + 1} is already full.")


class PlayerWin(Exception):
    """
    Exception raised when a player wins the game.

    Args:
        message (str): The error message associated with the exception.
    """

    def __init__(self, player_identifier: int):
        super().__init__(f"Player {player_identifier} won!")


class GameDraw(Exception):
    """Custom exception for a draw in Connect4."""

    def __init__(self):
        super().__init__("Draw!")
