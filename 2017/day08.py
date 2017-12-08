import operator

example_input = (
    "b inc 5 if a > 1",
    "a inc 1 if b < 5",
    "c dec -10 if a >= 1",
    "c inc -20 if c == 10",
)

largest = []
registers = {}
ops = {
    ">": lambda a, b: a > b,
    ">=": lambda a, b: a >= b,
    "<": lambda a, b: a < b,
    "<=": lambda a, b: a <= b,
    "==": lambda a, b: a == b,
    "!=": lambda a, b: a != b,
}

def run(puzzle_input):
    for line in puzzle_input:
        line = line.strip()
        parse_line(line)
    # print(registers)
    print(get_largest_value_in_any_register())
    print(get_largest_value_in_any_register_ever())

def parse_line(line):
    [lreg, lop, lval, _, rreg, rop, rval] = line.split(" ")
    lval = int(lval)
    rval = int(rval)
    
    rrval = registers.get(rreg, 0)
    if ops[rop](rrval, rval):
        if lop == "inc":
            registers[lreg] = registers.get(lreg, 0) + lval
        else:
            registers[lreg] = registers.get(lreg, 0) - lval
        # Find largest value in any register after every successful jump instruction
        largest.append(get_largest_value_in_any_register())

def get_largest_value_in_any_register():
    return max(registers.iteritems(), key=operator.itemgetter(1))

def get_largest_value_in_any_register_ever():
    return max(largest, key=operator.itemgetter(1))

# run(example_input)
run(file("input08.txt"))
