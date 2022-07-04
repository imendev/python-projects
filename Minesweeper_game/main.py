import random
import time
import pygame
from queue import Queue


pygame.init()
pygame.font.init()

WIDTH , HEIGHT = 750, 900

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BOMBESweeper Game")

# FONT TYPE
NUM_FONT = pygame.font.SysFont('comicsans', 20)
LOST_FONT = pygame.font.SysFont('comicsans', 50)
# THE GRID PARAMS
ROWS, COLS = 15, 15
BOMBES = 30 
SIZE = WIDTH / ROWS
# THE COLOR CODE 
BG_COLOR = "white"
NUM_COLOR = {1: "black", 2: "red", 3: "green", 4:"yellow", 5: "purple", 6: "pink", 7: "grey", 8: "blue"}
RECT_COLOR = (255, 255, 255)
CLICKED_RECT_COLOR = (125, 125, 25)
FLAG_COLOR = (0, 255, 0)
BOMB_COLOR = (255, 0, 0)

# GUESS THE NEIGHBORS OF AN ELEMENT
def get_neighbors(row, col, rows, cols):
    neighbors = []

    if row > 0: # UP
        neighbors.append((row -1, col))

    if row < rows: # DOWN
        neighbors.append((row +1, col))
    
    if col > 0: #LEFT
        neighbors.append((row, col -1))
    
    if col < cols: # RIGHT
        neighbors.append((row, col +1))
    
    if row > 0 and col > 0:
        neighbors.append((row -1, col -1))
    
    if row < rows and col < cols:
        neighbors.append((row +1, col +1))
    
    if row < rows and col > 0:
        neighbors.append((row +1, col -1))
    
    if row > 0 and col < cols:
        neighbors.append((row -1, col +1))
    
    return neighbors
    

# CREATE THE BOMBES GRID
def create_mine_field(rows, cols, BOMBES):
    # list comprehension 
    field = [[0 for _ in range(cols)] for _ in range(rows)]
   
    mine_positions = set()
  
    while len(mine_positions) < BOMBES:

        row = random.randrange(0, rows)
        col = random.randrange(0, cols)

        pos = row, col
        if pos in mine_positions:
            continue # do another while test
        mine_positions.add(pos)
        field[row][col] = -1
    
    for mine in mine_positions:
        neighbors = get_neighbors(*mine, rows-1, cols-1)
        
        for r,c in neighbors:
            if field[r][c] != -1:
                field[r][c] += 1
    
    return field



def draw(window, field, cover_field, current_time):
    window.fill(BG_COLOR)
    
    time_text = NUM_FONT.render(f"Time lapse: {round(current_time)}", 1, "red")

    window.blit(time_text, (10, HEIGHT - time_text.get_height()))
    
    for i, row in enumerate(field):
        y = SIZE * i
        for j, value in enumerate(row):
            x = SIZE * j

            is_covered = cover_field[i][j] == 0
            is_flag = cover_field[i][j] == -2
            is_bomb = value == -1

            # draw the flag rect
            if is_flag:
                pygame.draw.rect(window, FLAG_COLOR, (x, y, SIZE, SIZE))
                pygame.draw.rect(window, "grey", (x, y, SIZE, SIZE), 2)
                continue
            

            # draw the rectangle and the clicked rect
            if is_covered:
                pygame.draw.rect(window, RECT_COLOR, (x, y, SIZE, SIZE))
                pygame.draw.rect(window, "grey", (x, y, SIZE, SIZE), 2)
                continue
            else:
                pygame.draw.rect(window, CLICKED_RECT_COLOR, (x, y, SIZE, SIZE))
                pygame.draw.rect(window, "grey", (x, y, SIZE, SIZE), 2)

                # draw the bomb rect
                if is_bomb:
                    pygame.draw.circle(window, BOMB_COLOR, (x + SIZE/2, y + SIZE/2), SIZE/2 -4, )
                    

            if value > 0:
                text = NUM_FONT.render(str(value), 1, NUM_COLOR[value])
                window.blit(text, (x + (SIZE /2 - text.get_width()/2), 
                                   y + (SIZE /2 - text.get_height()/2)))
                

    pygame.display.update()

def get_grid_pos(mouse_pos):

    mx, my = mouse_pos

    row = int(my // SIZE)
    col = int(mx // SIZE)

    return row, col

def uncover_from_pos(row, col, cover_field, field):
    q = Queue()
    q.put((row, col))

    visited = set()

    while not q.empty():
        current = q.get()

        neighbors = get_neighbors(*current, ROWS-1, COLS-1)
        for r, c in neighbors:

            if (r, c) in visited:
                continue

            value = field[r][c]
            
            if value == 0 and cover_field[r][c] != -2:
                q.put((r, c))
            if cover_field[r][c] != -2:
                cover_field[r][c] = 1
            visited.add((r, c))

def draw_lost(window, text):

    text = LOST_FONT.render(text,1, "purple")
    window.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))

    pygame.display.update()


def main():
    run = True
    field = create_mine_field(ROWS, COLS, BOMBES)
    cover_field = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    
    lost = False 

    flags = BOMBES
    clicks = 0
    
    start_time = 0

    while run:
        if start_time > 0:
            current_time = time.time() - start_time
        else:
            current_time = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            # HANDLE THE CLICK RECT EVENT
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = pygame.mouse.get_pressed()
                row, col = get_grid_pos(pygame.mouse.get_pos())
                if row >= ROWS or col >= COLS:
                    continue
                if mouse_pressed[0] and cover_field[row][col] != -2:
                    cover_field[row][col] = 1

                    if field[row][col] == -1: # Bomb clicked !
                        
                        lost = True

                    if clicks == 0 or field[row][col] == 0:
                        uncover_from_pos(row, col, cover_field, field)
                    if clicks == 0:
                        start_time = time.time()
                    clicks += 1
                elif mouse_pressed[2]:
                    if cover_field[row][col] == -2:
                        cover_field[row][col] = 0
                        flags += 1
                    else:
                        flags -= 1
                        cover_field[row][col] = -2

        if lost:
            draw(win, field, cover_field, current_time)
            draw_lost(win, "You lost, try again ...")
            pygame.time.delay(5000)

            
            field = create_mine_field(ROWS, COLS, BOMBES)
            cover_field = [[0 for _ in range(COLS)] for _ in range(ROWS)]
            flags = BOMBES
            clicks = 0
            lost = False


        
        draw(win, field, cover_field, current_time)

    
    pygame.quit()

if __name__ == "__main__":
    main()