import numpy as np


class Player:
    def __init__(self, identifier: int):
        self.number = identifier
        self.wins = 0


class Connect4:
    def __init__(self):
        self.board = np.zeros((6, 7), dtype=int)
        self.num_of_moves = 0

    def clear_board(self):
        self.board = np.zeros((6, 7), dtype=int)
        self.num_of_moves = 0

    def make_move(self, column: int, player: Player):
        if not self.is_valid_move(column):
            raise ValueError(f"Column {column} is already full.")

        row = self.get_next_row(column)
        self.board[row][column] = player.number
        self.num_of_moves += 1

    def is_board_full(self) -> bool:
        return self.num_of_moves == 42

    def get_next_row(self, column: int) -> int:
        for row in range(5, -1, -1):
            if self.board[row][column] == 0:
                return row

    def is_valid_move(self, column: int) -> bool:
        return self.board[0][column] == 0

    def starting_player(self, players: [Player]) -> Player:
        return np.random.choice(players)

    def initiate_game(self):
        self.player_one = Player(1)
        self.player_two = Player(2)

        self.current_player = self.starting_player([self.player_one, self.player_two])

        while not self.is_board_full():
            column = (
                int(input(f"Player {self.current_player.number}, choose a column: "))
                - 1
            )

            try:
                self.make_move(column, self.current_player)

                print(self.board)
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
