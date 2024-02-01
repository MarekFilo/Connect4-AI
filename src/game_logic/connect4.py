import itertools
import numpy as np
from tools.errors import InvalidMoveError, PlayerWin, GameDraw
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
        board_layout() -> np.ndarray: Returns the game board layout.
        _get_next_row(column: int) -> int: Gets the next available row in the specified column.
        _is_valid_move(column: int) -> bool: Checks if the move is valid in the specified column.
        _choose_starting_player(players: [Player]) -> Player: Chooses a random starting player.
        _is_winning_move(player: Player) -> bool: Checks if the current player has won the game.
        _initiate_terminal_game() -> Optional[Player]: Starts a terminal-based game.
    """

    def __init__(self):
        """
        Initializes the Connect4 object.

        The game board is represented as a 2D numpy array with dimensions 6x7.
        The number of moves is set to 0.
        Two players are created using the Player class.
        The starting player is chosen randomly.
        """
        self.rows: int = 6
        self.columns: int = 7
        self.board: np.ndarray = np.zeros((self.rows, self.columns), dtype=int)
        self.num_of_moves: int = 0
        self.max_moves: int = self.rows * self.columns

        self.game_state: int = 0

        self.player_one: Player = Player(1)
        self.player_two: Player = Player(2)

        self.current_player: Player = self._choose_starting_player(
            [self.player_one, self.player_two]
        )

    def _clear_board(self):
        """
        Clears the game board and resets the number of moves.
        """
        self.board = np.zeros((self.rows, self.columns), dtype=int)
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


        Returns:
            Optional[str]: The result of the move (e.g., "Player 1 wins!", "Draw!").
        """

        self._is_valid_move(column)
        self.row = self._get_next_row(column)
        self.board[self.row][column] = self.current_player.identifier
        self.num_of_moves += 1

        if self._is_winning_move(self.current_player):
            self.current_player.wins += 1
            self.win_message = f"Player {self.current_player.identifier} wins!"
            self.game_state = 1
            raise PlayerWin(self.current_player.identifier)

        if self._is_board_full():
            self.game_state = 1
            raise GameDraw()

    def switch_player(self):
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
        return self.num_of_moves == self.max_moves

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
        if self.board[0][column] == 0:
            return True
        else:
            raise InvalidMoveError(column)

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

        # Diagonal check (from top-left to bottom-right)
        for row, col in itertools.product(range(3), range(4)):
            if all(self.board[row + i][col + i] == player.identifier for i in range(4)):
                return True

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
                self.switch_player()
                print(self.board)

                if self._is_winning_move(self.current_player):
                    print(f"Player {self.current_player.identifier} wins!")
                    return self.current_player

            except InvalidMoveError as e:
                print(column)

    def __str__(self) -> str:
        """
        Returns a string representation of the Connect4 object.

        Returns:
            str: The string representation of the object.
        """
        return str(self.board)
