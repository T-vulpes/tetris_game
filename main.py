#tetris game code
import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
SHAPES = [
    ([[1, 1, 1, 1]], CYAN),     # I
    ([[1, 1], [1, 1]], YELLOW),  # O
    ([[1, 0, 0], [1, 1, 1]], BLUE), # J
    ([[0, 0, 1], [1, 1, 1]], ORANGE), # L
    ([[0, 1, 1], [1, 1, 0]], GREEN),  # S
    ([[1, 1, 0], [0, 1, 1]], RED),    # Z
    ([[0, 1, 0], [1, 1, 1]], MAGENTA) # T
]

class Tetris:
    def __init__(self):
        self.width = 10
        self.height = 20
        self.field = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.score = 0
        self.game_over = False
        self.current_piece, self.current_color = self.new_piece()
        self.next_piece, self.next_color = self.new_piece()

    def new_piece(self):
        return random.choice(SHAPES)

    def can_move(self, shape, x, y):
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j] and (
                    i + y >= self.height or
                    j + x >= self.width or
                    j + x < 0 or
                    self.field[i + y][j + x]
                ):
                    return False
        return True

    def place_piece(self, shape, x, y):
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j]:
                    self.field[i + y][j + x] = shape[i][j]
        self.clear_lines()
        self.current_piece, self.current_color = self.next_piece, self.next_color
        self.next_piece, self.next_color = self.new_piece()
        if not self.can_move(self.current_piece, self.width // 2 - len(self.current_piece[0]) // 2, 0):
            self.game_over = True

    def clear_lines(self):
        new_field = [row for row in self.field if any(cell == 0 for cell in row)]
        lines_cleared = self.height - len(new_field)
        self.score += lines_cleared
        self.field = [[0 for _ in range(self.width)] for _ in range(lines_cleared)] + new_field

    def rotate(self, shape):
        return [[shape[y][x] for y in range(len(shape))] for x in range(len(shape[0]) - 1, -1, -1)]

    def draw_grid(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                if self.field[y][x]:
                    pygame.draw.rect(screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_piece(self, screen, shape, color, x, y):
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j]:
                    pygame.draw.rect(screen, color, ((x + j) * BLOCK_SIZE, (y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def draw_score(self, screen, font):
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH - 150, 20))

    def draw_game_over(self, screen, font):
        game_over_text = font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 36)

        current_x, current_y = self.width // 2 - len(self.current_piece[0]) // 2, 0

        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.can_move(self.current_piece, current_x - 1, current_y):
                        current_x -= 1
                    elif event.key == pygame.K_RIGHT and self.can_move(self.current_piece, current_x + 1, current_y):
                        current_x += 1
                    elif event.key == pygame.K_DOWN and self.can_move(self.current_piece, current_x, current_y + 1):
                        current_y += 1
                    elif event.key == pygame.K_UP:
                        rotated_piece = self.rotate(self.current_piece)
                        if self.can_move(rotated_piece, current_x, current_y):
                            self.current_piece = rotated_piece

            if not self.can_move(self.current_piece, current_x, current_y + 1):
                self.place_piece(self.current_piece, current_x, current_y)
                current_x, current_y = self.width // 2 - len(self.current_piece[0]) // 2, 0
            else:
                current_y += 1

            screen.fill(BLACK)
            self.draw_grid(screen)
            self.draw_piece(screen, self.current_piece, self.current_color, current_x, current_y)
            self.draw_score(screen, font)

            if self.game_over:
                self.draw_game_over(screen, font)

            pygame.display.flip()
            clock.tick(5)

        pygame.quit()

if __name__ == "__main__":
    game = Tetris()
    game.run()
