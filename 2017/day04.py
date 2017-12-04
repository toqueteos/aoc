def run(is_valid_fn):
    total = 0
    for line in file("input04.txt"):
        line = line.strip()
        if is_valid_passphrase(line, is_valid_fn):
            total += 1
    print(total)

def is_valid_passphrase(line, is_valid_fn):
    words = line.split()
    length = len(words)
    word_set = set()
    for word in words:
        is_valid_fn(word, word_set)
    return len(word_set) == length

def is_valid_part1(word, word_set):
    word_set.add(word)

def is_valid_part2(word, word_set):
    hist = [0] * 26
    for c in word:
        hist[ord(c)-97] += 1
    word_set.add(tuple(hist))

run(is_valid_part1)
run(is_valid_part2)
