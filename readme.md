## Conway's game of life
[Game of life - wiki](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)

### Installing
```python
pip install requirements.txt
cd ./src
python gol.py
```

### Loading pattern from Run-Length Encoding (.rle) file
```python
# python gol.py /path/to/rle_file
python ./gol.py path/to/proj_dir/example_patterns/glider.rle
```
*You can get rle pattern files from [patterns](https://conwaylife.com/wiki/Pattern_of_the_Year)*

### Shortcuts

`q` Quit

`a` Toggle automatic

`c` Kill all cells / clear screen

`s` Slows down speed if in automatic

`f` Increase the speed if in automatic

`ctrl +🖱️` Move cells

`ctrl + s` Saves current state of game in to the file [TODO]

`l` Load file [TODO]

`space` Generate next generation manually

`mouse left click` Make the cell alive

`mouse right click` Make the cell dead

### Todos

- [ ] Create seperate window for rendering cells rectangle.
- [ ] Create seperate window for rendering cells rectangle.
- [ ] Running it on just CLI would be great 🤷🏻.
- [ ] Implement saving and loading feature using .rle files.
    - [x]  Loading from .rle file
- [x] Create seperate window for rendering cells rectangle.
- [x] Command for loading file while opening program
    ```shell
    $ python gol.py [filename]
    ```
