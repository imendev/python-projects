import random
import time
import pygame
from queue import Queue


pygame.init()
pygame.font.init()

WIDTH , HEIGHT = 750, 900

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping-pong Game")

# FONT TYPE
NUM_FONT = pygame.font.SysFont('comicsans', 20)
WIN_FONT = pygame.font.SysFont('comicsans', 50)
SCORE_FONT = pygame.font.SysFont('Arial', 20)

# THE COLOR CODE 
BG_COLOR = "white"
# Frame per second
FPS = 60
# PADDLE PARAMS
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
WINNING_SCORE = 10

# DEFINE THE PADDLE CLASS
class Paddle:

    COLOR = (0, 0, 0)
    VEL = 4 # THE VELOCITY

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
    
    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))
    
    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL
    
    def reset(self):

        self.x = self.original_x
        self.y = self.original_y

# DEFINE THE CLASS BALL
class Ball:

    MAX_VEL = 5
    COLOR = (0, 0, 0)

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0
    
    def draw(self, window):

        pygame.draw.circle(window, self.COLOR, (self.x, self.y), self.radius)
    
    def move(self):

        self.x += self.x_vel
        self.y += self.y_vel
    
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1

def draw(window, paddles, ball, left_score, right_score):
    window.fill(BG_COLOR)

    # DRAW THE SCORE
    left_score_text = SCORE_FONT.render(f"Score: {left_score}", 1, "black")
    right_score_text = SCORE_FONT.render(f"Score: {right_score}", 1, "black")
    window.blit(left_score_text, (20, 10))
    window.blit(right_score_text, (WIDTH -right_score_text.get_width()*2 , 10))
    
    for paddle in paddles:
        paddle.draw(window)
    
    for i in range(7, HEIGHT, HEIGHT//20):
        if i % 2 == 0:
            continue
        pygame.draw.rect(window, "black", (WIDTH//2 -5, i, 5, HEIGHT//20))

    ball.draw(window)

    pygame.display.update()

def handle_paddle_movement(keys, left_paddle, right_paddle):

    
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.height < HEIGHT -5:
        right_paddle.move(up=False)
    if keys[pygame.K_UP] and right_paddle.y > 5:
        right_paddle.move(up=True)
    
    if keys[pygame.K_w] and left_paddle.y + left_paddle.height  < HEIGHT -5:
        left_paddle.move(up=False)
    if keys[pygame.K_s] and left_paddle.y > 5:
        left_paddle.move(up=True)
# DEFINE THE COLLISION BETWEEN BALL AND PADDLE
def handle_collision(ball, left_paddle, right_paddle):
    # THE BALL IS OUT OF THE SCREEN
    if ball.y + ball.radius >= HEIGHT:
        # REVERSE THE DIRECTION OF THE BALL
        ball.y_vel *= -1
        # WHEN THE BALL IS UNDER 0 (THE TOP)
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1 # ball.y_vel is negative here, so we multiply by -1 for being positive and change the direction 
    # CHECK THE DIRECTION OF THE BALL HORIZONTALLY <----O---->
    if ball.x_vel < 0:
        
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factory = (left_paddle.height /2) / ball.MAX_VEL

                y_vel = difference_in_y / reduction_factory
                ball.y_vel = -1*y_vel


    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factory = (right_paddle.height /2) / ball.MAX_VEL

                y_vel = difference_in_y / reduction_factory
                ball.y_vel = -1*y_vel


def main():
    run = True

    clock = pygame.time.Clock()

    left_paddle  = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

    ball = Ball(WIDTH //2, HEIGHT //2, 15)

    left_score = 0
    right_score = 0
    
    while run:
        
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
            
        draw(win, [left_paddle, right_paddle], ball, left_score, right_score)
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_score += 1
            ball.reset()
        if ball.x > WIDTH:
            left_score += 1
            ball.reset()
        
        won = False
        if right_score >= WINNING_SCORE:
            won = True
            win_text = "Right player won !"
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Left player won !"
        
        if won:
            text = WIN_FONT.render(win_text, 1, "green")
            win.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height() //2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            right_paddle.reset()
            left_paddle.reset()
            right_score = 0
            left_score = 0
            
    
    pygame.quit()

if __name__ == "__main__":
    main()