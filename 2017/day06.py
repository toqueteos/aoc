class Day06(object):
    def __init__(self, puzzle_input):
        self.steps = 0
        self.seen = set()
        self.when = dict()
        self._run(puzzle_input)

    def _run(self, puzzle_input):
        self._save(puzzle_input)
        while True:
            idx = self._find_largest_bank(puzzle_input)
            # print('idx', idx, 'value', value)
            # print(puzzle_input)
            self._redistribute(puzzle_input, idx)
            self.steps += 1
            if not self._is_saved(puzzle_input):
                self._save(puzzle_input)
            else:
                break
        print('steps', self.steps, 'loop_size', self._loop_size(puzzle_input))

    def _is_saved(self, puzzle_input):
        bank_composition = tuple(puzzle_input)
        return bank_composition in self.seen

    def _save(self, puzzle_input):
        thing = tuple(puzzle_input)
        self.seen.add(thing)
        self.when[thing] = self.steps

    def _find_largest_bank(self, puzzle_input):
        sorted_puzzle_input = sorted(enumerate(puzzle_input),
            key=lambda x: x[1],
            reverse=True)
        for idx, _ in sorted_puzzle_input:
            return idx

    def _redistribute(self, puzzle_input, idx):
        length = len(puzzle_input)
        qty = puzzle_input[idx]
        puzzle_input[idx] = 0
        while qty > 0:
            pos = (idx + 1) % length
            idx += 1
            puzzle_input[pos] += 1
            qty -= 1
    
    def _loop_size(self, puzzle_input):
        bank_composition = tuple(puzzle_input)
        return self.steps - self.when[bank_composition]

example_input = [0, 2, 7, 0]
real_input = [0, 5, 10, 0, 11, 14, 13, 4, 11, 8, 8, 7, 1, 4, 12, 11]

Day06(example_input)
Day06(real_input)
