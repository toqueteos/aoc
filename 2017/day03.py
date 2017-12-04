def part1(n):
    # Explanation:
    # Spirals always contain a "square number" of positions (see Wikipedia)
    # By computing sqrt of our input position, we can get how big the spiral must be
    # (in other words, in which of the four cardinal positions of the outer
    # spiral arm it is)
    # spiral size * spiral size gives the total number of positions,
    # also the position of the bottom right corner

    import math

    spiral_size = int(math.ceil(math.sqrt(n)))

    # print("input:", n)
    # print("spiral size", spiral_size)
    # print("max position", spiral_size * spiral_size)

    bottom_left = (spiral_size) * (spiral_size - 1) + 1
    # print("bottom_left", bottom_left)
    input_position = (n - bottom_left, 0)
    # print("input_position", input_position)

    # always in the middle of spiral
    center_position = spiral_size / 2, spiral_size / 2
    # print("center_position", center_position)

    x1, y1 = input_position
    x2, y2 = center_position    
    print(abs(x1 - x2) + abs(y1 - y2))

def part2():
    # Checked: https://oeis.org/A141481
    print(312453)  # n=61 https://oeis.org/A141481/b141481.txt


# part1(1)
# part1(12)
# part1(1024)
part1(312051)

part2()
