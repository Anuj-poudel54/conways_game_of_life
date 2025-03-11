from .base_renderer import Renderer

import pygame
from pygame.surface import Surface
class GUIRenderer(Renderer):
    def __init__(self,
                grid: list[list[bool]] = None, 
                surface_size: tuple[int] = None,
                window_size: tuple[int] = None,
                ):

        pygame.init()

        # pygame setup
        desktop_size = pygame.display.get_desktop_sizes()[0]
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = window_size if window_size else (desktop_size[0]*.9, desktop_size[1] * .9 )

        if not surface_size:
            self.CELL_SURFACE_WIDTH, self.CELL_SURFACE_HEIGHT = self.WINDOW_WIDTH, self.WINDOW_HEIGHT

        super().__init__(grid, (self.CELL_SURFACE_WIDTH, self.CELL_SURFACE_HEIGHT))

        self.CELL_SIZE = 20

        self.CELL_ROW_COUNT =  self.WINDOW_HEIGHT // self.CELL_SIZE
        self.CELL_COL_COUNT =  self.WINDOW_WIDTH // self.CELL_SIZE

        # window and surface settings
        pygame.display.set_caption("Conway's game of life")
        self.window = pygame.display.set_mode((self.WINDOW_WIDTH , self.WINDOW_HEIGHT))
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

    def _handle_events(self) -> bool:
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

        return True

    def render(self) -> bool:

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
                gridx = ((x - self.cell_surface_coord[0]) // self.CELL_SIZE)% self.CELL_COL_COUNT
                gridy = ((y - self.cell_surface_coord[1]) // self.CELL_SIZE)% self.CELL_ROW_COUNT

                self.grid[gridy][gridx] = True if left else False
                self.window.fill("black")
        
        if not self.is_any_cell_alive:
            self.auto = False

        if self.auto:
            self._calculate_next_gen()

        # Rendering cells
        for row in range(self.CELL_ROW_COUNT):
            for col in range(self.CELL_COL_COUNT):

                color = "black" if self.grid[row][col] else "gray"
                r = (row * self.CELL_SIZE)
                c = (col * self.CELL_SIZE)

                pygame.draw.rect(self.cells_surface, color, pygame.Rect(c, r, self.CELL_SIZE, self.CELL_SIZE), border_radius=2)

        pygame.display.set_caption(f"Conway's game of life \t Populations: {self.populations} | Generations: {self.generations} ")

        # Rendering cell surface at the center of window
        self.window.blit(self.cells_surface, self.cell_surface_coord)

        pygame.display.update(self.cells_surface.get_rect())

        self.clock.tick(self.fps)

        if not self._handle_events(): return False
        return True

    def clean(self):
        pygame.quit()

if __name__ == "__main__":

    GUIRenderer().start_loop()