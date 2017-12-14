def knot_hash_round(values, hash_input, idx, skip):
    length = len(values)
    for v in hash_input:
        foo = [values[(k + idx) % length] for k in xrange(v)]
        for k, val in enumerate(reversed(foo)):
            values[(k + idx) % length] = val
        idx += v + skip
        skip += 1
    return [values, idx, skip]

def knot_hash(length, puzzle_input):
    hash_input = [ord(ch) for ch in puzzle_input.strip()]
    hash_input.extend([17, 31, 73, 47, 23])

    hashed_list = range(length)
    skip = 0
    i = 0

    for k in xrange(64):
        hashed_list, i, skip = knot_hash_round(hashed_list, hash_input, i, skip)

    dense = []
    for i in xrange(0, length, 16):
        dense_value = reduce(lambda x, y: x ^ y, hashed_list[i:i+16])
        dense.append(dense_value)
    
    hex_string = []
    for value in dense:
        hex_string.append(str.format('{:02x}', value))
    return ''.join(hex_string)

def run(length, puzzle_input):
    hash_input = map(int, puzzle_input.split(","))
    hashed_list, i, skip = knot_hash_round(range(length), hash_input, 0, 0)
    print(hashed_list[0] * hashed_list[1])

    print(knot_hash(256, puzzle_input))

if __name__ == '__main__':
    example_input = '3,4,1,5'
    real_input = '183,0,31,146,254,240,223,150,2,206,161,1,255,232,199,88'

    run(5, example_input)
    # 12
    # 4a19451b02fb05416d73aea0ec8c00c0

    run(256, real_input)
    # 15990
    # 90adb097dd55dea8305c900372258ac6
