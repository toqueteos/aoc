def run(puzzle_input):
    guards = []
    for line in puzzle_input:
        line = line.strip()
        left, right = parse_line(line)
        guards.append((left, right))
    print(severity(guards))
    print(walk_undetected(guards))

def parse_line(line):
    return map(int, line.split(": "))

def caught_by_guard(depth, _range):
    return depth % (2 * (_range - 1)) == 0

def severity(guards):
    return sum(d * r for d, r in guards if caught_by_guard(d, r))
    # total = 0
    # for d, r in guards:
    #     if caught_by_guard(d, r):
    #         total += d * r
    # return total

def walk_undetected(guards):
    delay = 0
    caught = False
    while any(caught_by_guard(delay+d, r) for d, r in guards):
        delay += 1
    return delay

example_input = (
    "0: 3",
    "1: 2",
    "4: 4",
    "6: 4",
)
real_input = file("input13.txt")

run(example_input)
# 24
# 10

run(real_input)
# 748
# 3873662
