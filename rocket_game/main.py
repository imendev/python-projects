import os
import pygame

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500

WIN = pygame.display.set_mode((900, 500))

pygame.display.set_caption('Rocket - game')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED= (255, 0, 0)
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

ROCKET_WIDTH, ROCKET_HIEGHT =55, 40

# event of yellow and red hit bullet
YELLOW_HIT = pygame.USEREVENT +1
RED_HIT = pygame.USEREVENT +2

BORDER = pygame.Rect(WIDTH // 2 -5, 0, 10, HEIGHT)

# Image import assets
YELLOW_ROCKET_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
RED_ROCKET_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

# Sound effect assets
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
# Resize and rotate the rockets
YELLOW_ROCKET = pygame.transform.rotate(pygame.transform.scale(YELLOW_ROCKET_IMAGE, (ROCKET_WIDTH, ROCKET_HIEGHT)), 90)
RED_ROCKET = pygame.transform.rotate(pygame.transform.scale(RED_ROCKET_IMAGE, (ROCKET_WIDTH, ROCKET_HIEGHT)), -90)

#Frame per second we want our game to update at
FPS = 60
SPEED = 5
SPEED_BULLET = 3
MAX_BULLETS = 4

# function for designing the game's window
def draw_window(red, yellow, red_ballets, yellow_ballets, red_health, yellow_health):

    #WIN.fill(WHITE)
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    # tHE tEXT 
    red_health_text = HEALTH_FONT.render("Health : "+ str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health : "+ str(yellow_health), 1, WHITE)

    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() -10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_ROCKET, (yellow.x, yellow.y))
    WIN.blit(RED_ROCKET, (red.x, red.y))

    for ballet in red_ballets:
        pygame.draw.rect(WIN, RED, ballet)

    for ballet in yellow_ballets:
        pygame.draw.rect(WIN, YELLOW, ballet)

    pygame.display.update()

# define the yellow rocket movement
def yellow_handle_movement(keys, yellow):
    if keys[pygame.K_l] and yellow.x -SPEED > 0: # when press L keyboard the rocket get to the LEFT 
        yellow.x -= SPEED
    if keys[pygame.K_r] and yellow.x +SPEED + yellow.width < BORDER.x : # when press R keyboard the rocket get to the RIGHT
        yellow.x += SPEED

    if keys[pygame.K_t] and yellow.y -SPEED > 0 : # when press T keyboard the rocket get to the TOP 
        yellow.y -= SPEED
    if keys[pygame.K_d] and yellow.y +SPEED + yellow.height < HEIGHT -10 : # when press D keyboard the rocket get to the BOTTOM
        yellow.y += SPEED

# define the red rocket movement 
def red_handle_movement(keys, red):
    if keys[pygame.K_LEFT] and red.x -SPEED > BORDER.x + BORDER.width : # LEFT 
        red.x -= SPEED
    if keys[pygame.K_RIGHT] and red.x +SPEED + red.width < WIDTH : # RIGHT
        red.x += SPEED

    if keys[pygame.K_UP] and red.y -SPEED > 0  : # TOP 
        red.y -= SPEED
    if keys[pygame.K_DOWN] and red.y +SPEED + red.height < HEIGHT -10 : # BOTTOM
        red.y += SPEED

# Through out the bullets
def handle_bullets(yellow_bullets, red_bullets, yellow, red):

    for bullet in yellow_bullets:
        bullet.x += SPEED_BULLET

        # the yellow ballet hit the red rocket
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= SPEED_BULLET

        # the red ballet hit the yellow rocket
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):

    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))

    pygame.display.update()
    pygame.time.delay(5000)


def main():
    yellow_bullets = []
    red_bullets = []

    red_health = 10
    yellow_health = 10

    yellow = pygame.Rect(100, 300, ROCKET_WIDTH, ROCKET_HIEGHT)
    red = pygame.Rect(700, 300, ROCKET_WIDTH, ROCKET_HIEGHT)

    clock = pygame.time.Clock()
    run = True
    while run:
        # Every 60s the game get updated
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:

                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height// 2 - 2, 10, 5 )
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:

                    bullet = pygame.Rect(red.x, red.y + red.height// 2 - 2, 10, 5 )
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:  
                yellow_health -= 1 
                BULLET_HIT_SOUND.play() 
        
        winner_text = ""
        if yellow_health <= 0:
            winner_text = "RED Wins!"

        if red_health <= 0:
            winner_text = "YELLOW Wins!"
        if winner_text != "":
           draw_winner(winner_text)
           break
        
        keys_pressed = pygame.key.get_pressed()

        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
    main()

if __name__ == "__main__" :
    main()   


