def part1(raw_line=""):
    if raw_line == "":
        raw_line = file("input01.txt")
    for line in raw_line:
        first = line[0]

        total = 0
        currentChar = first

        lineWithFirstAtEnd = line[1:].strip() + first

        for nextChar in lineWithFirstAtEnd:
            if nextChar == currentChar:
                total += int(currentChar)
            currentChar = nextChar

        print(total)

def part2(raw_line=""):
    if raw_line == "":
        raw_line = file("input01.txt")
    for line in raw_line:
        total = 0

        line = line.strip()
        halfLength = len(line) / 2
        half1, half2 = line[:halfLength], line[halfLength:]

        for i in xrange(halfLength):
            ch1, ch2 = half1[i], half2[i]
            if ch1 == ch2:
                total += int(ch1)

        for i in xrange(halfLength):
            ch1, ch2 = half2[i], half1[i]
            if ch1 == ch2:
                total += int(ch1)

        print(total)

# part1(["1122"])
# part1(["1111"])
# part1(["1234"])
# part1(["91212129"])
part1()

# part2(["1212"])
# part2(["1221"])
# part2(["123425"])
# part2(["123123"])
# part2(["12131415"])
part2()
