import itertools
import numpy as np
from tools.errors import InvalidMoveError, PlayerWin, GameDraw
from .player import Player
from typing import Optional


class Connect4:
    """
    Represents the Connect4 game.

    Attributes:
    - rows (int): The number of rows on the game board.
    - columns (int): The number of columns on the game board.
    - _board (np.ndarray): The game board represented as a NumPy array.
    - _num_of_moves (int): The number of moves made in the game.
    - _max_moves (int): The maximum number of moves allowed in the game.
    - game_state (int): The current state of the game (0 for ongoing, 1 for finished).
    - Player_one (Player): The first player in the game.
    - Player_two (Player): The second player in the game.
    - current_player (Player): The player who is currently making a move.

    Methods:
    - clear_board(): Clears the game board and resets the number of moves to zero.
    - rematch(): Resets the game state, clears the board, and chooses a new starting player.
    - make_move(column: int) -> Optional[Exception]: Makes a move in the specified column.
    - _switch_player(): Switches the current player to the other player.
    - _is_board_full() -> bool: Checks if the game board is full.
    - board_layout() -> np.ndarray: Returns the current layout of the game board.
    - _get_next_row(column: int) -> int: Returns the next available row in the specified column.
    - _is_valid_move(column: int) -> bool: Checks if the specified column is a valid move.
    - choose_starting_player(players: [Player]) -> Player: Chooses a random player as the starting player.
    - _is_winning_move(player: Player) -> bool: Checks if the current move is a winning move for the player.
    - __str__() -> str: Returns a string representation of the game board.
    """

    def __init__(self):
        """
        Initializes a Connect4 game instance.

        Attributes:
        - rows (int): The number of rows on the game board.
        - columns (int): The number of columns on the game board.
        - _board (np.ndarray): The game board represented as a NumPy array.
        - _num_of_moves (int): The current number of moves made in the game.
        - _max_moves (int): The maximum number of moves allowed in the game.
        - game_state (int): The current state of the game.
        - Player_one (Player): The first player in the game.
        - Player_two (Player): The second player in the game.
        - current_player (Player): The player who is currently making a move.
        """

        self.rows: int = 6
        self.columns: int = 7
        self._board: np.ndarray = np.zeros((self.rows, self.columns), dtype=int)
        self._num_of_moves: int = 0
        self._max_moves: int = self.rows * self.columns

        self.game_state: int = 0

        self.Player_one: Player = Player(1, "#70D6FF")
        self.Player_two: Player = Player(2, "#FF70A6")

        self.current_player: Player = self.choose_starting_player(
            [self.Player_one, self.Player_two]
        )

    def clear_board(self):
        """
        Clears the game board and resets the number of moves to zero.
        """
        self._board = np.zeros((self.rows, self.columns), dtype=int)
        self._num_of_moves = 0

    def rematch(self):
        """
        Resets the game state and clears the board for a rematch.
        The starting player for the rematch is chosen randomly from the two players.

        Parameters:
            None

        Returns:
            None
        """
        self.game_state = 0
        self.clear_board()
        self.current_player: Player = self.choose_starting_player(
            [self.Player_one, self.Player_two]
        )

    def make_move(self, column: int) -> Optional[Exception]:
        """
        Makes a move in the Connect4 game by placing a token in the specified column.

        Args:
            column (int): The column number where the token should be placed.

        Returns:
            Optional[Exception]: Returns an exception if the move results in a win or draw, otherwise returns None.
        """

        if self.game_state != 0:
            return

        if self._is_valid_move(column):
            self.row = self._get_next_row(column)
            self._board[self.row][column] = self.current_player.identifier
            self._num_of_moves += 1

            if self._is_winning_move(self.current_player):
                self.current_player.wins += 1
                self.win_message = f"Player {self.current_player.identifier} wins!"
                self.game_state = 1
                raise PlayerWin(self.current_player.identifier)

            if self._is_board_full():
                self.game_state = 1
                raise GameDraw()

            self._switch_player()

    def _switch_player(self):
        """
        Switches the current player to the other player.
        """
        self.current_player
        self.current_player = (
            self.Player_one
            if self.current_player == self.Player_two
            else self.Player_two
        )

    def _is_board_full(self) -> bool:
        """
        Check if the game board is full.

        Returns:
            bool: True if the board is full, False otherwise.
        """
        return self._num_of_moves == self._max_moves

    def board_layout(self) -> np.ndarray:
        """
        Returns the current layout of the game board.

        Returns:
            np.ndarray: The current layout of the game board.
        """
        return self._board

    def _get_next_row(self, column: int) -> int:
        """
        Get the next available row in the specified column.

        Args:
            column (int): The column index.

        Returns:
            int: The row index of the next available row in the column.
        """
        for row in range(5, -1, -1):
            if self._board[row][column] == 0:
                return row

    def _is_valid_move(self, column: int) -> bool:
        """
        Check if a move is valid in the specified column.

        Args:
            column (int): The column to check.

        Returns:
            bool: True if the move is valid, False otherwise.

        Raises:
            InvalidMoveError: If the column is already full.
        """
        if self._board[0][column] == 0:
            return True
        else:
            raise InvalidMoveError(column)

    def choose_starting_player(self, players: [Player]) -> Player:
        """
        Randomly selects a player from the given list of players to be the starting player.

        Args:
            players (list): A list of Player objects representing the players in the game.

        Returns:
            Player: The randomly selected starting player.
        """
        return np.random.choice(players)

    def _is_winning_move(self, player: Player) -> bool:
        """
        Check if the specified player has made a winning move on the game board.

        Args:
            player (Player): The player to check for a winning move.

        Returns:
            bool: True if the player has made a winning move, False otherwise.
        """
        # Horizontal check
        for row, col in itertools.product(range(6), range(4)):
            if all(self._board[row][col + i] == player.identifier for i in range(4)):
                return True

        # Vertical check
        for row, col in itertools.product(range(3), range(7)):
            if all(self._board[row + i][col] == player.identifier for i in range(4)):
                return True

        # Diagonal check (from bottom-left to top-right)
        for row, col in itertools.product(range(3, 6), range(4)):
            if all(
                self._board[row - i][col + i] == player.identifier for i in range(4)
            ):
                return True

        # Diagonal check (from top-left to bottom-right)
        for row, col in itertools.product(range(3), range(4)):
            if all(
                self._board[row + i][col + i] == player.identifier for i in range(4)
            ):
                return True

    def __str__(self) -> str:
        """
        Returns a string representation of the Connect4 game board.

        Returns:
            str: The string representation of the game board.
        """
        return str(self._board)
