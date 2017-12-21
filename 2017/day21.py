def diag(kp):
	nk = []
	for x in xrange(len(kp)):
		l = []
		for y in xrange(len(kp)):
			l.append(kp[y][x])
		nk.append("".join(l))
	return tuple(nk)

def parse_line(line):
    left, right = line.strip().split(" => ")
    a = tuple(left.split("/"))
    b = right.split("/")
    return a, b

def parse_input(puzzle_input):
    rules = {}
    for line in puzzle_input:
        k, v = parse_line(line)
        rules[k] = v
        rules[diag(k)] = v

        k2 = tuple([s[::-1] for s in k])
        rules[k2] = v
        rules[diag(k2)] = v

        k3 = tuple(s for s in k[::-1])
        rules[k3] = v
        rules[diag(k3)] = v

        k4 = tuple([s[::-1] for s in k3])
        rules[k4] = v
        rules[diag(k4)] = v
    return rules

def num_on(g):
	return sum([sum([c == "#" for c in l]) for l in g])

def run(puzzle_input):
    rules = parse_input(puzzle_input)
    grid = [
        ".#.",
        "..#",
        "###",
    ]
    for it in xrange(18):
        length = len(grid)
        new_grid = []

        if length % 2 == 0:
            for y in xrange(0, length, 2):
                new_lines = [[],[],[]]
                for x in xrange(0, length, 2):
                    k = tuple([grid[y][x:x+2], grid[y+1][x:x+2]])
                    v = rules[k]
                    for i, l in enumerate(v):
                        new_lines[i].extend(list(l))
                new_grid.extend(["".join(l) for l in new_lines])
        elif length % 3 == 0:
            for y in xrange(0, length, 3):
                new_lines = [[],[],[],[]]
                for x in xrange(0, length, 3):
                    k = tuple([grid[y][x:x+3], grid[y+1][x:x+3], grid[y+2][x:x+3]])
                    v = rules[k]
                    for i, l in enumerate(v):
                        new_lines[i].extend(list(l))
                new_grid.extend(["".join(l) for l in new_lines])
        else:
            raise "bad dimension"
        grid = new_grid
        if it == 4:
            print(num_on(grid))
    print(num_on(grid))

if __name__ == "__main__":
    example_input = (
        "../.# => ##./#../...",
        ".#./..#/### => #..#/..../..../#..#",
    )
    # run(example_input)
    # 12
    # 

    run(file("input21.txt"))
    # 147
    # 1936582
