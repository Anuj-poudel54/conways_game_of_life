
from loaders import load_rle
from renderers import renderer_factory

import sys
import os
from pathlib import Path

cwd = Path(os.getcwd())
# getting file name
argv = sys.argv[1:]

renderer_mode = 'gui'
file_path = None

if argv:
    i = 0
    while i < len(argv):
        if argv[i].lower() == '-r':
            renderer_mode = argv[i+1]

        if argv[i].lower() == '-f':
            file_path = (cwd / argv[i+1] )
            file_path = file_path if os.path.isfile(file_path) else None

        i += 2


if __name__ == "__main__":
    if renderer_mode == 'cli' and not file_path:
        print("ERROR: Need to provide pattern file path if using 'cli' mode. ")
        print("       Use '-f <file_path>' flag for passing file.")
        exit(-1)

    renderer_class = renderer_factory(renderer_mode)
    renderer = renderer_class()
    if file_path:
        renderer.grid = load_rle(file_path,  renderer.grid)
    renderer.start_loop()

