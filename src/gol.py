
from load_game_file import load_game_rle
from renderers import renderer_factory

import sys
import os
from pathlib import Path

cwd = Path(os.getcwd())
# getting file name
argv = sys.argv[1:]
file_path = None
if argv:
    file_path = (cwd / argv[0] )
    file_path = file_path if os.path.isfile(file_path) else None

if __name__ == "__main__":
    renderer_class = renderer_factory("gui")
    renderer = renderer_class(surface_size=(1000, 1000))
    if file_path:
        renderer.grid = load_game_rle(file_path,  renderer.grid)
    renderer.start_loop()

