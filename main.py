from src.game_logic.connect4 import Connect4
from src.app.connect4_gui import Connect4GUI


def main():
    game = Connect4()
    game._initiate_terminal_game()


if __name__ == "__main__":
    main()
