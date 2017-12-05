def run(input, jump_fn):
    lines = []
    for line in input:
        value = int(line.strip())
        lines.append(value)
    steps = jump_fn(lines)
    print(steps)
    # print(steps, lines)

def jump_fn_part1(lines):
    length, pos, steps = len(lines), 0, 0
    while pos < length:
        next_pos = lines[pos]
        lines[pos] += 1
        pos += next_pos
        steps += 1
    return steps

def jump_fn_part2(lines):
    length, pos, steps = len(lines), 0, 0
    while pos < length:
        next_pos = lines[pos]
        if next_pos >= 3:
            lines[pos] -= 1
        else:
            lines[pos] += 1
        pos += next_pos
        steps += 1
    return steps

# run(["0\n", "3\n", "0\n", "1\n", "-3\n"], jump_fn_part1)
# run(["0\n", "3\n", "0\n", "1\n", "-3\n"], jump_fn_part2)

run(file("input05.txt"), jump_fn_part1)
run(file("input05.txt"), jump_fn_part2)
