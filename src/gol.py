import pygame
from pygame.surface import Surface

from collections import Counter
from functools import reduce
from load_game_file import load_game_rle
import sys
import os
pygame.init()

# getting file name
argv = sys.argv[1:]
file_path = None
if argv:
    file_path = argv[0] if os.path.isfile(argv[0]) else None

# pygame setup
WINDOW_WIDTH, WINDOW_HEIGHT = (700, 700)
CELL_SURFACE_WIDTH, CELL_SURFACE_HEIGHT = (1000, 1000)
CELL_SIZE = 20

CELL_ROW_COUNT =  WINDOW_HEIGHT // CELL_SIZE
CELL_COL_COUNT =  WINDOW_WIDTH // CELL_SIZE

pygame.display.set_caption("Conway's game of life")
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(pygame.font.get_default_font(), 20)

cells_surface = Surface((CELL_SURFACE_WIDTH, CELL_SURFACE_HEIGHT))

CELL_COL_COUNT =  cells_surface.get_width() // CELL_SIZE
CELL_ROW_COUNT =  cells_surface.get_height() // CELL_SIZE

running = True
FPS = 60
generations = 0

grid: list[list[bool]] = [ [False for _ in range(CELL_COL_COUNT) ] for _ in range(CELL_ROW_COUNT) ]

if file_path:
    grid = load_game_rle(file_path, grid)

def calculate_live_neighbours(row, col) -> int:
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i == 0 and j == 0): continue
            
            r = (row + i) % CELL_ROW_COUNT
            c = (col + j) % CELL_COL_COUNT

            count += 1 if grid[r][c] else 0

    return count

def dprint_grid(grid: list[list[bool]]):
    for row in grid:
        for col in row:
            if col:
                print("X", end=" ")
            else:
                print("-", end=" ")
        print()

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

dprint_grid(grid)

auto = False

cell_surface_coord = (0,0)
ctrl_pressed = False
move_mode = False      ## TO move cells surface.
last_mouse_pos = (0,0) ## For tracking how much mouse moved while pressing ctrl.
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mouse event
        if ctrl_pressed and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                move_mode = True
                last_mouse_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                move_mode = False

        # Key board event
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL:
                ctrl_pressed = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

            # FPS handling for fast or slow (Not good idea i guess?????)
            if event.key == pygame.K_s:
                FPS -= 4 if FPS >= 10 else 0
            if event.key == pygame.K_f:
                FPS += 4 if FPS <= 60 else 0

            # in-game shortcuts
            if event.key == pygame.K_LCTRL:
                ctrl_pressed = True
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

    # Calculating populations and generations
    is_any_cell_alive = any(map( lambda rows: any(rows), grid ) )
    populations = Counter(reduce( lambda x,y: x + y , grid, [] ))[True]

    # Handling mouse events
    (left, _, right) = pygame.mouse.get_pressed()
    if left or right:
        
        (x, y) = pygame.mouse.get_pos()

        # If move_mode is false, make cells alive if left click else move cell_surface
        if move_mode and ctrl_pressed:

            # Calculating how much mouse moved from last time move_mode was on.
            delta_mouse_movement = ( last_mouse_pos[0] - x, last_mouse_pos[1] - y)
            cell_surface_coord = ( (cell_surface_coord[0] - delta_mouse_movement[0]),
                                  (cell_surface_coord[1] - delta_mouse_movement[1])
                                  )

            last_mouse_pos = (x, y)
            window.fill("black")
        else:
            cell_surface_coord = (0,0) ## Should remove, it is here for not able to clik on intended cell when surface is moved.
            gridx = (y // CELL_SIZE)% CELL_ROW_COUNT
            gridy = (x // CELL_SIZE)% CELL_COL_COUNT

            grid[gridx][gridy] = True if left else False

    if auto:
        calculate_next_gen(grid)

    # Rendering cells
    for row in range(CELL_ROW_COUNT):
        for col in range(CELL_COL_COUNT):

            color = "black" if grid[row][col] else "gray"
            r = (row * CELL_SIZE)
            c = (col * CELL_SIZE)

            pygame.draw.rect(cells_surface, color, pygame.Rect(c, r, CELL_SIZE, CELL_SIZE), border_radius=2)


    text_surfaces = []
    text_surfaces.append(font.render(f'Generations: {generations}', True, "black"))
    text_surfaces.append(font.render(f'Populations: {populations}', True, "black"))
    
    # Rendering cell surface at the center of window
    window.blit(cells_surface, cell_surface_coord)
    
    for i, text_surface in enumerate(text_surfaces):
        window.blit(text_surface, (0, text_surfaces[i].get_height() + 17 * i ))


    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()