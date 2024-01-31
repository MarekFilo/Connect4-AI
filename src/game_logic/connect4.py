import numpy as np


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


class Connect4:
    """
    Represents a Connect4 game.

    The Connect4 game is played on a 6x7 board with two players.
    Players take turns dropping colored discs into the columns of the board.
    The goal is to connect four discs of the same color in a row, column, or diagonal.

    Attributes:
        player_one (Player): The first player.
        player_two (Player): The second player.
        board (numpy.ndarray): The game board represented as a 6x7 numpy array.
        num_of_moves (int): The number of moves made in the game.
    """

    def __init__(self):
        """
        Initializes a new instance of the Connect4 game.

        The game starts with an empty board and two players, player_one and player_two.
        The board is represented as a 6x7 numpy array filled with zeros.
        The number of moves is initially set to 0.
        """
        self.player_one = Player(1)
        self.player_two = Player(2)
        self.board = np.zeros((6, 7), dtype=int)
        self.num_of_moves = 0

    def clear_board(self):
        """
        Clears the game board by setting all positions to 0.
        Resets the number of moves to 0.
        """
        self.board = np.zeros((6, 7), dtype=int)
        self.num_of_moves = 0

    def make_move(self, column: int, player: Player):
        """
        Makes a move in the specified column for the given player.

        Args:
            column (int): The column number where the move is to be made.
            player (Player): The player making the move.

        Raises:
            ValueError: If the specified column is already full.

        Returns:
            None
        """
        if not self.is_valid_move(column):
            raise ValueError(f"Column {column} is already full.")

        row = self.get_next_row(column)
        self.board[row][column] = player.number
        self.num_of_moves += 1

    def is_board_full(self) -> bool:
        """
        Check if the game board is full.

        Returns:
            bool: True if the board is full, False otherwise.
        """
        return self.num_of_moves == 42

    def get_next_row(self, column: int) -> int:
        """
        Returns the next available row in the specified column.

        Args:
            column (int): The column index.

        Returns:
            int: The row index of the next available row in the column.
        """
        for row in range(5, -1, -1):
            if self.board[row][column] == 0:
                return row

    def is_valid_move(self, column: int) -> bool:
        """
        Check if a move is valid in the given column.

        Args:
            column (int): The column index to check.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        return self.board[0][column] == 0

    def starting_player(self, players: [Player]) -> Player:
        """
        Randomly selects and returns a player from the given list of players.

        Parameters:
            players (list): A list of Player objects representing the players.

        Returns:
            Player: The randomly selected player.
        """
        return np.random.choice(players)

    def is_winning_move(self, player: Player) -> bool:
        """
        Checks if the specified player has a winning move on the game board.

        Args:
            player (Player): The player to check for a winning move.

        Returns:
            bool: True if the player has a winning move, False otherwise.
        """

        # Horizontal check
        for row in range(6):
            for col in range(4):
                if all(self.board[row][col + i] == player.number for i in range(4)):
                    return True

        # Vertical check
        for row in range(3):
            for col in range(7):
                if all(self.board[row + i][col] == player.number for i in range(4)):
                    return True

        # Diagonal check (from bottom-left to top-right)
        for row in range(3, 6):
            for col in range(4):
                if all(self.board[row - i][col + i] == player.number for i in range(4)):
                    return True

        # Diagonal check (from top-left to bottom-right)
        for row in range(3):
            for col in range(4):
                if all(self.board[row + i][col + i] == player.number for i in range(4)):
                    return True

        return False

    def _initiate_terminal_game(self) -> Player:
        """
        Initiates a terminal-based Connect4 game.

        This method allows players to take turns making moves until the game is over.
        The current player is prompted to choose a column to make a move in.
        After each move, the board is printed and checked for a winning move.
        If a winning move is found, the game ends and the winning player is announced.

        Raises:
            ValueError: If an invalid column number is chosen.

        Returns:
            Player: The winning player, if there is one. Otherwise, None.
        """
        self.current_player = self.starting_player([self.player_one, self.player_two])

        while not self.is_board_full():
            column = (
                int(input(f"Player {self.current_player.number}, choose a column: "))
                - 1
            )

            try:
                self.make_move(column, self.current_player)

                print(self.board)

                if self.is_winning_move(self.current_player):
                    print(f"Player {self.current_player.number} wins!")
                    return self.current_player

                self.current_player = (
                    self.player_one
                    if self.current_player == self.player_two
                    else self.player_two
                )

            except ValueError as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    game = Connect4()
    print(game.board)
