from copy import deepcopy
import pygame
pygame.init()

# pygame setup
WINDOW_WIDTH, WINDOW_HEIGHT = (600, 600)
CELL_SIZE = 20
CELL_ROW_COUNT =  int(WINDOW_HEIGHT / CELL_SIZE)
CELL_COL_COUNT =  int(WINDOW_WIDTH / CELL_SIZE)

pygame.display.set_caption("Conway's game of life")
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
running = True
FPS = 10

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

auto = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    (left, _, right) = pygame.mouse.get_pressed()

    if left or right:
        (x, y) = pygame.mouse.get_pos()
        gridy = x // CELL_SIZE
        gridx = y // CELL_SIZE

        grid[gridy][gridx] = True if left else False

    if keys[pygame.K_SPACE] and not auto:
        calculate_next_gen(grid)

    if keys[pygame.K_a]:
        auto = not auto

    if auto:
        calculate_next_gen(grid)

    if keys[pygame.K_c]:
         auto = False
         for row in range(CELL_ROW_COUNT):
            for col in range(CELL_COL_COUNT):
                grid[row][col] = False

    for row in range(CELL_ROW_COUNT):
        for col in range(CELL_COL_COUNT):

            color = "white" if grid[row][col] else "black"
            r = (row * CELL_SIZE)
            c = (col * CELL_SIZE)

            pygame.draw.rect(window, color, pygame.Rect(r, c, CELL_SIZE, CELL_SIZE), border_radius=2)

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()