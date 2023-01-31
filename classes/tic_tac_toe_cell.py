import json
import pygame
from typing import Tuple


class TicTacToeCell:
    """
    TicTacToeCell defines a cell in a TicTacToe board.
        In the common TicTacToe board there are 9 cells. Each one can be filled
        by just one of the two players during the game. A cell can be filled
        only if it is available. Once a cell is filled by a player, the cell
        has a winner and it's no longer available and can't be filled again.
        This class is intended to be used inside the TicTacToeBoard
        class to define the cells' behaviour and the game's logic.

    TicTacToeCell Attributes:
        width     - cell's shape is a {width}x{width} square
        _winner   - {0: not filled, 1: filled by player1, 2: filled by player2}
        available - whether the cell can be filled in the current turn

    TicTacToeCell Methods:
        winner    - return value of _winner
        update    - updates the cell state: _winner, available attributes
        draw      - displays the cell (square) depending on the _winner value
    """

    def __init__(self,
                 topleft: Tuple[float, float],
                 width: int,
                 config_path: str = "../config/classes_config.json"
                 ) -> None:
        """
        Inits TicTacToeCell instance at a given location with a given width

        :param topleft: coordinates of the top-left corner of the cell
        :param width: length of the square defining the cell's shape
        :param config_path: path from where to read the configuration file
        """

        self.width = width  # a cell is represented by a {width}x{width} square
        self._winner = 0  # initially, the cell is not filled
        self.available = True  # initially, all the cells are available

        # Set up the customized attributes from the configuration file
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        # color of the cell when it is available or unavailable
        self._available_bg_color = config['available_bg_color']
        self._unavailable_bg_color = config['unavailable_bg_color']
        player1_img = pygame.image.load(config['player1_img']).convert()
        self._player1_img = pygame.transform.scale(player1_img, (width, width))
        player2_img = pygame.image.load(config['player2_img']).convert()
        self._player2_img = pygame.transform.scale(player2_img, (width, width))

        # create the {width}x{width} square representing the cell
        self._image = pygame.Surface([self.width, self.width])
        self._rect = self._image.get_rect(topleft=topleft)

    def winner(self) -> int:
        """
        Returns the value of _winner. This method follows the structure of the
        TicTacToeBasicBoard class, so it can be called recursively.
        :return: int: _winner value
        """

        return self._winner

    def update(self, state: int) -> None:
        """
        Updates the state of the cell, defined by attributes available, _winner
        :param state: -1 if unavailable, 0 if available, 1|2 if filled
        :return: None
        :raises: ValueError if state not in (-1,0,1,2)
        """

        # NOTE: if the cell has a winner (_winner != 0), availability does not
        # matter, since the cell can't be chosen again
        if state == -1:  # set to unavailable
            self.available = False
        elif state == 0:  # set to available
            self.available = True
        elif state in (1, 2):  # a player has filled the cell
            self._winner = state
        else:
            raise ValueError("wrong value for cell state")

    def draw(self, screen: pygame.Surface) -> None:
        """
        Displays the cell on the given surface
        :param screen: pygame Surface where the cell is placed
        :return: None
        """

        # NOTE: cell availability only matters when it has not been filled yet
        if self._winner:
            # if there is a winner, display its image
            img = self._player1_img if self._winner == 1 else self._player2_img
            self._image = img
        else:  # no cell winner, fill the cell with a plain color
            if self.available:  # available and not filled yet
                bg_color = self._available_bg_color
            else:  # unavailable and not filled yet
                bg_color = self._unavailable_bg_color
            self._image.fill(bg_color)
        screen.blit(self._image, self._rect)


if __name__ == "__main__":
    # 1) create a pygame Surface where the cells will be placed
    screen_width, screen_height = 600, 600
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("~ TIC-TAC-TOE CELL ~")
    clock = pygame.time.Clock()

    # 2) Initialize a set of random cells having different locations and widths
    random_cells = [
        TicTacToeCell(topleft=(500, 20), width=80),
        TicTacToeCell(topleft=(10, 400), width=150),
        TicTacToeCell(topleft=(300, 300), width=250),
        TicTacToeCell(topleft=(50, 50), width=100)
    ]

    # 3) Update the cells to display all the possible scenarios (cell states)
    random_cells[0].update(state=-1)  # unavailable and not filled
    random_cells[1].update(state=0)   # available and not filled (by default)
    random_cells[2].update(state=1)   # filled by player1
    random_cells[3].update(state=2)   # filled by player2
    # random_cells[0].update(state=10)  # raises a ValueError

    # 4) Set up the usual pygame flow
    done = False
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill([0, 0, 0])  # fill the screen with a black background
        # Display the cells on the screen
        for cell in random_cells:
            cell.draw(screen)
        pygame.display.update()  # update the screen content

        clock.tick(60)

    pygame.quit()
