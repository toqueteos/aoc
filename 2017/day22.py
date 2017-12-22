from __future__ import print_function
import collections

DIR_UP = 0
DIR_RIGHT = 1
DIR_DOWN = 2
DIR_LEFT = 3

def parse_input(puzzle_input):
    return [line.strip() for line in puzzle_input]

def parse_line(line):
    return list(line)

def to_infinite_grid(matrix):
    grid = collections.defaultdict(lambda: ".")
    for y, row in enumerate(matrix):
        for x, value in enumerate(row):
            if value == "#":
                grid[(x,y)] = value
    x = y = (len(matrix) // 2)
    return grid, (x, y)

def forward(x, y, di):
    if di == DIR_UP:
        return x, y-1
    elif di == DIR_RIGHT:
        return x+1, y
    elif di == DIR_DOWN:
        return x, y+1
    elif di == DIR_LEFT:
        return x-1, y
    else:
        raise "invalid direction"

rot90_left = {DIR_LEFT: DIR_DOWN, DIR_DOWN: DIR_RIGHT, DIR_RIGHT: DIR_UP, DIR_UP: DIR_LEFT}
rot90_right = {DIR_LEFT: DIR_UP, DIR_UP: DIR_RIGHT, DIR_RIGHT: DIR_DOWN, DIR_DOWN: DIR_LEFT}
rot180 = {DIR_LEFT: DIR_RIGHT, DIR_UP: DIR_DOWN, DIR_RIGHT: DIR_LEFT, DIR_DOWN: DIR_UP}

def rotate90(rot, di):
    if rot == DIR_LEFT:
        return rot90_left[di]
    elif rot == DIR_RIGHT:
        return rot90_right[di]
    else:
        raise "invalid rotation"

def rotate180(di):
    return rot180[di]

def simulator(grid, center, bursts=10000):
    infections = 0
    x, y = center
    di = DIR_UP
    for _ in xrange(bursts):
        node = grid[(x,y)]
        if node == "#":
            di = rotate90(DIR_RIGHT, di)
        else:
            di = rotate90(DIR_LEFT, di)
            infections += 1
        grid[(x,y)] = not node
        x, y = forward(x, y, di)
    return infections

def simulator2(grid, center):
    infections = 0
    x, y = center
    di = DIR_UP
    for it in xrange(10000000):
        node = grid[(x,y)]
        if node == "#":
            di = rotate90(DIR_RIGHT, di)
            grid[(x,y)] = "F"
        elif node == ".":
            di = rotate90(DIR_LEFT, di)
            grid[(x,y)] = "W"
        elif node == "W":
            grid[(x,y)] = "#"
            infections += 1
        elif node == "F":
            di = rotate180(di)
            del grid[(x,y)]
        x, y = forward(x, y, di)
    return infections

def run(puzzle_input):
    lines = parse_input(puzzle_input)
    matrix = [parse_line(line) for line in lines]
    
    grid, center = to_infinite_grid(matrix)
    print(simulator(grid, center))

    grid, center = to_infinite_grid(matrix)
    print(simulator2(grid, center))

if __name__ == "__main__":
    example_input = (
        "..#",
        "#..",
        "...",
    )
    # run(example_input)
    # 5587
    #

    run(file("input22.txt"))
    #
    #