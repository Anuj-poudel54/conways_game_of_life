from .base_renderer import Renderer

import time, os

class CLIRenderer(Renderer):
    def __init__(self, grid = None, surface_size = ...):
        super().__init__(grid, surface_size)
        self._wrap_around = True

    def render(self):
        os.system("cls")
        self._dprint_grid()
        self._calculate_next_gen()
        time.sleep(.2)

        return True