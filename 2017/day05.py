def jump(lines, fn):
    length, pos, steps = len(lines), 0, 0
    while pos < length:
        next_pos = lines[pos]
        if fn(next_pos):
            lines[pos] -= 1
        else:
            lines[pos] += 1
        pos += next_pos
        steps += 1
    return steps

def run(puzzle_input):
    lines = []
    for line in puzzle_input:
        value = int(line.strip())
        lines.append(value)

    print(jump(list(lines), lambda pos: False))
    print(jump(list(lines), lambda pos: pos >= 3))

if __name__ == "__main__":
    run(["0", "3", "0", "1", "-3"])
    # 5
    # 10

    run(file("input05.txt"))
    # 325922
    # 24490906
