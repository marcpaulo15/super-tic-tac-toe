import pygame
import json
from typing import Tuple, Optional
from super_tic_tac_toe_board import SuperTicTacToeBoard
from tic_tac_toe_cell import TicTacToeCell

class GameHandler:

    # TODO: deal with global winner and game draw
    # TODO: add sounds
    # TODO: when there is a local game draw, empty (reset) the board

    # TODO: add BUTTON sound on/off
    # TODO: create a proper config file with everything
    # TODO: write the readme file

    def __init__(self,
                 config_path: str = "../config/classes_config.json") -> None:

        # TODO: deal with player names
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        self.screen_height = config['screen_height']
        self.screen_width = config['screen_width']
        self._set_up_global_board(topleft=config['board_topleft'],
                                  width=config['board_width'])
        self.mouse_pos = None

        self.font = pygame.font.SysFont(name=config['text_font'],
                                   size=config['text_font_size'])
        self.text_color = config['text_color']
        self.player_text = self._text("Player ")
        self.player_text_tl = (
            self.board.topleft[0],
            (self.board.topleft[1] - self.player_text.get_height()) // 2
        )

        self.active_player_icon = TicTacToeCell(
            topleft=(self.board.topleft[0] + self.player_text.get_width(),
                self.player_text_tl[1]),
            width=self.player_text.get_height()
        )
        self.active_player_icon.update(state=self.active_player)

        self.your_turn_text = self._text(", it's your turn!")
        self.your_turn_text_tl = (
            self.board.topleft[0] + self.player_text.get_width()\
                + self.active_player_icon.width,
            self.player_text_tl[1]
        )
        self.winner_text = self._text(", you win!!!")
        self.game_is_a_draw_text = self._text("This game is a draw!!!")

        small_font = pygame.font.SysFont(name='comicsans', size=50)
        self.new_game_button = small_font.render(
            "new game", True, config['new_game_button_text_color'], (153, 204, 255)
        )
        m = 10
        self.new_game_button_rect = self.new_game_button.get_rect(
            x=self.screen_width - self.new_game_button.get_width() - m, y=m
        )

    def _text(self, text: str) -> pygame.Surface:
        return self.font.render(text, True, self.text_color)

    def _set_up_global_board(self,
                             topleft: Optional[Tuple[float, float]] = None,
                             width: Optional[int] = None) -> None:
        """

        :param topleft:
        :param width:
        :return:
        """
        if hasattr(self, "board"):
            _topleft, _width = self.board.topleft, self.board.width
        elif topleft is not None and width is not None:
            _topleft, _width = topleft, width
        else:
            raise TypeError("If board attribute is not defined,"
                            "provide topleft and width arguments")

        # Set up the global board and the initial value for the game attributes
        self.board = SuperTicTacToeBoard(topleft=_topleft, width=_width)
        self.board.update(state=0)  # make all cells available
        self.active_player = 1  # player1 starts the game
        self.available_local_board = -1  # all local boards ara available

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mouse_pos = pygame.mouse.get_pos()
        return False

    def _update_availability(self, make_available: bool):
        if self.board.winner():
            # if there is global winner, everything becomes unavailable
            for local_board in self.board:
                local_board.update(state=-1)
        else:
            state = 0 if make_available else -1
            if self.available_local_board == GameHandler.all_available:
                for local_board in self.board:
                    local_board.update(state=state)
            else:
                self.board[self.available_local_board].update(state=state)

    def _update_active_player(self):
        self.active_player = 1 if self.active_player == 2 else 2
        self.active_player_icon.update(state=self.active_player)

    def _update_available_local_board(self, local_board):
        if self.board[local_board].winner():
            self.available_local_board = GameHandler.all_available
        else:
            self.available_local_board = local_board

    def _mark_cell(self, player, local_board, cell):
        self.board.update(state=player, local_board=local_board, cell=cell)
        # TODO: play sounds here
        if self.board.winner():
            pass  # global_win
        elif self.board[local_board].winner():
            pass  # local win
        else:  # cell win
            pass

    def _process_turn(self):
        selected_local_board_id, selected_cell_id = None, None
        for local_board_id, local_board in enumerate(self.board):
            for cell_id, cell in enumerate(local_board):
                if cell.collidepoint(self.mouse_pos):
                    if cell.available:
                        selected_local_board_id = local_board_id
                        selected_cell_id = cell_id
                    break

        if selected_cell_id is None or selected_local_board_id is None:
            return

        self._update_availability(make_available=False)
        self._mark_cell(player=self.active_player,
                        local_board=selected_local_board_id,
                        cell=selected_cell_id)
        self._update_active_player()
        self._update_available_local_board(local_board=selected_cell_id)
        self._update_availability(make_available=True)

    def run_logic(self):
        # only mouse clicks can change the state of the game
        if self.mouse_pos is GameHandler.mouse_not_clicked:
            return
        if self.new_game_button_rect.collidepoint(self.mouse_pos):
            self._set_up_global_board()
            # TODO: add a sound on / off button
        else:
            self._process_turn()

        self.active_player_icon.update(state=self.active_player)
        self.mouse_pos = GameHandler.mouse_not_clicked


    def _display_game_information(self, screen):
        screen.blit(self.player_text, self.player_text_tl)
        self.active_player_icon.draw(screen)
        if self.board.winner() > 0:  # winner (player1 or player2)
            screen.blit(self.winner_text, self.your_turn_text_tl)
        elif self.board.winner() == -1:  # game draw
            # TODO: change to game_is_draw_text
            screen.blit(self.your_turn_text, self.your_turn_text_tl)
        else:  # game is running
            screen.blit(self.your_turn_text, self.your_turn_text_tl)
        """
        text = f"Player {self.active_player}, it's your turn!"
        font = pygame.font.SysFont(name='comicsans', size=50)
        text = font.render(text, True, [0,0,0], [255,0,0])
        # TODO: text.get_rect(), set rect.x and rect.y, save text and rect as attributes, call screen.blit(text, rect)
        tl_x = self.board.tl[0]
        tl_y = (self.board.tl[1] - text.get_height()) // 2
        screen.blit(text, dest=(tl_x, tl_y))
        """

    def draw(self, screen):
        # TODO get bg_color from config
        screen.fill([255, 255, 255])
        self._display_game_information(screen)
        self.board.draw(screen)
        screen.blit(self.new_game_button, self.new_game_button_rect)
        pygame.display.update()


if __name__ == "__main__":
    WIDTH, HEIGHT = 800, 800

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("~ ULTIMATE TIC-TAC-TOE ~")
    clock = pygame.time.Clock()

    game = GameHandler()

    done = False
    while not done:
        done = game.process_events()
        game.run_logic()
        game.draw(screen)
        clock.tick(60)

    pygame.quit()