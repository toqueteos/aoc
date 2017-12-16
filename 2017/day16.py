def parse_steps(puzzle_input):
    return [line.strip() for line in puzzle_input]

def dance(state, steps):
    programs = [letter for letter in state]
    for step in steps:
        for expr in step.split(","):
            op, args = expr[0], expr[1:]
            if op == "s":
                distance = int(args)
                programs = programs[-distance:] + programs[:-distance]
            else:
                left, right = args.split("/")
                if op == "x":
                    a, b = int(left), int(right)
                else:
                    a, b = programs.index(left), programs.index(right)
                programs[a], programs[b] = programs[b], programs[a]
    return ''.join(programs)

def guess_period(input_state, puzzle_input, first_state):
    total = 0
    old_state = input_state
    while True:
        state = dance(old_state, puzzle_input)
        total += 1
        if state == first_state:
            return total
        old_state = state

ONE_BILLION = 1000000000

def run(state, puzzle_input):
    steps = parse_steps(puzzle_input)
    dance_state = dance(state, steps)
    print(dance_state)

    period = guess_period(state, steps, state)
    for _ in xrange(ONE_BILLION % period):
        state = dance(state, steps)
    print(state)

if __name__ == "__main__":
    example_input = ["s1,x3/4,pe/b"]
    real_input = file("input16.txt")

    run("abcde", example_input)
    # baedc
    # abcde

    run("abcdefghijklmnop", real_input)
    # iabmedjhclofgknp
    # oildcmfeajhbpngk
