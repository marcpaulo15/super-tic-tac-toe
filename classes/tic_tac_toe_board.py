import pygame
import json
from tic_tac_toe_cell import TicTacToeCell
from tic_tac_toe_basic_board import TicTacToeBasicBoard


class TicTacToeBoard(TicTacToeBasicBoard):

    config_path = "../config/classes_config.json"

    def __init__(self, tl, width):
        TicTacToeBasicBoard.__init__(self)

        with open(TicTacToeBoard.config_path, 'r') as config_file:
            config = json.load(config_file)
        dist_pct = config['intra_cell_dist_pct']

        cell_width = (width * (1-dist_pct)) // 3
        cell_dist = (width*dist_pct) // 4

        self.big_cell = TicTacToeCell(
            tl=(cell_dist + tl[0], cell_dist + tl[1]),
            width=(3*cell_width + 2*cell_dist)
        )

        self.board = [
            TicTacToeCell(
                tl=(
                    cell_dist + tl[0] + (i % 3)*(cell_width+cell_dist),
                    cell_dist + tl[1] + (i//3)*(cell_width+cell_dist)
                ),
                width=(width * (1-dist_pct)) // 3
            )
            for i in range(9)
        ]

    def update(self, state, cell=None):
        # TODO: review logic
        # state = {-1: unavailable, 0: available, 1: winner1, 2: winner2}
        if cell is None:
            if state in (-1, 0):  # update the board (all the cells)
                for _cell in self.board:
                    _cell.update(state=state)
            else:  # state in (1, 2): local win
                self.big_cell.update(state)
        else:  # update only the given cell
            self.board[cell].update(state=state)

    def draw(self, screen):
        if self.big_cell.winner:
            self.big_cell.draw(screen)
        else:
            for cell in self.board:
                cell.draw(screen)


if __name__ == "__main__":
    # 0 | 1 | 2
    # ---------
    # 3 | 4 | 5
    # ---------
    # 6 | 7 | 8

    WIDTH, HEIGHT = 800, 800

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("~ TIC-TAC-TOE BOARD ~")
    clock = pygame.time.Clock()

    board = TicTacToeBoard(tl=(100, 100), width=600)
    board[0].update(1)
    board[1].update(0)
    board[5].update(2)
    board[6].update(0)
    board[8].update(2)

    done = False
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill([0, 0, 0])
        board.draw(screen)
        pygame.display.update()

        clock.tick(60)

    pygame.quit()
