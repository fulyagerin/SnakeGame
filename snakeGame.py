#Documentation link: https://universitaetstgallen-my.sharepoint.com/:w:/g/personal/fulyanur_gerin_student_unisg_ch/EQUAubGzCFBOtL_Q4BjxFjQB3af7vwlwOwgOz70x6S2UvA?e=oWQYBq

#Libraries
import pygame
import sys
import random
from pygame.math import Vector2

#Initialize Pygame
pygame.init()

#Set up the display
title = pygame.font.Font(None, 60)
score = pygame.font.Font(None, 40)
highest_score_font = pygame.font.Font(None, 40)
game_over_font = pygame.font.Font(None, 80)

#Initialize variables
highest_score = 0

#Colors
GREEN = (173, 204, 96)
DARK_GREEN = (43, 51, 24)

#Set up the game (size)
cell_size = 25
number_of_cells = 20

OFFSET = 75

#Food functions
class Food:

    #Initialize the food
    def __init__(self, snake_body):
        self.position = self.set_random_food_position(snake_body)

    #Draw the food
    def draw_food(self):
        #Creating a rectangle object in Pygame, the position of the food is determined by self.position which is a Vector2 object containing 
        # the x and y coordinates of the food
        food_rect = pygame.Rect(OFFSET + self.position.x * cell_size, OFFSET + self.position.y * cell_size, cell_size, cell_size)
        #The rectangle object on the screen is visible by drawing it
        screen.blit(food_surface, food_rect)

    def generate_random_cell(self):
        #Generate a random cell in the grid
        x = random.randint(0, number_of_cells - 1)
        y = random.randint(0, number_of_cells - 1)
        #Return the random cell as a Vector2 object
        return Vector2(x, y)
    
    def set_random_food_position(self, snake_body):
        #Generate a random cell
        position = self.generate_random_cell()

        #Check if the random cell is in the snake's body
        while position in snake_body:
            position = self.generate_random_cell()
        #Return the random cell
        return position
        
class Snake:
    def __init__(self):
        #Set the initial position of the snake
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        #Set the initial direction of the snake
        self.direction = Vector2(1, 0)
        #Add a block to the snake
        self.add_block = False
        
    
    def draw_snake(self):
        #draw the snake
        for block in self.body:
            #Create a rectangle object in Pygame, the position of the snake is determined 
            # by the x and y coordinates of the block
            block_rect = (OFFSET + block.x * cell_size, OFFSET + block.y * cell_size, cell_size, cell_size)
            #The rectangle object on the screen is visible by drawing it
            pygame.draw.rect(screen, DARK_GREEN, block_rect, 0, 7)

    def update_snake(self):
        #Move the snake
        self.body.insert(0, self.body[0] + self.direction)
        #Check if the snake has eaten the food
        if self.add_block == True:
            self.add_block = False
        else:
            #If the snake has not eaten the food, remove the last block
            self.body = self.body[:-1]

    def reset_snake(self):
        #Reset the snake to its initial position
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)

class Game:
    def __init__(self):
        #Calling the Snake and Food classes
        self.snake = Snake()
        self.food = Food(self.snake.body)
        #State of the game
        self.state = "RUNNING"
        #Score value in the beginning of the game
        self.score_value = 0
        #Speed of the game in miliseconds
        self.speed = 180 

    def draw(self):
        #Draw the food and the snake
        self.food.draw_food()
        self.snake.draw_snake()

    def update(self):
        #When the game is running, update the snake
        if self.state == "RUNNING":
            #Initializing the game by updating the snake, checking for collision with food, edges and itself
            self.snake.update_snake()
            self.check_collision_with_food()
            self.check_collision_with_edges()
            self.check_collision_with_itself()

    def check_collision_with_food(self):
        #Check if the snake has eaten the food
        if self.snake.body[0] == self.food.position:
            self.food.position = self.food.set_random_food_position(self.snake.body)
            #If the snake has eaten the food, add a block to the snake and increase the score
            self.snake.add_block = True
            #Increase score by 1
            self.score_value += 1
            #After eating the food the speed of the game increases
            self.speed = max(120, self.speed - 6)  
            pygame.time.set_timer(SNAKE_UPDATE, self.speed)

    def check_collision_with_edges(self):
        #Check if the snake has collided with the edges of the screen
        if self.snake.body[0].x == number_of_cells or self.snake.body[0].x == -1:
            self.game_over()
        #Check if the snake has collided with itself on the screen
        if self.snake.body[0].y == number_of_cells or self.snake.body[0].y == -1:
            self.game_over()

    def game_over(self):
        #Reset the snake, food, state, score and speed
        self.snake.reset_snake()
        # Reset the food position
        self.food.position = self.food.set_random_food_position(self.snake.body)
        # Reset the state
        self.state = "STOPPED"
        # Reset the score
        self.score_value = 0
         # Reset speed to starting value
        self.speed = 180
        # Reset the timer
        pygame.time.set_timer(SNAKE_UPDATE, self.speed)  

        # Render "Game Over!" in large font
        game_over_surface = game_over_font.render("GAME OVER!", True, DARK_GREEN)
        screen.blit(game_over_surface, (OFFSET + 75, OFFSET + number_of_cells * cell_size // 2 - 40))
        
        # Render replay instructions
        replay_surface = score.render("Press any key to restart", True, DARK_GREEN)
        screen.blit(replay_surface, (OFFSET + 93, OFFSET + number_of_cells * cell_size // 2 + 30))

        
    def check_collision_with_itself(self):
        #Check if the snake has collided with itself
        headless_body = self.snake.body[1:]
        #If the head of the snake is in the body of the snake, the game is over
        if self.snake.body[0] in headless_body:
            self.game_over()

#Set up the screen
screen = pygame.display.set_mode((2*OFFSET + cell_size * number_of_cells, 2*OFFSET+cell_size * number_of_cells))

#Set up the caption
pygame.display.set_caption("Sneak Game")

#Set up the clock
clock = pygame.time.Clock()

#Set up the game
game = Game()
#Load image of the food 
food_surface = pygame.image.load("apple.png")
#Scale the image of the food
food_surface = pygame.transform.scale(food_surface, (cell_size, cell_size))

#Set up the timer
SNAKE_UPDATE = pygame.USEREVENT
#Set up the timer to update the snake
pygame.time.set_timer(SNAKE_UPDATE, 200)

while True:
    #Check for events
    for event in pygame.event.get():
        #When the event is to update the snake and the game is running, update the game
        if event.type == SNAKE_UPDATE and game.state == "RUNNING":
            game.update()
        #When the event is to quit the game, quit the game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #When the event is a key press and the game is stopped, start the game
        if event.type == pygame.KEYDOWN:

            if game.state == "STOPPED": 
                game.state = "RUNNING"
            #When the event is a key press, change the direction of the snake to the direction of the key press
            if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
                game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
                game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
                game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
                game.snake.direction = Vector2(1, 0)

    #Fill the screen with the color green
    screen.fill(GREEN)
    #Draw a rectangle around the screen
    pygame.draw.rect(screen, DARK_GREEN, (OFFSET-5, OFFSET-5, cell_size * number_of_cells+10, cell_size * number_of_cells+10), 5)

    #When the the game is running and the score is higher than the highest score, update the highest score
    if game.state == "RUNNING":
        #Compare the score with the highest score
        if game.score_value > highest_score:
            #Initialize the new highest score
            highest_score = game.score_value

        #Draw the game
        game.draw()
        #Render the title, score 
        title_surface = title.render("Snake Game", True, DARK_GREEN)
        #Render the score 
        score_surface = score.render("Score: " + str(game.score_value), True, DARK_GREEN)
        #Render the highest score
        highest_score_surface = highest_score_font.render("Highest Score: " + str(highest_score), True, DARK_GREEN)

        #Display the title, score and highest score on the screen
        screen.blit(title_surface, (OFFSET-5, 20))
        screen.blit(score_surface, (OFFSET-5, OFFSET + cell_size * number_of_cells + 10))
        screen.blit(highest_score_surface, (OFFSET-5, OFFSET + cell_size * number_of_cells + 40))
    
    #When the game is stopped, display the game over message
    elif game.state == "STOPPED":
        # Show Game Over message
        game.game_over()  

    #Update the display
    pygame.display.update()
    #Set the frames per second
    clock.tick(60)
