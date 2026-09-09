import pygame
import random

pygame.init()

# Constants
BLOCK_SIZE = 30 # Tamaño de cada bloque en pixeles
GRID_WIDTH = 10 # Ancho del tablero en bloques
GRID_HEIGHT = 20 # Alto del tablero en bloques
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 8) # Espacio extra para siguiente pieza y puntaje
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 128, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (255, 0, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

#Forms
SHAPES = [
    [[1, 1, 1, 1]],           #I
    [[1, 0, 0],[1, 1, 1]],    #J
    [[0, 0, 1],[1, 1, 1]],    #L
    [[1, 1], [1, 1]],         #O
    [[0, 1, 1],[1, 1, 0]],    #S
    [[0, 1, 0],[1, 1, 1]],    #T
    [[1, 1, 0],[0, 1, 1]]     #Z
]

COLORS = [CYAN, BLUE, ORANGE, YELLOW, GREEN, PURPLE, RED]

class Tetromino:
    def __init__(self):
        self.shape_idx = random.randint(0, len(SHAPES) - 1)
        self.shape = [row[:] for row in SHAPES[self.shape_idx]]
        self.color = COLORS[self.shape_idx]
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
    def rotate(self):
        self.shape = [[self.shape[y][x] for y in range(len(self.shape) -1, -1, -1)]
                      for x in range(len(self.shape[0]))]

class TetrisGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = Tetromino()
        self.next_piece = Tetromino()
        self.game_over = False
        self.score = 0
        self.fall_time = 0
        self.fall_speed = 500
        self.font = pygame.font.SysFont("Arial", 36)

    def valid_move(self, piece, x, y):
        for i in range(len(piece.shape)):
            for j in range(len(piece.shape[i])):
                if piece.shape[i][j]:
                    if (x + j < 0 or x + j >= GRID_WIDTH or
                            y + i >= GRID_HEIGHT or
                            (y + i >= 0 and self.grid[y + i][x + j] != BLACK)):
                        return False
        return True

    def lock_piece(self):
        for i in range(len(self.current_piece.shape)):
            for j in range(len(self.current_piece.shape[i])):
                if self.current_piece.shape[i][j]:
                    if self.current_piece.y + i <= 0:
                        self.game_over = True
                        return
                    self.grid[self.current_piece.y + i][self.current_piece.x + j] = self.current_piece.color

        if not self.game_over:
            self.clear_lines()
            self.current_piece = self.next_piece
            self.next_piece = Tetromino()

            # Verificar si la nueva pieza puede entrar en el tablero
            for i in range(len(self.current_piece.shape)):
                for j in range(len(self.current_piece.shape[i])):
                    if (self.current_piece.shape[i][j] and
                        self.grid[self.current_piece.y + i][self.current_piece.x + j] != BLACK):
                        self.game_over = True
                        return

    def clear_lines(self):
        lines_cleared = 0
        for i in range(len(self.grid)):
            if all(cell != BLACK for cell in self.grid[i]):
                lines_cleared += 1
                del self.grid[i]
                self.grid.insert(0, [BLACK for _ in range(GRID_WIDTH)])
            if lines_cleared:
                self.score += (100 * lines_cleared)

    def draw_grid(self):
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                pygame.draw.rect(self.screen, self.grid[i][j],
                                 (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(self.screen, GRAY,
                                 (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

        for i in range(len(self.current_piece.shape)):
            for j in range(len(self.current_piece.shape[i])):
                if self.current_piece.shape[i][j]:
                    pygame.draw.rect(self.screen, self.current_piece.color,
                                     ((self.current_piece.x + j) * BLOCK_SIZE,
                                      (self.current_piece.y + i) * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE))
        next_piece_text = self.font.render('Siguiente:', True, WHITE)
        self.screen.blit(next_piece_text, (GRID_WIDTH * BLOCK_SIZE + 20, 20))
        for i in range(len(self.next_piece.shape)):
            for j in range(len(self.next_piece.shape[i])):
                if self.next_piece.shape[i][j]:
                    pygame.draw.rect(self.screen, self.next_piece.color,
                                     (GRID_WIDTH * BLOCK_SIZE + 20 + j * BLOCK_SIZE,
                                      80 + i * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE))

        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (GRID_WIDTH * BLOCK_SIZE + 20, 200))

    def run(self):
        while not self.game_over:
            self.fall_time += self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.valid_move(self.current_piece, self.current_piece.x - 1, self.current_piece.y):
                            self.current_piece.x -= 1
                    elif event.key == pygame.K_RIGHT:
                        if self.valid_move(self.current_piece, self.current_piece.x + 1, self.current_piece.y):
                            self.current_piece.x += 1
                    elif event.key == pygame.K_DOWN:
                        if self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y + 1):
                            self.current_piece.y += 1
                    elif event.key == pygame.K_UP:
                        original_shape = [row[:] for row in self.current_piece.shape]
                        self.current_piece.rotate()
                        if not self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y):
                            self.current_piece.shape = original_shape

            if self.fall_time >= self.fall_speed:
                if self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y + 1):
                    self.current_piece.y += 1
                else:
                    self.lock_piece()
                self.fall_time = 0

            self.screen.fill(BLACK)
            self.draw_grid()
            pygame.display.flip()

        game_over = True
        self.screen.fill(BLACK)
        self.draw_grid()

        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                    game_over = False

            dark_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            dark_surface.fill(BLACK)
            dark_surface.set_alpha(128)
            self.screen.blit(dark_surface, (0, 0))

            # Mostrar mensaje de Game Over
            game_over_text = self.font.render('Game Over!', True, WHITE)
            score_text = self.font.render(f'Score Final: {self.score}', True, WHITE)
            continue_text = self.font.render('Presione X para salir', True, WHITE)

            # Posicionar textos
            text_y = SCREEN_HEIGHT // 2 - 60
            for text in [game_over_text, score_text, continue_text]:
                text_x = SCREEN_WIDTH // 2 - text.get_width() // 2
                self.screen.blit(text, (text_x, text_y))
                text_y += 40
            pygame.display.flip()

        # Oscurecer el fondo
        dark_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        dark_surface.fill(BLACK)
        dark_surface.set_alpha(128)
        self.screen.blit(dark_surface, (0, 0))

if __name__ == '__main__':
    game = TetrisGame()
    game.run()
    pygame.quit()

