import pygame
import sys
import random
from pygame.math import Vector2


pygame.init()

title = pygame.font.Font(None, 60)
score = pygame.font.Font(None, 40)
highest_score_font = pygame.font.Font(None, 40)
game_over_font = pygame.font.Font(None, 80)

highest_score = 0

GREEN = (173, 204, 96)
DARK_GREEN = (43, 51, 24)

cell_size = 25
number_of_cells = 20

OFFSET = 75

class Food:
    def __init__(self, snake_body):
        self.position = self.set_random_food_position(snake_body)

    def draw_food(self):
        food_rect = pygame.Rect(OFFSET + self.position.x * cell_size, OFFSET + self.position.y * cell_size, cell_size, cell_size)
        # pygame.draw.rect(screen, DARK_GREEN, food_rect)
        screen.blit(food_surface, food_rect)

    def generate_random_cell(self):
        x = random.randint(0, number_of_cells - 1)
        y = random.randint(0, number_of_cells - 1)
        return Vector2(x, y)
    
    def set_random_food_position(self, snake_body):
        position = self.generate_random_cell()
        while position in snake_body:
            position = self.generate_random_cell()
        return position
        
class Snake:
    def __init__(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)
        self.add_block = False
        
    
    def draw_snake(self):
        for block in self.body:
            block_rect = (OFFSET + block.x * cell_size, OFFSET + block.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, DARK_GREEN, block_rect, 0, 7)

    def update_snake(self):
        self.body.insert(0, self.body[0] + self.direction)
        if self.add_block == True:
            self.add_block = False
        else:
            self.body = self.body[:-1]

    def reset_snake(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = "RUNNING"
        self.score_value = 0
        self.speed = 200  # Initial speed in milliseconds

    def draw(self):
        self.food.draw_food()
        self.snake.draw_snake()

    def update(self):
        if self.state == "RUNNING":
            self.snake.update_snake()
            self.check_collision_with_food()
            self.check_collision_with_edges()
            self.check_collision_with_itself()

    def check_collision_with_food(self):
        if self.snake.body[0] == self.food.position:
            self.food.position = self.food.set_random_food_position(self.snake.body)
            self.snake.add_block = True
            self.score_value += 1
            
            # Adjust speed (lower interval = faster game)
            self.speed = max(50, self.speed - 10)  # Decrease by 10ms, minimum 50ms
            pygame.time.set_timer(SNAKE_UPDATE, self.speed)

    def check_collision_with_edges(self):
        if self.snake.body[0].x == number_of_cells or self.snake.body[0].x == -1:
            self.game_over()
        if self.snake.body[0].y == number_of_cells or self.snake.body[0].y == -1:
            self.game_over()

    def game_over(self):
        self.snake.reset_snake()
        self.food.position = self.food.set_random_food_position(self.snake.body)
        self.state = "STOPPED"
        self.score_value = 0
        self.speed = 200  # Reset speed to starting value
        pygame.time.set_timer(SNAKE_UPDATE, self.speed)  # Reset the timer

        # Render "Game Over!" in large font
        game_over_surface = game_over_font.render("GAME OVER!", True, DARK_GREEN)
        screen.blit(game_over_surface, (OFFSET + 75, OFFSET + number_of_cells * cell_size // 2 - 40))
        
        # Render replay instructions
        replay_surface = score.render("Press any key to restart", True, DARK_GREEN)
        screen.blit(replay_surface, (OFFSET + 93, OFFSET + number_of_cells * cell_size // 2 + 30))

        
    def check_collision_with_itself(self):
        headless_body = self.snake.body[1:]
        if self.snake.body[0] in headless_body:
            self.game_over()


screen = pygame.display.set_mode((2*OFFSET + cell_size * number_of_cells, 2*OFFSET+cell_size * number_of_cells))

pygame.display.set_caption("Sneak Game")

clock = pygame.time.Clock()

game = Game()
food_surface = pygame.image.load("apple.png")
food_surface = pygame.transform.scale(food_surface, (cell_size, cell_size))


SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 200)

while True:
    for event in pygame.event.get():
        if event.type == SNAKE_UPDATE and game.state == "RUNNING":
            game.update()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if game.state == "STOPPED":  # Restart game on key press
                game.state = "RUNNING"
            if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
                game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
                game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
                game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
                game.snake.direction = Vector2(1, 0)

    screen.fill(GREEN)
    pygame.draw.rect(screen, DARK_GREEN, (OFFSET-5, OFFSET-5, cell_size * number_of_cells+10, cell_size * number_of_cells+10), 5)

    if game.state == "RUNNING":
        if game.score_value > highest_score:
            highest_score = game.score_value

        game.draw()
        title_surface = title.render("Snake Game", True, DARK_GREEN)
        score_surface = score.render("Score: " + str(game.score_value), True, DARK_GREEN)
        highest_score_surface = highest_score_font.render("Highest Score: " + str(highest_score), True, DARK_GREEN)

        screen.blit(title_surface, (OFFSET-5, 20))
        screen.blit(score_surface, (OFFSET-5, OFFSET + cell_size * number_of_cells + 10))
        screen.blit(highest_score_surface, (OFFSET-5, OFFSET + cell_size * number_of_cells + 40))
    elif game.state == "STOPPED":
        # Show Game Over message
        game.game_over()  # Render Game Over and Replay Message

    pygame.display.update()
    clock.tick(60)

    #TODO: Add a game over screen with a replay button
    #TODO: Add a high score feature
    #TODO: Fasten the game speed as the score increases
