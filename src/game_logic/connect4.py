import numpy as np


class Player:
    def __init__(self, identifier: int):
        self.number = identifier
        self.wins = 0


class Connect4:
    def __init__(self):
        self.board = np.zeros((6, 7), dtype=int)
        self.num_of_moves = 0
        self.player_one = Player(1)
        self.player_two = Player(2)

    def clear_board(self):
        self.board = np.zeros((6, 7), dtype=int)
        self.num_of_moves = 0

    def make_move(self, column: int, player: Player) -> bool:
        if self.is_valid_move(column):
            row = self.get_next_row(column)
            self.board[row][column] = player.number
            self.num_of_moves += 1
            return True
        else:
            return False

    def get_next_row(self, column: int) -> int:
        for row in range(5, -1, -1):
            if self.board[row][column] == 0:
                return row

    def is_valid_move(self, column: int) -> bool:
        return self.board[0][column] == 0

    def starting_player(self, players: [Player]) -> Player:
        return np.random.choice(players)


if __name__ == "__main__":
    game = Connect4()
    print(game.board)
