def generator(value, factor, mod=1):
    while True:
        value = (value * factor) % 2147483647
        if value % mod == 0:
            yield value & 0xffff

def run(puzzle_input):
    import itertools
    
    FACTOR_A = 16807
    FACTOR_B = 48271
    FORTY_MILLION = 40000000
    FIVE_MILLION = 5000000
    MOD_4 = 4
    MOD_8 = 8

    A, B = puzzle_input

    ga = generator(A, FACTOR_A)
    gb = generator(B, FACTOR_B)
    print(sum(next(ga) == next(gb) for _ in xrange(FORTY_MILLION)))

    ga = generator(A, FACTOR_A, MOD_4)
    gb = generator(B, FACTOR_B, MOD_8)
    print(sum(next(ga) == next(gb) for _ in xrange(FIVE_MILLION)))

if __name__ == "__main__":
    example_input = [65, 8921]
    real_input = [883, 879]

    run(example_input)
    # 588
    # 309

    run(real_input)
    # 609
    # 253
