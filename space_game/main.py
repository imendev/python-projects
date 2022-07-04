import os
import random
import emoji
from matplotlib.pyplot import title
import pygame
from regex import B

# INIT THE FONT 
pygame.font.init()

# SET UP THE WINDOW
WIDTH, HEIGHT = 500, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SHIP SPACE WAR ")
# LOAD IMAGES

READ_SHIP_SPACE = pygame.image.load(os.path.join('assets', 'pixel_ship_red_small.png'))
GREEN_SHIP_SPACE = pygame.image.load(os.path.join('assets', 'pixel_ship_green_small.png'))
BLUE_SHIP_SPACE = pygame.image.load(os.path.join('assets', 'pixel_ship_blue_small.png'))

# THE PLAYER SHIP SPACE
YELLOW_SHIP_SPACE = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'pixel_ship_yellow.png')), (90, 100))

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background-black.png')), (WIDTH, HEIGHT))

# THE LASERS
BLUE_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_blue.png'))
GREEN_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_green.png'))
RED_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_red.png'))
YELLOW_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_yellow.png'))

# FONT FOR TEXT
MAIN_FONT = pygame.font.SysFont("comicsans", 20)
LOST_FONT = pygame.font.SysFont("comicsans", 50)
# Colour code
WHITE = (255, 255, 255)

# DEFINE LASER CLASS 
class Laser:

    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    
    def move(self, speed):
        self.y += speed
    
    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

# DEFINE SHIP CLASS 
class Ship:

    COOLDOWN = 30

    def __init__(self, x, y, health= 100):
        self.x = x
        self.y =y
        self.health = health
        self.ship_image = None
        self.ship_laser = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        #pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, 50, 50))
        window.blit(self.ship_image, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
    
    def move_lasers(self, speed, obj):

        self.cooldown()
        for laser in self.lasers:
            laser.move(speed)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)


    

    def cooldown(self):

        if self.cool_down_counter >= self.COOLDOWN:

            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:

            self.cool_down_counter += 1    
    
    def shoot(self):

        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.ship_laser)
            self.lasers.append(laser)
            self.cool_down_counter = 1
    
    def get_width(self):
        
        return self.ship_image.get_width()

    def get_height(self):

        return self.ship_image.get_height()

# DEFINE THE PLAYER CLASS WHO EXTENDS THE SHIP 
class Player(Ship):

    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_image = YELLOW_SHIP_SPACE
        self.ship_laser = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_image) # Tell us where the pixels of the images are located
        self.max_health = health

    def move_lasers(self, speed, objs):

        self.cooldown()
        for laser in self.lasers:
            laser.move(speed)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_image.get_height() + 2, self.ship_image.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_image.get_height() + 2, self.ship_image.get_width() * (self.health/self.max_health), 10))

# DEFINE THE ENEMY SHIP WHO EXTENDS THE SHIP*
class Enemy(Ship):

    COLOR_MAP = {
        "red": (READ_SHIP_SPACE, RED_LASER),
        "green": (GREEN_SHIP_SPACE, GREEN_LASER),
        "blue": (BLUE_SHIP_SPACE, BLUE_LASER)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_image, self.ship_laser = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_image)

    def move(self, speed):
        self.y += speed # speed is the number of pixels that the ship enemy could do from top to bottom so we increase y

    def shoot(self):

        if self.cool_down_counter == 0:
            laser = Laser(self.x -20, self.y, self.ship_laser)
            self.lasers.append(laser)
            self.cool_down_counter = 1

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x 
    offset_y = obj2.y - obj1.y

    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():

    run = True
    FPS = 60 # Frame per second that's means the game is under control 6 times per second
    clock = pygame.time.Clock()

    level = 1
    lives = 5

    lost = False
    lost_count = 0

    speed_player = 5

    enemies = []
    waves_length = 5
    speed_enemy = 1
    speed_laser = 4

    # Instanciate a ship
    player = Player(WIDTH //2 -5 , HEIGHT - 120 )

    def draw_window():

        WIN.blit(BACKGROUND, (0,0))

        #draw text inside the window
        level_label = MAIN_FONT.render(f"Level: {level}", 1, WHITE)
        lives_label = MAIN_FONT.render(f"Lives: {lives}", 1, WHITE)
        

        WIN.blit(level_label, (WIDTH - level_label.get_width() -5, 10))
        WIN.blit(lives_label, (5, 10))

        if lost:
            msg = emoji.emojize('YOU LOST :grimacing:', language="en")
            print(msg)
            lost_label = LOST_FONT.render(msg, 1, WHITE)
            WIN.blit(lost_label, (WIDTH /2 - lost_label.get_width() /2, HEIGHT /2 - lost_label.get_height()))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        pygame.display.update()

    while run :

        clock.tick(FPS) # set the clock speed, the game run faster no matter the OS will be. 
        draw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS *3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level +=1
            waves_length += 5
            for i in range(waves_length):
                enemy = Enemy(random.randrange(50, WIDTH -100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]) )
                enemies.append(enemy)

        for event in  pygame.event.get():

            if event.type == pygame.QUIT:
                quit()
                print("Cio baby <3 !")

            if event.type == pygame.KEYDOWN:
                print('READY TO PLAY !')

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player.y > 0:
            player.y -= speed_player
        if keys[pygame.K_DOWN] and player.y + speed_player + player.get_height() +15 < HEIGHT:
            player.y += speed_player
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= speed_player
        if keys[pygame.K_RIGHT] and player.x + player.get_width() < WIDTH:
            player.x += speed_player  
        
        if keys[pygame.K_SPACE]:
            player.shoot()
        
        for enemy in enemies[:]:
            enemy.move(speed_enemy)
            enemy.move_lasers (speed_laser,player)

            # THE ENEMY SHOOTS
            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
            
            

        player.move_lasers(- speed_laser, enemies) # the - speed_laser for lser be shooted from bottom to top

# DEFINE THE MAIN MENU
def main_menu():
    
    title_font = pygame.font.SysFont('comicsans', 20)
    run = True
    while run:

        WIN.blit(BACKGROUND, (0,0))
        title_label = title_font.render('Press the mouse key dow to start ...', 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    
    pygame.quit()
        

if __name__ == "__main__":
    main_menu()
