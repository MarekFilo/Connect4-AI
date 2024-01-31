class Player:
    """
    Represents a player in the Connect4 game.

    Attributes:
        number (int): The identifier of the player.
        wins (int): The number of wins the player has.
    """

    def __init__(self, identifier: int):
        self.number = identifier
        self.wins = 0
