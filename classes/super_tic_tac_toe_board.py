import pygame
from tic_tac_toe_board import TicTacToeBoard
from tic_tac_toe_basic_board import TicTacToeBasicBoard


class SuperTicTacToeBoard(TicTacToeBasicBoard):

    def __init__(self, tl, width):
        TicTacToeBasicBoard.__init__(self)

        self.board = [
            TicTacToeBoard(
                tl=(tl[0] + (i % 3)*width/3, tl[1] + (i//3)*width/3),
                width=width // 3
            )
            for i in range(9)
        ]

    def update(self, state, local_board=None, cell=None):
        # TODO: review this
        if local_board is None:
            if cell is None:
                pass  # update the status of the global board (available)
            else:
                raise Exception("Provide a board for the given cell")
        else:
            if cell is None:
                self.board[local_board].update(state=state)
            else:
                self.board[local_board][cell].update(state=state)

    def draw(self, screen):
        for local_board in self.board:
            local_board.draw(screen)


if __name__ == "__main__":

    WIDTH, HEIGHT = 800, 800

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("~ TIC-TAC-TOE BOARD ~")
    clock = pygame.time.Clock()

    super_board = SuperTicTacToeBoard(tl=(100, 100), width=600)

    super_board.update(state=0, local_board=0)
    super_board.update(state=1, local_board=1)
    super_board.update(state=2, local_board=2)
    super_board.update(state=0, local_board=3, cell=3)
    super_board.update(state=1, local_board=5, cell=7)
    super_board.update(state=2, local_board=7, cell=7)
    super_board.update(state=0, local_board=8)
    # super_board.update(state=0)

    done = False
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill([0, 0, 0])
        super_board.draw(screen)
        pygame.display.update()

        clock.tick(60)

    pygame.quit()
