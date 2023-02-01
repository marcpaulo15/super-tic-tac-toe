import pygame
from typing import Optional, Tuple
from tic_tac_toe_cell import TicTacToeCell
from tic_tac_toe_basic_board import TicTacToeBasicBoard


class TicTacToeBoard(TicTacToeBasicBoard):
    """
    TicTacToeBoard Implements the functionalities of a TicTacToe board.
        Inherits functionalities from TicTacToeBasicBoard class.
        Fills the board attribute with 9 TicTacToeCells (3x3 grid)

    TicTacToeBoard Attributes
        (refer to TicTacToeBasicBoard class documentation)
        board     - list of TicTacToeCells that simulate a 3x3 local board
        big_cell  - defines the behaviour of the board when it acts as a cell

    TicTacToeBoard Methods
        (refer to TicTacToeBasicBoard class documentation)
        update    - updates the board state or the state of a given cell
        draw      - displays the board depending on its state
    """

    # Percentage of the width that used to create a separation between cells
    cell_dist_pct = 0.10
    # TODO: try to use this attr in SuperTicTacToeBoard as well

    def __init__(self, topleft: Tuple[float, float], width: int) -> None:
        """
        Inits a TicTacToeBoard instance at a given location with a given width

        :param topleft: coordinates of the top-left corner of the board
        :param width: length of the square defining the board's shape
        """

        # Inits parent class
        TicTacToeBasicBoard.__init__(self, topleft=topleft, width=width)

        # computes the real cell width taking into account a margin (distance)
        cell_width = (width * (1-TicTacToeBoard.cell_dist_pct)) // 3
        # there is a separation at both extremes and between cells
        cell_dist = (width * TicTacToeBoard.cell_dist_pct) // 4

        # defined a (big) cell with the same shape as the board. When the board
        # has winner, it will act as a filled cell in the global board
        self.big_cell = TicTacToeCell(
            topleft=(cell_dist + topleft[0], cell_dist + topleft[1]),
            width=(3 * cell_width + 2 * cell_dist)
        )
        # define a list of 9 cells to simulate a 3x3 grid
        self.board = [
            TicTacToeCell(
                topleft=(
                    cell_dist + topleft[0] + (i % 3)*(cell_width+cell_dist),
                    cell_dist + topleft[1] + (i//3)*(cell_width+cell_dist)
                ),
                width=cell_width
            )
            for i in range(9)
        ]

    def update(self, state: int, cell: Optional[int] = None) -> None:
        """
        If a cell is provided, update the state of the given cell (winner).
        Otherwise, update the overall state of the board (availability).

        :param state: -1 if board is unavailable, 0 if board available, 1|2 if
            a given cell is filled
        :param cell: index of cell that has been filled (state is 1|2)
        :return: None
        :raise: ValueError if (state in (-1,0) and cell is None)
            or (state in (1,2) and cell is None)
        """

        if cell is None:
            # update the overall state of the board (available or unavailable)
            # NOTE: can't set the board state to 1|2, it depends on the cells
            if state in (-1, 0):  # update the availability of board
                for _cell in self.board:
                    _cell.update(state=state)
            else:  # the winner depends on the game, can't be set manually
                raise ValueError("wrong value for board availability")
        else:  # a cell is provided
            # update the state of the given cell (filled by player1 or player2)
            # NOTE: can't set the cell state to 1|2, availability is an
            # attribute of the board. Its cells are either all available or not
            if state in (1, 2):
                self.board[cell].update(state=state)
            else:  # availability can't be set to a specific cell but the board
                raise ValueError("wrong value for the cell state in the board")
        # TODO: move this to another place
        # update local winner
        if self.winner():
            self.big_cell.update(state=self.winner())

    def draw(self, screen: pygame.Surface) -> None:
        """
        Displays the board on the given surface -> displays its cells
        :param screen: pygame Surface where the board is placed
        :return: None
        """

        # NOTE: in the Super Tic-Tac-Toe game, if there is a winner the board
        # acts as a (big) cell and displays the winner's image
        if self.big_cell.winner():
            self.big_cell.draw(screen)
        else:
            for cell in self.board:
                cell.draw(screen)


if __name__ == "__main__":
    # 1) create a pygame Surface where the local board will be placed
    screen_width, screen_height = 800, 800
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("~ TIC-TAC-TOE BOARD ~")
    clock = pygame.time.Clock()

    # 2) Initialize a board for the TicTacToe game
    board = TicTacToeBoard(topleft=(100, 100), width=600)

    # 3) Update the cells to display an example of a local board configuration
    # by default, every cell in the board is available
    board.update(state=1, cell=1)  # cell1 is marked by player1
    board.update(state=2, cell=2)  # cell2 is marked by player2
    board.update(state=1, cell=6)  # cell6 is marked by player1
    board.update(state=2, cell=8)  # cell8 is marked by player2
    board.update(state=-1)         # make board unavailable (all its cells)
    # board.update(state=3, cell=7)  # ValueError: wrong value for cell state

    # 4) Set up the usual pygame flow
    done = False
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill([0, 0, 0])  # fill the screen with a black background
        board.draw(screen)  # display the board (its cells)
        pygame.display.update()  # update the screen content

        clock.tick(60)

    pygame.quit()
