from .base_renderer import Renderer

import pygame
from pygame.surface import Surface

class GUIRenderer(Renderer):
    def __init__(self,
                grid: list[list[bool]] = None, 
                surface_size: tuple[int] = (700, 700),
                window_size: tuple[int] = (700, 700),
                ):
        super().__init__(grid, surface_size)

        pygame.init()

        # pygame setup
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = window_size
        self.CELL_SIZE = 20

        self.CELL_ROW_COUNT =  self.WINDOW_HEIGHT // self.CELL_SIZE
        self.CELL_COL_COUNT =  self.WINDOW_WIDTH // self.CELL_SIZE

        # window and surface settings
        pygame.display.set_caption("Conway's game of life")
        self.window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.cells_surface = Surface((self.CELL_SURFACE_WIDTH, self.CELL_SURFACE_HEIGHT))

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 20)

        self.CELL_COL_COUNT =  self.cells_surface.get_width() // self.CELL_SIZE
        self.CELL_ROW_COUNT =  self.cells_surface.get_height() // self.CELL_SIZE

        # Game modes
        self.cell_surface_coord = (0,0)
        self.ctrl_pressed = False
        self.move_mode = False      ## TO move cells surface.
        self.last_mouse_pos = (0,0) ## For tracking how much mouse moved while pressing ctrl.

        self.fps = 60

    def render(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Mouse event
            if self.ctrl_pressed and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    self.move_mode = True
                    self.last_mouse_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    self.move_mode = False

            # Key board event
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LCTRL:
                    self.ctrl_pressed = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False

                # FPS handling for fast or slow (Not good idea i guess?????)
                if event.key == pygame.K_s:
                    self.fps -= 4 if self.fps >= 10 else 0
                if event.key == pygame.K_f:
                    self.fps += 4 if self.fps <= 60 else 0

                # in-game shortcuts
                if event.key == pygame.K_LCTRL:
                    self.ctrl_pressed = True
                if event.key == pygame.K_a:
                    self.auto = not self.auto
                if event.key ==  pygame.K_SPACE:
                    self.auto = False
                    self._calculate_next_gen()
                if event.key == pygame.K_c:
                    self.auto = False
                    for row in range(self.CELL_ROW_COUNT):
                        for col in range(self.CELL_COL_COUNT):
                            self.grid[row][col] = False

        # Handling mouse events
        (left, _, right) = pygame.mouse.get_pressed()
        if left or right:

            (x, y) = pygame.mouse.get_pos()

            # If move_mode is false, make cells alive if left click else move cell_surface
            if self.move_mode and self.ctrl_pressed:

                # Calculating how much mouse moved from last time move_mode was on.
                delta_mouse_movement = ( self.last_mouse_pos[0] - x, self.last_mouse_pos[1] - y)
                self.cell_surface_coord = ( (self.cell_surface_coord[0] - delta_mouse_movement[0]),
                                    (self.cell_surface_coord[1] - delta_mouse_movement[1])
                                    )

                self.last_mouse_pos = (x, y)
                self.window.fill("black")
            else:
                self.cell_surface_coord = (0,0) ## Should remove, it is here for not able to clik on intended cell when surface is moved.
                gridx = (y // self.CELL_SIZE)% self.CELL_ROW_COUNT
                gridy = (x // self.CELL_SIZE)% self.CELL_COL_COUNT

                self.grid[gridx][gridy] = True if left else False
                self.window.fill("black")

        if self.auto:
            self._calculate_next_gen()

        # Rendering cells
        for row in range(self.CELL_ROW_COUNT):
            for col in range(self.CELL_COL_COUNT):

                color = "black" if self.grid[row][col] else "gray"
                r = (row * self.CELL_SIZE)
                c = (col * self.CELL_SIZE)

                pygame.draw.rect(self.cells_surface, color, pygame.Rect(c, r, self.CELL_SIZE, self.CELL_SIZE), border_radius=2)


        text_surfaces = []
        text_surfaces.append(self.font.render(f'Generations: {self.generations}', True, "black"))
        text_surfaces.append(self.font.render(f'Populations: {self.populations}', True, "black"))
        
        # Rendering cell surface at the center of window
        self.window.blit(self.cells_surface, self.cell_surface_coord)
        
        for i, text_surface in enumerate(text_surfaces):
            self.window.blit(text_surface, (0, text_surfaces[i].get_height() + 17 * i ))

        pygame.display.flip()

        self.clock.tick(self.fps)

    def clean(self):
        pygame.quit()

if __name__ == "__main__":

    GUIRenderer().start_loop()