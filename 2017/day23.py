from __future__ import print_function
import collections


def parse_input(puzzle_input):
    return [line.strip().split(" ") for line in puzzle_input]


def value_of(registers, key):
    if key in "abcdefgh":
        return registers[key]
    else:
        return int(key)

def step(registers, program, ip):
    op, x, y = program[ip]
    vx = value_of(registers, x)
    vy = value_of(registers, y)
    if op == "set":
        registers[x] = vy
    elif op == "sub":
        registers[x] = vx - vy
    elif op == "mul":
        registers[x] = vx * vy
        registers["mul_count"] += 1
    elif op == "jnz":
        if vx != 0:
            ip += vy
            return registers, ip
    else:
        raise "unknown op: {}".format(op)
    ip += 1
    return registers, ip


def part1(program):
    registers = collections.defaultdict(lambda: 0)
    ip = 0
    while ip < len(program):
        registers, ip = step(registers, program, ip)
    return registers["mul_count"]


def part2():
    h = 0
    # value of b is extracted from lines 1, 5, 6
    # value of c is extracted from lines 7, 8
    # step value is taken from line 31
    b = 108100
    c = 125100
    for x in xrange(b, c + 1, 17):
        for i in xrange(2, x):
            if x % i == 0:
                h += 1
                break
    return h


def run(puzzle_input):
    program = parse_input(puzzle_input)
    print(part1(program))
    print(part2())


if __name__ == "__main__":
    run(file("input23.txt"))
    # 6241
    # 909
