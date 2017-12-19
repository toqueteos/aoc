import string
    
DIR_UP = 1
DIR_DOWN = 2
DIR_LEFT = 3
DIR_RIGHT = 4

DASH = "-"
PIPE = "|"
PLUS = "+"
NONE = " "

def get_cell_at(grid, x, y):
    width = len(grid[0])
    height = len(grid)
    if 0 <= x < width and 0 <= y < height:
        return grid[y][x]
    return NONE

def dir_to_symbol(di):
    if di == DIR_UP or di == DIR_DOWN:
        return PIPE
    elif di == DIR_LEFT or di == DIR_RIGHT:
        return DASH
    else:
        return NONE

def forward(x, y, di):
    if di == DIR_UP:
        return x, y-1
    elif di == DIR_DOWN:
        return x, y+1
    elif di == DIR_LEFT:
        return x-1, y
    elif di == DIR_RIGHT:
        return x+1, y
    else:
        return -1, -1

def rotate(grid, x, y, prev_cell):
    symbols = string.uppercase

    if prev_cell == PIPE:
        to_check = [DIR_LEFT, DIR_RIGHT]
        symbols += DASH
    else:
        to_check = [DIR_UP, DIR_DOWN]
        symbols += PIPE

    for di in to_check:
        cell = get_cell_at(grid, *forward(x, y, di))
        if cell in symbols:
            return di
    return NONE

def parse_input(puzzle_input):
    return [line.rstrip("\n\r") for line in puzzle_input]

def run(start, puzzle_input):
    grid = parse_input(puzzle_input)

    letters = []
    steps = 0

    pos = start
    x, y, di = pos

    cell = get_cell_at(grid, x, y)
    while True:
        if cell in string.uppercase:
            letters.append(cell)
        elif cell == NONE:
            break

        dir_symbol = dir_to_symbol(di)
        x, y = forward(x, y, di)
        cell = get_cell_at(grid, x, y)
        steps += 1

        while cell == "+":
            di = rotate(grid, x, y, dir_symbol)

            x, y = forward(x, y, di)
            cell = get_cell_at(grid, x, y)
            steps += 1
            
    print(''.join(letters))
    print(steps)

if __name__ == "__main__":
    example_input = (
        "    |          ",
        "    |  +--+    ",
        "    A  |  C    ",
        "F---|----E|--+ ",
        "    |  |  |  D ",
        "    +B-+  +--+ ",
    )
    run((4, 0, DIR_DOWN), example_input)
    # ABCDEF
    # 38

    real_input = file("input19.txt")
    run((1, 0, DIR_DOWN), real_input)
    # EOCZQMURF
    # 16312
