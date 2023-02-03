import sys
sys.path.insert(0, '../classes')
from game_handler import GameHandler


if __name__ == "__main__":
    game = GameHandler()
    game.run()
