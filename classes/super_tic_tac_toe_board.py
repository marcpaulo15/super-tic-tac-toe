import pygame
import json
from typing import Tuple, Optional
from tic_tac_toe_board import TicTacToeBoard
from tic_tac_toe_basic_board import TicTacToeBasicBoard


class SuperTicTacToeBoard(TicTacToeBasicBoard):
    """
    SuperTicTacToeBoard Implements the functionalities of a Super TicTacToe
        board. Inherits functionalities from TicTacToeBasicBoard class.
        Fills the board attribute with 9 TicTacToeBoards, each one containing a
        local board with 9 TicTacToeCells.

    SuperTicTacToeBoard Attributes
        (refer to TicTacToeBasicBoard class documentation)
        board     - list of TicTacToeBoard that simulate a 3x3 global board

    SuperTicTacToeBoard Methods
        (refer to TicTacToeBasicBoard class documentation)
        update    - updates the board state or the state of a given cell
        draw      - displays the board depending on its state
    """

    def __init__(self,
                 topleft: Tuple[float, float],
                 width: int,
                 config_path: str = "../config/config.json") -> None:
        """
        Inits a SuperTicTacToeBoard instance at a given location with a given
        width

        :param topleft: coordinates of the top-left corner of the board
        :param width: length of the square defining the board's shape
        :param config_path: path from where to read the configuration file
        """

        # Inits parent class
        TicTacToeBasicBoard.__init__(self, topleft=topleft, width=width)

        # define a list of 9 local boards to simulate a 3x3 grid
        self.board = [
            TicTacToeBoard(
                topleft=(topleft[0] + (i % 3)*width/3,
                         topleft[1] + (i//3)*width/3),
                width=width//3
            )
            for i in range(9)
        ]

        # Define a rect to draw the edges of the global grid
        self.global_grid = pygame.Rect(self.topleft, (self.width, self.width))

        # From the config file, retrieve the color of the edges
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        self.edge_color = config['edge_color']

    def update(self,
               state: int,
               local_board: Optional[int] = None,
               cell: Optional[int] = None) -> None:
        """
        If a cell and a local board are provided, update the winner of the cell
        If only a local board is provided, update the availability of the board
        If only state is provided, update the availability of the global board.

        :param state: state of the global board / local board / cell to update
        :param local_board: if provided, local board to update
        :param cell: if provided, cell to update (in the given local board)
        :return: None
        :raise: ValueError if the update violate any rule of the game
        """

        # NOTE: regarding the state of the boards, only availability can be
        # updated. The winner is computed dynamically depending on the boards.
        # NOTE: regarding the state of the cells, only the winner can be
        # updated. The availability is updated for the entire local board
        if local_board is None and cell is None:  # only state is provided
            # update the state of the global board
            if state in (-1, 0):  # availability of the global board
                for _local_board in self.board:
                    _local_board.update(state=state)
            else:  # state in (1,2) (winner)
                raise ValueError("The game winner can't be set manually")
        elif local_board is None and cell is not None:
            # a cell is given but its local board is missing
            raise ValueError("Provide a local board for the given cell")
        else:  # local board is not None, mark the cell
            self.board[local_board].update(state=state, cell=cell)
            if self.board[local_board].winner() > 0:
                # update the local board
                self.board[local_board].big_cell.update(
                    state=self.board[local_board].winner())
            elif self.board[local_board].winner() == -1:  # local game is draw
                # reset the local board
                for _cell in self.board[local_board]:
                    _cell.reset()

    def draw(self, screen: pygame.Surface) -> None:
        """
        Displays the global board on the given surface.
        :param screen: pygame Surface where the global board is placed
        :return: None
        """

        # Draw the grid edges
        pygame.draw.rect(screen, color=self.edge_color, rect=self.global_grid)
        # Draw the global board on top of the grid
        for local_board in self.board:
            local_board.draw(screen)


if __name__ == "__main__":
    # 1) create a pygame Surface where the global board will be placed
    WIDTH, HEIGHT = 800, 800
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("~ SUPER TIC-TAC-TOE BOARD ~")
    clock = pygame.time.Clock()

    # 2) Initialize a board for the Super TicTacToe game
    super_board = SuperTicTacToeBoard(topleft=(100, 100), width=600)

    # 3) Update the cells to display an example of a global board configuration
    # by default, all the cells are available

    # fill some random cells
    super_board.update(state=1, local_board=7, cell=8)
    super_board.update(state=2, local_board=2, cell=0)
    super_board.update(state=1, local_board=4, cell=4)
    super_board.update(state=2, local_board=4, cell=5)
    super_board.update(state=1, local_board=8, cell=1)
    super_board.update(state=2, local_board=3, cell=6)

    # simulate a player1's win on the local_board_1 (simply fill the first row)
    super_board.update(state=1, local_board=1, cell=0)
    super_board.update(state=1, local_board=1, cell=1)
    super_board.update(state=1, local_board=1, cell=2)
    # simulate a player1's win on the local_board_5 (simply fill the first col)
    super_board.update(state=1, local_board=5, cell=0)
    super_board.update(state=1, local_board=5, cell=3)
    super_board.update(state=1, local_board=5, cell=6)
    # simulate a player2's win on the local_board_6 (simply fill the asc diag)
    super_board.update(state=2, local_board=6, cell=2)
    super_board.update(state=2, local_board=6, cell=4)
    super_board.update(state=2, local_board=6, cell=6)

    super_board.update(state=-1)  # make all the cells unavailable
    super_board.update(state=0, local_board=3)  # make board3 available
    # super_board.update(state=1, cell=6)  # ValueError: local board is missing

    # 4) Set up the usual pygame flow
    done = False
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill([0, 0, 0])  # fill the screen with a black background
        super_board.draw(screen)  # display the global board (its local boards)
        pygame.display.update()  # update the screen content

        clock.tick(60)

    pygame.quit()
