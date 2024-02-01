class InvalidMoveError(Exception):
    """
    Exception raised when an invalid move is made in the Connect 4 game.

    Attributes:
        column (int): The column number of the invalid move.
    """

    def __init__(self, column: int):
        self.column = column
        super().__init__(f"Invalid move: Column {column + 1} is already full.")


class PlayerWin(Exception):
    """
    Exception raised when a player wins the game.

    Attributes:
        player_identifier (int): The identifier of the winning player.
    """

    def __init__(self, player_identifier: int):
        super().__init__(f"Player {player_identifier} won!")


class GameDraw(Exception):
    """Custom exception for a draw in Connect4.

    This exception is raised when the game ends in a draw, indicating that no player has won.
    """

    def __init__(self):
        super().__init__("Draw!")
