def part1(raw_line=""):
    if raw_line == "":
        raw_line = file("input02.txt")

    total = 0
    for line in raw_line:
        line = line.strip()

        rmin, rmax = float('inf'), -float('inf')
        for match in line.split("\t"):
            value = int(match)
            if value < rmin:
                rmin = value
            if value > rmax:
                rmax = value

        total += rmax - rmin
    print(total)


def part2(raw_line=""):
    import itertools

    if raw_line == "":
        raw_line = file("input02.txt")

    total = 0
    for line in raw_line:
        line = line.strip()

        numbers = map(int, line.split("\t"))
        print(numbers)

        for (a, b) in itertools.product(numbers, numbers):
            if a == b:
                continue

            if a < b:
                b, a = a, b
            div, mod = divmod(a, b)

            if mod == 0:
                total += div
                break
    print(total)

part1()

part2()
