import math
import pygame

pygame.init()
# DEFINE THE WINDOW
WIDTH, HEIGHT = 750, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("-- Planet Simulation --")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (188, 39, 50)
DARK_GREY = (169,169,169)
DARK_BLUE = ( 7, 22, 48)

# DEFINE A FONT 
FONT = pygame.font.SysFont('comicsans', 12)

# DEFINE THE PLANET CLASS
class Planet:

    AU = 149.6e6 * 1000  # Astronamical Unit: distance of the earth to the sun in meter
    G = 6.67428e-11      # The gravity const for determine the force of the attraction between objects
    SCALE = 200/AU       # 1AU = 100 pixels
    TIMESTEP = 3600*24   # each 1 day the simulation of the planets how they move, is get updated  

    def __init__(self, x, y, radius, color, mass):
        
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []  # the different points of the planet movement 
        self.sun = False # The planet will move arround the sun
        self.distance_to_sun = 0

        # velocity or the speed of the movement of a planet wich is moving on two axes (x, y)
        self.x_vel = 0
        self.y_vel = 0

    def draw(self, window):

        # Apply the scale over x and y
        x = self.x * self.SCALE + WIDTH /2
        y = self.y * self.SCALE + HEIGHT /2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + WIDTH / 2
                updated_points.append((x, y))

            pygame.draw.lines(window, self.color, False, updated_points, 2)

        pygame.draw.circle(window, self.color, (x, y), self.radius)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun / 1000, 1)}Km", 1, WHITE)
            window.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2 ))


    def attraction(self, other):
        other_x, other_y = other.x, other.y
        # distance between the current planet and the other one
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        # the square
        distance = math.sqrt(distance_x **2 + distance_y **2)

        if other.sun:
            self.distance_to_sun = distance
        
        force = self.G * self.mass * other.mass / distance **2
        # calculate the angle theta
        theta = math.atan2( distance_y, distance_x)

        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y

    def update_position(self, planets):
        total_fx, total_fy = 0, 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP

        self.orbit.append((self.x, self.y))





def main():
    
    run = True
    clock = pygame.time.Clock()

    # Init. the diffrent planets
    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet( -1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24 )
    earth.y_vel = 29.783 *1000

    mars = Planet( -1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 *1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 0.330 * 10**24)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 18, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000


    planets = [sun, earth, mars, mercury, venus]

    while run:
        clock.tick(60)

        WIN.fill(DARK_BLUE)
        

        for event in  pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()
        

    pygame.quit()

if __name__ == "__main__":
    main()