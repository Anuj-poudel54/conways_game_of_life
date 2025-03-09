from pathlib import Path

tag_state_map = {
    'b': False,
    'o': True
}

def load_game_rle(file_path: str | Path, grid: list[list[bool]]) -> list[list[bool]]:
    width = None
    height = None
    rule = None
    with open(file_path) as f:
        lines = f.readlines()

    lines = filter( lambda line: not line.startswith("#"), lines)
    lines = map( lambda line: line.strip("\n").strip().replace(" ", ""), lines )

    # parsing line 'x = INT, y = INT, rule = RULE'
    assignmetns_seperated = next(lines).split(",")
    assignmetns = map( lambda assn: assn.split("="), assignmetns_seperated)

    for key, value in assignmetns:
        if key == 'x': width = int(value)
        elif key == 'y': height = int(value)
        elif key == 'rule': rule = value

    # Parsing all patterns
    pattern = ''.join(list(lines))
    pattern_extended = ''
    run_count = ''
    for i in range(len(pattern)):
        let = pattern[i]
        if let.isnumeric():
            run_count += let

        elif run_count:
            for _ in range(int(run_count)):
                pattern_extended += let
            run_count = ''

        elif let != '!':
            pattern_extended += let

    
    row = col = 0
    for letter in pattern_extended:
        if letter == '$':
            row += 1
            col = 0
        else:
            grid[row][col] = tag_state_map[letter]
            col += 1

    return grid


if __name__ == "__main__":
    load_game_rle("./patterns/glider.rle", [[None for _ in range(100)] for _ in range(100)])