class KnotHash(object):
    def __init__(self, lengths, values):
        self.lengths = lengths
        self.values = values
        self.pos = 0
        self.skip = 0

    def one_round(self):
        mod_size = len(self.values)
        for length in self.lengths:
            self._reverse(self.pos, self.pos + length)
            self.pos = (self.pos + length + self.skip) % mod_size
            self.skip = (self.skip + 1) % mod_size
        return self.values

    def _reverse(self, start, end):
        import itertools

        length = len(self.values)
        sublist = []
        for i, v in enumerate(itertools.cycle(self.values)):
            if i < start:
                continue
            if i >= end:
                break
            sublist.append(v)

        sublist = sublist[::-1]
        subidx = 0
        sublength = len(sublist)

        for i, _ in enumerate(itertools.cycle(self.values)):
            if i < start:
                continue
            if subidx >= sublength:
                break
            idx = i % length
            self.values[idx] = sublist[subidx]
            subidx += 1

    def get_hash(self):
        for i in xrange(64):
            round_result = self.one_round()
        return round_result

def part1(values, lengths):
    values = range(256)

    h = KnotHash(lengths, values)
    round_result = h.one_round()
    print(round_result[0] * round_result[1])

def part2(puzzle_input):
    lengths = to_ascii(puzzle_input)
    lengths.extend([17, 31, 73, 47, 23])
    values = range(256)
    
    h = KnotHash(lengths, values)
    sparse_hash = h.get_hash()
    dense_hash = densify_hash(sparse_hash)
    hex_hash = hash_to_hex(dense_hash)
    print(hex_hash)


def to_ascii(puzzle_input):
    return [ord(ch) for ch in puzzle_input.strip()]

def densify_hash(sparse_hash):
    dense_hash = []
    for chunk in chunks(sparse_hash, 16):
        value = reduce(lambda x, y: x ^ y, chunk)
        dense_hash.append(value)
    return dense_hash

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def hash_to_hex(dense_hash):
    hex_string = []
    for value in dense_hash:
        hex_string.append(str.format('{:02x}', value))
    return ''.join(hex_string)

# example_input_part1 = [3, 4, 1, 5]
# part1(range(5), example_input_part1)

real_input_part1 = [183, 0, 31, 146, 254, 240, 223, 150, 2, 206, 161, 1, 255, 232, 199, 88]
part1(range(256), real_input_part1)

# part2("")
# part2("AoC 2017")
# part2("1,2,3")
# part2("1,2,4")

real_input_part2 = "183,0,31,146,254,240,223,150,2,206,161,1,255,232,199,88"
part2(real_input_part2)
