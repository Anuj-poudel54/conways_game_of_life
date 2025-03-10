from abc import ABC, abstractmethod
from functools import reduce
from collections import Counter

class Renderer(ABC):

    def __init__(self,
                grid: list[list[bool]] | None = None,
                surface_size: tuple[int] = (500, 500),
                 ):
        super().__init__()

        self._wrap_around = False

        self.CELL_SURFACE_WIDTH, self.CELL_SURFACE_HEIGHT = surface_size

        self.CELL_SIZE = 20
        self.CELL_COL_COUNT =  self.CELL_SURFACE_WIDTH // self.CELL_SIZE
        self.CELL_ROW_COUNT =  self.CELL_SURFACE_HEIGHT // self.CELL_SIZE

        self.auto = False
        self.is_any_cell_alive = 0
        self.populations = 0
        self.generations = 0

        self.grid = grid if grid else [ [False for _ in range(self.CELL_COL_COUNT) ] for _ in range(self.CELL_ROW_COUNT) ]

        self.fps = 60


    def start_loop(self):
        """ Contains main loop. It calls self.render method and self.clean after loop is exited """

        running = True
        while running:

            running = self.render()

            # Calculating populations and generations
            self.is_any_cell_alive = any(map( lambda rows: any(rows), self.grid ) )
            self.populations = Counter(reduce( lambda x,y: x + y , self.grid, [] ))[True]

        self.clean()

    def _calculate_next_gen(self):
    # Updating grid
        update_list = []
        for row in range(self.CELL_ROW_COUNT):
            for col in range(self.CELL_COL_COUNT):
                neigh_count = self._calculate_live_neighbours(row, col)
                if self.grid[row][col]:
                    if neigh_count < 2 or neigh_count > 3:
                        update_list.append(((row, col), False))
                elif not self.grid[row][col] and neigh_count == 3:
                        update_list.append(((row, col), True))

        for (x,y), alive in update_list:
            self.grid[x][y] = alive

        if self.is_any_cell_alive:
            self.generations += 1

    def _calculate_live_neighbours(self, row: int, col: int) -> int:
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i == 0 and j == 0): continue
                
                if self._wrap_around:
                    r = (row + i) % self.CELL_ROW_COUNT
                    c = (col + j) % self.CELL_COL_COUNT

                elif 0 <= row + i < self.CELL_ROW_COUNT and 0 <= col + j < self.CELL_COL_COUNT:
                    r = row + i
                    c = col + j

                else:
                    continue

                count += 1 if self.grid[r][c] else 0

        return count
    
    def _dprint_grid(self):
        for row in self.grid:
            for col in row:
                if col:
                    print("O", end=" ")
                else:
                    print(" ", end=" ")
            print()

    @abstractmethod
    def render(self) -> bool:
        raise NotImplemented

    def clean(self):
        ...
