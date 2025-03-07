import pygame
from collections import Counter
from functools import reduce
pygame.init()

# pygame setup
WINDOW_WIDTH, WINDOW_HEIGHT = (700, 700)
CELL_SIZE = 20

CELL_ROW_COUNT =  WINDOW_HEIGHT // CELL_SIZE
CELL_COL_COUNT =  WINDOW_WIDTH // CELL_SIZE

pygame.display.set_caption("Conway's game of life")
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(pygame.font.get_default_font(), 20)

running = True
FPS = 60
generations = 0

grid: list[list[bool]] = [ [False for _ in range(CELL_COL_COUNT) ] for _ in range(CELL_ROW_COUNT) ]

def calculate_live_neighbours(row, col) -> int:
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i == 0 and j == 0): continue
            
            r = (row + i) % CELL_ROW_COUNT
            c = (col + j) % CELL_COL_COUNT

            count += 1 if grid[r][c] else 0

    return count

is_any_cell_alive = False
def calculate_next_gen(grid):
    # Updating grid
    update_list = []
    for row in range(CELL_ROW_COUNT):
        for col in range(CELL_COL_COUNT):
            neigh_count = calculate_live_neighbours(row, col)
            if grid[row][col]:
                if neigh_count < 2 or neigh_count > 3:
                    update_list.append(((row, col), False))
            elif not grid[row][col] and neigh_count == 3:
                    update_list.append(((row, col), True))

    for (x,y), alive in update_list:
        grid[x][y] = alive

    global generations, is_any_cell_alive
    if is_any_cell_alive:
        generations += 1

auto = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Key board event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            # FPS handling for fast or slow (Not good idea i guess?????)
            if event.key == pygame.K_s:
                FPS -= 4 if FPS >= 10 else 0
            if event.key == pygame.K_f:
                FPS += 4 if FPS <= 60 else 0
            if event.key == pygame.K_a:
                auto = not auto
            if event.key ==  pygame.K_SPACE:
                auto = False
                calculate_next_gen(grid)
            if event.key == pygame.K_c:
                auto = False
                for row in range(CELL_ROW_COUNT):
                    for col in range(CELL_COL_COUNT):
                        grid[row][col] = False


    (left, _, right) = pygame.mouse.get_pressed()

    is_any_cell_alive = any(map( lambda rows: any(rows), grid ) )
    populations = Counter(reduce( lambda x,y: x + y , grid, [] ))[True]
    
    if left or right:
        (x, y) = pygame.mouse.get_pos()
        gridx = (y // CELL_SIZE) % CELL_COL_COUNT
        gridy = (x // CELL_SIZE) % CELL_ROW_COUNT

        grid[gridy][gridx] = True if left else False

    if auto:
        calculate_next_gen(grid)

    # Rendering cells
    for row in range(CELL_ROW_COUNT):
        for col in range(CELL_COL_COUNT):

            color = "black" if grid[row][col] else "gray"
            r = (row * CELL_SIZE)
            c = (col * CELL_SIZE)

            pygame.draw.rect(window, color, pygame.Rect(r, c, CELL_SIZE, CELL_SIZE), border_radius=2)


    text_surfaces = []
    text_surfaces.append(font.render(f'Generations: {generations}', True, "black"))
    text_surfaces.append(font.render(f'Populations: {populations}', True, "black"))
    
    for i, text_surface in enumerate(text_surfaces):
        window.blit(text_surface, (0, text_surfaces[i].get_height() + 17 * i ))


    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()