from src.game_logic.connect4 import Connect4


def main():
    game = Connect4()
    print(game.board)
    game.make_move(3, game.player_one)
    print(game.board)
    game.make_move(3, game.player_two)
    print(game.board)


if __name__ == "__main__":
    main()
