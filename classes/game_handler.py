import pygame
import json
from typing import Tuple
from classes.super_tic_tac_toe_board import SuperTicTacToeBoard
from classes.tic_tac_toe_cell import TicTacToeCell


class GameHandler:
    """
    GameHandler implements the logic of a Super Tic-Tac-Toe game.
        Process each turn and updates the state of the game. It updates the GUI
        (screen) according to the game state. Calling the 'run' method will run
        the game.

    GameHandler Attributes
        board          - global board, a SuperTicTacToeBoard instance
        active_player  - which player takes turn. one of [1 2]
        mouse_pos      - (x,y) mouse coordinates to process the player's action
        sound_on       - whether to play sounds
        screen         - pygame surface where the game is displayed

    GameHandler Methods
        process_events - process the events of the game (mouse clicks)
        run_logic      - runs the logic of the game based on user's actions
        draw           - displays the game's elements on the given surface
        run            - runs the main loop to play the game
    """

    def __init__(self,
                 config_path: str = "../config/config.json") -> None:
        """
        Inits a GameHandler instance

        :param config_path: path from where to read the configuration file
        """

        with open(config_path, 'r') as config_file:
            config = json.load(config_file)

        # Initialize pygame and create the screen (surface)
        screen_width = config['screen_width']
        screen_height = config['screen_height']
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption(config['title'])

        # Create the (global) Super TicTacToe board
        self.board = SuperTicTacToeBoard(
            topleft=config['board_topleft'], width=config['board_width']
        )

        self._available_local_board = -1  # all local boards ara available
        self.mouse_pos = None  # mouse_pos is not None when mouse is clicked
        self._first_player = config['player_starting_the_game']
        self.active_player = self._first_player  # player to take turn
        self._screen_bg_color = config['screen_bg_color']
        self.sound_on = config['is_sound_on']  # whether sounds will be played
        self.title = config['title']

        # Defines text elements to display information about the game's state
        # when the game is running, tell which player takes turn (active):
        #   "Player {icon}, it's your turn!"
        # when the game has a winner, tell which player has won:
        #   "Player {icon}, you win!!!"
        # when the game is a draw, tell the players that the game is over:
        #   "This game is a draw!!!"

        self._font = pygame.font.SysFont(name=config['text_font'],
                                         size=config['text_font_size'])
        self._text_color = config['text_color']
        self._player_text = self._text("Player ")
        self._player_text_tl = (
            self.board.topleft[0],
            (self.board.topleft[1] - self._player_text.get_height()) // 2
        )

        self._active_player_icon = TicTacToeCell(
            topleft=(self.board.topleft[0] + self._player_text.get_width(),
                     self._player_text_tl[1]),
            width=self._player_text.get_height()
        )
        self._active_player_icon.update(state=self.active_player)

        self._your_turn_text = self._text(", it's your turn!")
        self._game_info_tl = (
            self.board.topleft[0] + self._player_text.get_width()
            + self._active_player_icon.width,
            self._player_text_tl[1]
        )

        self._winner_text = self._text(", you win!!!")
        self._game_is_a_draw_text = self._text("This game is a draw!!!")

        small_font = pygame.font.SysFont(name=config['text_font'],
                                         size=config['text_font_size'])
        self._new_game_button = small_font.render(
            'new game', True, config['new_game_button_text_color'],
            config['new_game_button_color']
        )
        m = 10  # margin to separate the button from the screen boundaries
        self._new_game_button_rect = self._new_game_button.get_rect(
            x=screen_width - self._new_game_button.get_width() - m, y=m
        )

        # Load sounds to be played (only if sound is on)
        self._cell_win_sound = pygame.mixer.Sound(config['cell_win_sound'])
        self._local_win_sound = pygame.mixer.Sound(config['local_win_sound'])
        self._global_win_sound = pygame.mixer.Sound(config['global_win_sound'])

    def _text(self, text: str) -> pygame.Surface:
        """
        Renders the given string into a pygame surface

        :param text: string to be rendered
        :return: pygame Surface containing the given text
        """

        return self._font.render(text, True, self._text_color)

    def _reset_game(self) -> None:
        """
        Creates a new global board and sets the game parameters to their values
        by default when initialized. Called when new_game button is clicked

        :return: None
        """

        topleft, width = self.board.topleft, self.board.width
        self.board = SuperTicTacToeBoard(topleft=topleft, width=width)
        self.board.update(state=0)  # make all cells available
        self.active_player = self._first_player  # who starts the game
        self._active_player_icon.update(state=self.active_player)
        self._available_local_board = -1  # all local boards ara available

    def _update_availability(self, make_available: bool) -> None:
        """
        Updates the availability of the current available_local_board attribute

        :param make_available: whether to make it available or unavailable
        :return: None
        """

        if self.board.winner():
            # if there is global winner, make all local board unavailable
            for local_board in self.board:
                local_board.update(state=-1)
        else:  # game is running
            state = 0 if make_available else -1
            if self._available_local_board == -1:
                # update the availability of all the local boards
                for local_board in self.board:
                    local_board.update(state=state)
            else:
                self.board[self._available_local_board].update(state=state)

    def _update_active_player(self) -> None:
        """
        Alternate player1 and player2 to take turns. If the game already has a
        winner, don't change the active player icon (it's the winner one)

        :return: None
        """

        if self.board.winner() <= 0:  # no global winner
            self.active_player = 1 if self.active_player == 2 else 2
            # also updates the icon that is displayed in the game info (text)
            self._active_player_icon.update(state=self.active_player)

    def _update_available_local_board(self, local_board: int) -> None:
        """
        The position of the last selected cell defines the next available local
        board. If that local_board already has a winner, all the local boards
        become available.

        :param local_board: (index of) the next available local board
        :return: None
        """

        if self.board[local_board].winner():
            self._available_local_board = -1  # make all the boards available
        else:
            self._available_local_board = local_board

    def _mark_cell(self, player: int, local_board: int, cell: int) -> None:
        """
        Marks the given cell with the given player. Checks the state of the
        game once the cell is marked (global win, local win, local draw, same)
        and updates it accordingly. Plays sound if sound is on.

        :param player: which player is marking the cell
        :param local_board: board where the cell belongs to
        :param cell: cell marked by the given player
        :return: None
        """

        # Mark the cell with the given player
        self.board.update(state=player, local_board=local_board, cell=cell)

        # check the state of the boards once the new cell is marked
        if self.board.winner() > 0:  # the game has a winner
            # set the winner icon to be displayed
            self._active_player_icon.update(state=self.board.winner())
            if self.sound_on:
                self._global_win_sound.play()
        elif self.board[local_board].winner() > 0 and self.sound_on:
            self._local_win_sound.play()  # local win
        elif self.sound_on:
            self._cell_win_sound.play()  # cell win

    def _process_turn(self) -> None:
        """
        Check if the mouse_pos collides with any available cell. If that is the
        case, update the board and the game params accordingly to go on with
        the game. If the mouse_pos clicks on an unavailable cell or outside the
        board, do nothing (wait for the next mouse click)

        :return: None
        """

        # 1) check that the mouse clicked on an available cell
        local_board, cell = self._get_board_and_cell_from_mouse_pos()
        if local_board == -1 or cell == -1:
            # -1 means that no available cell was selected
            return  # there is nothing to process, wait for the next click

        # If an available cell was selected, run the steps to play the turn
        # 2) Make unavailable the local board that was available this turn
        self._update_availability(make_available=False)
        # 3) Mark the cell in the board
        self._mark_cell(player=self.active_player,
                        local_board=local_board,
                        cell=cell)
        # 4) Let the inactive player be the active player the next turn
        self._update_active_player()
        # 5) Set which local board are available the next turn
        self._update_available_local_board(local_board=cell)
        # 6) Make those boards available
        self._update_availability(make_available=True)
        # 7) The next player is ready to take turn

    def _get_board_and_cell_from_mouse_pos(self) -> Tuple[int, int]:
        """
        Assuming that self.mouse_pos is not None, check if the mouse position
        collides with any available cell. Returns the cell_id and the
        local_board_id where the cell belongs to.
        If no collision is found, return (-1,-1)

        :return: two integers from 0 to 8 representing a local board and a cell
            return (-1,-1) if the mouse did not collide with any available cell
        """

        for local_board_id, local_board in enumerate(self.board):
            for cell_id, cell in enumerate(local_board):
                if cell.collidepoint(self.mouse_pos):
                    if cell.available:
                        return local_board_id, cell_id
        return -1, -1  # no available cell was clicked

    def _display_game_information(self, screen: pygame.Surface) -> None:
        """
        Displays information about the state of the game. If the game is
        running, tells which player takes turn. If there is a winner, announce
        the winner. If the game is a draw, inform the players about it.

        :param screen: pygame surface where the text is displayed
        :return: None
        """

        if self.board.winner() >= 0:
            # if the game is not a draw, display the active or winner player
            screen.blit(self._player_text, self._player_text_tl)
            self._active_player_icon.draw(screen)
            if self.board.winner() > 0:  # active player is the winner
                screen.blit(self._winner_text, self._game_info_tl)
            else:  # active player is player taking turn
                screen.blit(self._your_turn_text, self._game_info_tl)
        else:  # self.board.winner() == -1
            # the game is a draw, don't display the active player
            screen.blit(self._game_is_a_draw_text, self._player_text_tl)

    def process_events(self) -> bool:
        """
        Deals with the user's input (right mouse click).
        Possible actions: quit the game, right mouse click

        :return: whether to quit the game
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # store the position of the mouse click. It will be used in the
                # run_logic method
                self.mouse_pos = pygame.mouse.get_pos()
        return False

    def run_logic(self) -> None:
        """
        Translates the mouse clicks from the users into the proper game change
        Possible actions: click on a cell, click the new_game button

        :return: None
        """

        if self.mouse_pos is None:
            return  # only react against the player's mouse clicks
        if self._new_game_button_rect.collidepoint(self.mouse_pos):
            self._reset_game()  # restart the game (board)
        else:  # a cell has been selected
            self._process_turn()
        # return to default value, wait for the next mouse click
        self.mouse_pos = None

    def draw(self, screen: pygame.Surface) -> None:
        """
        Displays the game's elements on the given surface.

        :param screen: pygame Surface where the game is displayed
        :return: None
        """

        screen.fill(self._screen_bg_color)
        self.board.draw(screen=screen)
        self._display_game_information(screen=screen)
        screen.blit(self._new_game_button, self._new_game_button_rect)
        pygame.display.update()

    def run(self) -> None:
        """
        Runs the main loop to play the game

        :return: None
        """

        clock = pygame.time.Clock()
        done = False
        while not done:
            done = self.process_events()
            self.run_logic()
            self.draw(screen=self.screen)
            clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    game = GameHandler()
    game.run()
