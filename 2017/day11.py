class Hex(object):
    def __init__(self, q, r, s):
        self.q = q
        self.r = r
        self.s = s
        # self.s = (-q) - r

    def add(self, other):
        self.q += other.q
        self.r += other.r
        self.s += other.s

    def __repr__(self):
        return str.format("Hex<{}, {}, {}>", self.q, self.r, self.s)

directions = {
    "n": Hex(0, 1, -1),
    "ne": Hex(1, 0, -1),
    "se": Hex(1, -1, 0),
    "s": Hex(0, -1, 1),
    "sw": Hex(-1, 0, 1),
    "nw": Hex(-1, 1, 0),
}

def hex_distance(a, b):
    return max(abs(a.q - b.q), abs(a.r - b.r), abs(a.s - b.s))

def run(puzzle_input):
    start = Hex(0, 0, 0)
    pos = Hex(0, 0, 0)
    furthest = 0
    for line in puzzle_input:
        line = line.strip()
        for d in line.split(","):
            pos.add(directions[d])
            distance = hex_distance(start, pos)
            if distance > furthest:
                furthest = distance
        # print(start, pos)
        print(hex_distance(start, pos))
        print(furthest)

# run(["ne,ne,ne"])
# run(["ne,ne,sw,sw"])
# run(["ne,ne,s,s"])
# run(["se,sw,se,sw,sw"])
run(file("input11.txt"))
