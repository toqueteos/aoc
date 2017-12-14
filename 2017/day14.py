from day10 import knot_hash

def knot_hash256(puzzle_input):
    return knot_hash(256, puzzle_input)

def knot_hash_to_bin(hash_input):
    return bin(int(hash_input, 16))[2:].zfill(128)

def count_ones(grid):
    return sum([g.count("1") for g in grid])

def grid_value(grid, pos):
    return grid[pos[1]][pos[0]]

def count_regions(grid):
    import itertools
    to_visit = set(itertools.product(xrange(len(grid)), repeat=2))

    visited = set()
    regions = []
    while len(to_visit) > 0:
        current = to_visit.pop()
        if current in visited:
            continue
        if grid_value(grid, current) is '0':
            continue

        region = set()
        queue = set()
        queue.add(current)
        while len(queue) > 0:
            pos = queue.pop()
            if pos in visited:
                continue
            if grid_value(grid, pos) is '1':
                region.add(pos)
            visited.add(pos)

            for n in neighbors_of(grid, pos):
                if n in visited:
                    continue
                if grid_value(grid, n) is '0':
                    visited.add(pos)
                    continue
                queue.add(n)

        if len(region) > 0:
            regions.append(region)

        to_visit = to_visit.difference(region)

    return len(regions)

def neighbors_of(grid, pos):
    grid_length = len(grid)
    x, y = pos
    candidates = [(x, y-1), (x+1, y), (x, y+1), (x-1, y)]
    candidates = filter(lambda pos: pos[0] >= 0 and pos[0] < grid_length, candidates)
    candidates = filter(lambda pos: pos[1] >= 0 and pos[1] < grid_length, candidates)
    return candidates

def run(puzzle_input):
    grid = []
    for i in xrange(128):
        result = knot_hash256("{}-{}".format(puzzle_input, i))
        grid.append(knot_hash_to_bin(result))

    print(count_ones(grid))
    print(count_regions(grid))

if __name__ == "__main__":
    example_input = "flqrgnkx"
    real_input = "amgozmfv"

    run(example_input)
    # 8108
    # 1242

    run(real_input)
    # 8222
    # 1086
