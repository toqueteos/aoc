def run(puzzle_input):
    for line in puzzle_input:
        line = line.strip()
        total, non_canceled_chars = parse_line(line)
        print(total, non_canceled_chars)

def parse_line(line):
    total = 0
    non_canceled_chars = 0
    level = 0
    garbage = False
    skip_next = False
    for c in line:
        if skip_next:
            skip_next = False
            continue
        if c == "!":
            skip_next = True
            continue
        if c == "<":
            if not garbage:
                garbage = True
            else:
                non_canceled_chars += 1
            continue
        if c == ">":
            garbage = False
        if c == "{" and not garbage:
            level += 1
        if c == "}" and not garbage:
            total += level
            level -= 1
        if garbage:
            non_canceled_chars += 1
    return total, non_canceled_chars

# Part 1
# run(["<>"])
# run(["<random characters>"])
# run(["<<<<>"])
# run(["<{!>}>"])
# run(["<!!>"])
# run(["<!!!>>"])
# run(["<{o\"i!a,<{i<a>"])
# run(["{}"])
# run(["{{{}}}"])
# run(["{{},{}}"])
# run(["{{{},{},{{}}}}"])
# run(["{<{},{},{{}}>}"])

# Part 2
# run(["<>"])
# run(["<random characters>"])
# run(["<<<<>"])
# run(["<{!>}>"])
# run(["<!!>"])
# run(["<!!!>>"])
# run(["<{o\"i!a,<{i<a>"])
run(file("input09.txt"))
