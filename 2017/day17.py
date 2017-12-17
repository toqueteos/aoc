def spinlock(offset):
    pos = 0
    buffer = [0]
    for x in xrange(1, 2019):
        pos = (pos + offset) % len(buffer)
        buffer.insert(pos + 1, x)
        pos = (pos + 1) % len(buffer)
    idx = buffer.index(2017)
    return buffer[idx+1:][0]

def angry_spinlock(offset):
    pos = 0
    length = 1
    pos1 = None
    for x in xrange(1, 50000000):
        pos = (pos + offset) % length
        length += 1
        if pos is 0:
            pos1 = x
        pos = (pos + 1) % length
    return pos1

def run(puzzle_input):
    print(spinlock(puzzle_input))
    print(angry_spinlock(puzzle_input))

if __name__ == "__main__":
    # run(3)
    # 638
    # 

    run(343)
    # 1914
    # 41797835
