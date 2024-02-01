import itertools
import numpy as np
from tools.errors import InvalidMoveError
from .player import Player
from typing import Optional


class Connect4:
    """
    Connect4 class represents the Connect 4 game.

    Attributes:
        board (numpy.ndarray): The game board represented as a 2D numpy array.
        num_of_moves (int): The number of moves made in the game.
        player_one (Player): The first player.
        player_two (Player): The second player.
        current_player (Player): The current player making a move.

    Methods:
        __init__(): Initializes the Connect4 object.
        _clear_board(): Clears the game board and resets the number of moves.
        rematch(): Starts a new game by clearing the board and choosing a new starting player.
        make_move(column: int) -> Optional[str]: Makes a move by placing a disc in the specified column.
        _switch_player(): Switches the current player.
        _is_board_full() -> bool: Checks if the game board is full.
        _get_next_row(column: int) -> int: Gets the next available row in the specified column.
        _is_valid_move(column: int) -> bool: Checks if the move is valid in the specified column.
        _choose_starting_player(players: [Player]) -> Player: Chooses a random starting player.
        _is_winning_move(player: Player) -> bool: Checks if the current player has won the game.
        _initiate_terminal_game() -> Player: Starts a terminal-based game.
    """

    def __init__(self):
        """
        Initializes the Connect4 object.

        The game board is represented as a 2D numpy array with dimensions 6x7.
        The number of moves is set to 0.
        Two players are created using the Player class.
        The starting player is chosen randomly.
        """
        self.board: np.ndarray = np.zeros((6, 7), dtype=int)
        self.num_of_moves: int = 0

        self.player_one: Player = Player(1)
        self.player_two: Player = Player(2)

        self.current_player: Player = self._choose_starting_player(
            [self.player_one, self.player_two]
        )

    def _clear_board(self):
        """
        Clears the game board and resets the number of moves.
        """
        self.board = np.zeros((6, 7), dtype=int)
        self.num_of_moves = 0

    def rematch(self):
        """
        Starts a new game by clearing the board and choosing a new starting player.
        """
        self._clear_board()
        self.current_player: Player = self._choose_starting_player(
            [self.player_one, self.player_two]
        )

    def make_move(self, column: int) -> Optional[str]:
        """
        Makes a move by placing a disc in the specified column.

        Args:
            column (int): The column where the disc should be placed.

        Raises:
            InvalidMoveError: If the move is invalid.

        Returns:
            Optional[str]: The result of the move (e.g., "Player 1 wins!", "Draw!").
        """
        if not self._is_valid_move(column):
            raise InvalidMoveError(column)

        row = self._get_next_row(column)
        self.board[row][column] = self.current_player.identifier
        self.num_of_moves += 1

        if self._is_winning_move(self.current_player):
            self.current_player.wins += 1
            return f"Player {self.current_player.identifier} wins!"

        if self._is_board_full():
            return "Draw!"

        self._switch_player()

    def _switch_player(self):
        """
        Switches the current player.
        """
        self.current_player = (
            self.player_one
            if self.current_player == self.player_two
            else self.player_two
        )

    def _is_board_full(self) -> bool:
        """
        Checks if the game board is full.

        Returns:
            bool: True if the board is full, False otherwise.
        """
        return self.num_of_moves == 42

    def board_layout(self) -> np.ndarray:
        """
        Returns the game board layout.

        Returns:
            np.ndarray: The game board layout.
        """
        return self.board

    def _get_next_row(self, column: int) -> int:
        """
        Gets the next available row in the specified column.

        Args:
            column (int): The column to check.

        Returns:
            int: The next available row in the column.
        """
        for row in range(5, -1, -1):
            if self.board[row][column] == 0:
                return row

    def _is_valid_move(self, column: int) -> bool:
        """
        Checks if the move is valid in the specified column.

        Args:
            column (int): The column to check.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        return self.board[0][column] == 0

    def _choose_starting_player(self, players: [Player]) -> Player:
        """
        Chooses a random starting player.

        Args:
            players ([Player]): The list of players.

        Returns:
            Player: The randomly chosen starting player.
        """
        return np.random.choice(players)

    def _is_winning_move(self, player: Player) -> bool:
        """
        Checks if the current player has won the game.

        Args:
            player (Player): The current player.

        Returns:
            bool: True if the current player has won, False otherwise.
        """
        # Horizontal check
        for row, col in itertools.product(range(6), range(4)):
            if all(self.board[row][col + i] == player.identifier for i in range(4)):
                return True

        # Vertical check
        for row, col in itertools.product(range(3), range(7)):
            if all(self.board[row + i][col] == player.identifier for i in range(4)):
                return True

        # Diagonal check (from bottom-left to top-right)
        for row, col in itertools.product(range(3, 6), range(4)):
            if all(self.board[row - i][col + i] == player.identifier for i in range(4)):
                return True

        return any(
            all(self.board[row + i][col + i] == player.identifier for i in range(4))
            for row, col in itertools.product(range(3), range(4))
        )

    def _initiate_terminal_game(self) -> Optional[Player]:
        """
        Starts a terminal-based game.

        Returns:
            Player: The winning player, if any.
        """
        while not self._is_board_full():
            column = (
                int(
                    input(f"Player {self.current_player.identifier}, choose a column: ")
                )
                - 1
            )

            try:
                self.make_move(column)

                print(self.board)

                if self._is_winning_move(self.current_player):
                    print(f"Player {self.current_player.identifier} wins!")
                    return self.current_player

            except ValueError as e:
                print(f"Error: {e}")

    def __str__(self) -> str:
        """
        Returns a string representation of the Connect4 object.

        Returns:
            str: The string representation of the object.
        """
        return str(self.board)
