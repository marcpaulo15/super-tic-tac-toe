import json
import pygame


class TicTacToeCell:

    config_path = "../config/classes_config.json"

    def __init__(self, tl, width):

        self.width = width
        self.winner = 0
        self.available = False

        with open(TicTacToeCell.config_path, 'r') as config_file:
            config = json.load(config_file)

        self.available_bg_color = config['available_bg_color']
        self.unfilled_bg_color = config['unfilled_bg_color']
        player1_img = pygame.image.load(config['player1_img']).convert()
        self.player1_img = pygame.transform.scale(player1_img, (width, width))
        player2_img = pygame.image.load(config['player2_img']).convert()
        self.player2_img = pygame.transform.scale(player2_img, (width, width))

        self.image = pygame.Surface([self.width, self.width])
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = tl[0], tl[1]
        self.image.fill(self.unfilled_bg_color)

    def update(self, state):
        # state = {-1: unavailable, 0: available, 1: winner1, 2: winner2}
        if state == -1:
            self.available = False
        elif state == 0:
            self.available = True
        elif state in (1, 2):
            self.winner = state
            self.available = False
        else:
            raise Exception("wrong value for cell state")

    def draw(self, screen):
        if self.winner:
            img = self.player1_img if self.winner == 1 else self.player2_img
            self.image = img
        else:  # not filled yet
            if self.available:
                bg_color = self.available_bg_color
            else:  # unavailable and not filled yet
                bg_color = self.unfilled_bg_color
            self.image.fill(bg_color)
        screen.blit(self.image, self.rect)
        # or pygame.blit(screen, self.rect, (tl_x, tl_))
        # this way we avoid creating 81 surface (one for each cell)


if __name__ == "__main__":
    WIDTH, HEIGHT = 600, 600

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("~ TIC-TAC-TOE CELL ~")
    clock = pygame.time.Clock()

    random_cells = [
        TicTacToeCell(tl=(300, 300), width=250),
        TicTacToeCell(tl=(50, 50), width=100),
        TicTacToeCell(tl=(10, 400), width=150),
        TicTacToeCell(tl=(500, 20), width=80)
    ]
    random_cells[0].update(state=0)
    random_cells[1].update(state=1)
    random_cells[2].update(state=2)

    done = False
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill([0, 0, 0])  # black
        for cell in random_cells:
            cell.draw(screen)
        pygame.display.update()

        clock.tick(60)

    pygame.quit()
