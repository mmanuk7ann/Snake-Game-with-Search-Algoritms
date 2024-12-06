import pygame
from pygame.locals import *
import time
import random
from collections import deque
from queue import PriorityQueue

SIZE = 40
BACKGROUND_COLOR = (105, 163, 47)


class Apple:
    def __init__(self, parent_screen) -> None:
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.move()
    
    def draw(self):
        self.parent_screen.blit(self.image,(self.x, self.y))
        pygame.display.flip()

    def move(self):
        snake_body = set(zip(self.parent_screen.snake.x, self.parent_screen.snake.y))  # Get the snake's body as a set of tuples
        while True:
            self.x = random.randint(0, 23) * SIZE
            self.y = random.randint(0, 18) * SIZE
            if (self.x, self.y) not in snake_body:  # Ensure the new position is not in the snake's body
                break



class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.length = length
        self.x = [random.randint(0, 24) * SIZE] * length
        self.y = [random.randint(0, 19) * SIZE] * length
        self.direction = random.choice(["down", "up", "left", "right"])

    def draw(self):
        self.parent_screen.fill(BACKGROUND_COLOR)
        for i in range(self.length):
            self.parent_screen.blit(self.block,(self.x[i], self.y[i]))
        pygame.display.flip()

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "up":
            self.y[0] -= SIZE
        if self.direction == "down":
            self.y[0] += SIZE
        if self.direction == "left":
            self.x[0] -= SIZE
        if self.direction == "right":
            self.x[0] += SIZE
        
        #Allows Snake to go through walls
        # self.x[0] %= 1000 
        # self.y[0] %= 800
        
        self.draw()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.surface = pygame.display.set_mode((1000, 800))
        self.surface.fill(BACKGROUND_COLOR)
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.is_algorithm_mode = "manual"  # Default to user control
        self.start_game_mode()  # Prompt for mode selection at the start

    

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def heuristic(self, snake_x, snake_y, apple_x, apple_y):
        """Calculate Manhattan distance between the snake's head and the apple."""
        return abs(snake_x - apple_x) + abs(snake_y - apple_y)
    
   
    def greedy_move(self):
        """Determine the best move based on the Greedy algorithm."""
        head_x, head_y = self.snake.x[0], self.snake.y[0]
        apple_x, apple_y = self.apple.x, self.apple.y

        # Calculate Manhattan distance for all possible moves
        moves = {
            "up": self.heuristic(head_x, head_y - SIZE, apple_x, apple_y),
            "down": self.heuristic(head_x, head_y + SIZE, apple_x, apple_y),
            "left": self.heuristic(head_x - SIZE, head_y, apple_x, apple_y),
            "right": self.heuristic(head_x + SIZE, head_y, apple_x, apple_y),
        }

        best_move = min(moves, key=moves.get)

        # Update the snake's direction
        if best_move == "up" and self.snake.direction != "down":
            self.snake.move_up()
        elif best_move == "down" and self.snake.direction != "up":
            self.snake.move_down()
        elif best_move == "left" and self.snake.direction != "right":
            self.snake.move_left()
        elif best_move == "right" and self.snake.direction != "left":
            self.snake.move_right()


    def a_star_move(self):
        start = (self.snake.x[0], self.snake.y[0])
        goal = (self.apple.x, self.apple.y)

        open_list = {start: (0, [])}  # {node: (f_cost, path)}
        visited = set()
        body_nodes = set(zip(self.snake.x[1:], self.snake.y[1:]))

        directions = {
            "up": (0, -SIZE),
            "down": (0, SIZE),
            "left": (-SIZE, 0),
            "right": (SIZE, 0),
        }

        while open_list:
            # Find the node with the lowest f_cost
            current, (f_cost, path) = min(open_list.items(), key=lambda x: x[1][0])
            del open_list[current]

            if current == goal:
                if path:
                    next_direction = path[0]
                    if next_direction == "up":
                        self.snake.move_up()
                    elif next_direction == "down":
                        self.snake.move_down()
                    elif next_direction == "left":
                        self.snake.move_left()
                    elif next_direction == "right":
                        self.snake.move_right()
                return

            visited.add(current)

            for direction, (dx, dy) in directions.items():
                neighbor = (current[0] + dx, current[1] + dy)

                # Validate move
                if not (0 <= neighbor[0] < 1000 and 0 <= neighbor[1] < 800):
                    continue
                if neighbor in visited or neighbor in body_nodes:
                    continue

                g_cost = len(path) + 1
                h_cost = abs(neighbor[0] - goal[0]) + abs(neighbor[1] - goal[1])
                f_cost = g_cost + h_cost

                # Update the open list
                if neighbor not in open_list or open_list[neighbor][0] > f_cost:
                    open_list[neighbor] = (f_cost, path + [direction])





    def dfs_move(self):
        visited = set()
        stack = deque([(self.snake.x[0], self.snake.y[0], self.snake.direction)])

        while stack:
            x, y, direction = stack.pop()
            if (x, y) in visited:
                continue
            visited.add((x, y))

            if x == self.apple.x and y == self.apple.y:
                self.snake.direction = direction
                return

            for new_direction, (dx, dy) in [("up", (0, -SIZE)), ("down", (0, SIZE)), ("left", (-SIZE, 0)), ("right", (SIZE, 0))]:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < 1000 and 0 <= new_y < 800 and (new_x, new_y) not in visited:
                    stack.append((new_x, new_y, new_direction))

 
    def check_corner_collision(self):
        head_x, head_y = self.snake.x[0], self.snake.y[0]
        screen_width = 1000
        screen_height = 800

        # Check if the snake's head is at any of the edge points, including the exact boundaries
        if head_x < 0 or head_x >= screen_width:  # Left or right edges
            return True

        if head_y < 0 or head_y >= screen_height:  # Top or bottom edges
            return True   

        return False



    
    def play(self):
        """Play the game where the user controls the snake."""
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()
        
        if self.check_corner_collision():
            raise Exception("Game Over")

        # Check collision with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increase_length()
            self.apple.move()
        
        # Check collision with itself (only if snake length > 3)
        if self.snake.length > 3:
            for i in range(3, self.snake.length):
                if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                    raise Exception()

    def play_algorithm(self):
        """Play the game using the Greedy algorithm."""
        if self.is_algorithm_mode == "greedy":
            self.greedy_move()
        if self.is_algorithm_mode == "dfs":
            self.dfs_move()
        if self.is_algorithm_mode == "a*":
            self.a_star_move()
        
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        
        if self.check_corner_collision():
            raise Exception("Game Over") 


        # Check collision with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increase_length()
            self.apple.move()
        
        # Check collision with itself (only if snake length > 3)
        if self.snake.length > 3:
            for i in range(3, self.snake.length):
                if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                    raise Exception("Game Over")


    def handle_user_input(self, event):
            """Handle user input to control snake's movement."""
            if event.key == K_UP and self.snake.direction != "down":
                self.snake.move_up()
            elif event.key == K_DOWN and self.snake.direction != "up":
                self.snake.move_down()
            elif event.key == K_LEFT and self.snake.direction != "right":
                self.snake.move_left()
            elif event.key == K_RIGHT and self.snake.direction != "left":
                self.snake.move_right()

    def reset(self):
            """Reset the game."""
            self.snake = Snake(self.surface, 1)
            self.apple = Apple(self.surface)

    def run(self):
            """Main game loop."""
            running = True
            pause = False

            while running:
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            running = False
                        elif event.key == K_RETURN:
                            pause = False
                        elif not pause and self.is_algorithm_mode == "manual":
                            self.handle_user_input(event)  # Only process user input when not in algorithm mode
                    elif event.type == QUIT:
                        running = False

                try:
                    if not pause:
                        if self.is_algorithm_mode == "manual":
                            self.play()  # User controls the snake
                        elif self.is_algorithm_mode == "greedy":
                            self.play_algorithm()  # Greedy algorithm controls the snake
                        elif self.is_algorithm_mode == "dfs":
                            self.play_algorithm() 
                        elif self.is_algorithm_mode == "a*":
                            self.play_algorithm() 
                except Exception as e:
                    self.show_game_over()
                    pause = True
                    self.reset()

                time.sleep(0.09)

    def display_score(self):
            font = pygame.font.SysFont("arial", 30)
            score = font.render(f"Score: {self.snake.length - 1}", True, (5, 5, 5))  # Display score as length - 1
            self.surface.blit(score, (800, 10))

    def start_game_mode(self):
        """Ask the user to choose between manual control or the Greedy algorithm."""
        # Set the background color for the start screen
        self.surface.fill((50, 50, 150))  # A different color, e.g., dark blue
        pygame.display.flip()

        # Define font and render multi-line text
        font = pygame.font.SysFont("arial", 30)
        line1 = font.render("Press Enter to Play Manually", True, (255, 255, 255))
        line2 = font.render("Press G to Play with Greedy", True, (255, 255, 255))
        line3 = font.render("Press D to Play with DFS", True, (255, 255, 255))
        line4 = font.render("Press A to Play with A*", True, (255, 255, 255))

        # Display the text on separate lines
        self.surface.blit(line1, (250, 350)) 
        self.surface.blit(line2, (250, 400))  
        self.surface.blit(line3, (250, 450))
        self.surface.blit(line4, (250, 500))
        pygame.display.flip()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:  # User chooses to play manually
                        self.is_algorithm_mode = "manual"
                        waiting_for_input = False
                    elif event.unicode == "g":  # User chooses to play using Greedy search
                        self.is_algorithm_mode = "greedy"
                        waiting_for_input = False
                    elif event.unicode == "d":  
                        self.is_algorithm_mode = "dfs"
                        waiting_for_input = False
                    elif event.unicode == "a":  
                        self.is_algorithm_mode = "a*"
                        waiting_for_input = False
                elif event.type == QUIT:
                    waiting_for_input = False

    def show_game_over(self):
            self.surface.fill((9, 33, 84))
            font = pygame.font.SysFont("arial", 30)
            line1 = font.render(f"Game Over! Your score is {self.snake.length - 1}", True, (255, 255, 255))
            self.surface.blit(line1, (200, 300))
            line2 = font.render("To play again, press Enter. To exit, press Escape!", True, (255, 255, 255))
            self.surface.blit(line2, (200, 350))
            pygame.display.flip()



    


if __name__ == "__main__":
    game = Game()
    game.run()

    
    

    
    
    
     
    
    

    
