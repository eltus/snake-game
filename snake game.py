import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
FPS = 10

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (192, 192, 192)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Snake class
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % WIDTH), (cur[1] + (y * GRID_SIZE)) % HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            return True  # Game over
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
            return False

    def reset(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    def render(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0], p[1], GRID_SIZE, GRID_SIZE))

# Fruit class
class Fruit:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (WIDTH // GRID_SIZE - 1)) * GRID_SIZE,
                         random.randint(0, (HEIGHT // GRID_SIZE - 1)) * GRID_SIZE)

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))

# Game Over screen
def show_game_over_screen(surface, score):
    font = pygame.font.SysFont(None, 36)
    text1 = font.render("Game Over", True, GRAY)
    text2 = font.render(f"Your Score: {score}", True, GRAY)
    text3 = font.render("Press R to Restart", True, GRAY)
    surface.blit(text1, (WIDTH // 3, HEIGHT // 3))
    surface.blit(text2, (WIDTH // 3, HEIGHT // 2))
    surface.blit(text3, (WIDTH // 4, HEIGHT * 2 // 3))

# Main function
def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    snake = Snake()
    fruit = Fruit()

    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if snake.direction != DOWN:
                        snake.direction = UP
                elif event.key == pygame.K_DOWN:
                    if snake.direction != UP:
                        snake.direction = DOWN
                elif event.key == pygame.K_LEFT:
                    if snake.direction != RIGHT:
                        snake.direction = LEFT
                elif event.key == pygame.K_RIGHT:
                    if snake.direction != LEFT:
                        snake.direction = RIGHT
                elif event.key == pygame.K_r and game_over:
                    snake.reset()
                    fruit.randomize_position()
                    game_over = False

        if not game_over:
            game_over = snake.update()

            if snake.get_head_position() == fruit.position:
                snake.length += 1
                snake.score += 1
                fruit.randomize_position()

            surface.fill(WHITE)
            snake.render(surface)
            fruit.render(surface)
        else:
            surface.fill(WHITE)
            show_game_over_screen(surface, snake.score)

        screen.blit(surface, (0, 0))
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
