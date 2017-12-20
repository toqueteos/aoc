import re

class Particle(object):
    def __init__(self, p, v, a):
        self.pos = p
        self.vel = v
        self.acc = a

    def step(self):
        for i in xrange(3):
            self.vel[i] += self.acc[i]
            self.pos[i] += self.vel[i]

    def distance0(self):
        return sum([abs(x) for x in self.pos])

particle_pattern = re.compile("(\-?[0-9]+)")

def parse_particle(line):
    parts = map(int, particle_pattern.findall(line))
    return Particle(parts[:3], parts[3:6], parts[6:])

def parse_input(puzzle_input):
    return [line.strip() for line in puzzle_input]

def lowest(distances):
    import operator
    lowest, _ = min(enumerate(distances), key=operator.itemgetter(1))
    return lowest

def particle_simulator(particles, n, destroy_on_collision=False):
    import collections
    counter = collections.Counter()
    distances = [part.distance0() for part in particles.itervalues()]

    for _ in xrange(n):
        for idx, part in particles.iteritems():
            part.step()
            distances[idx] = part.distance0()

        low = lowest(distances)
        counter.update([low])
    
        if destroy_on_collision:
            groups = collections.defaultdict(list)
            for idx, part in particles.iteritems():
                k = tuple(part.pos)
                groups[k].append(idx)

            for pos, group in groups.iteritems():
                if len(group) > 1:
                    for idx in group:
                        del particles[idx]

    if destroy_on_collision:
        return len(particles)
    else:
        return counter.most_common(1)[0][0]

def run(puzzle_input, n=100):
    import copy

    lines = parse_input(puzzle_input)
    particles = {idx: parse_particle(line) for idx, line in enumerate(lines)}

    print(particle_simulator(copy.deepcopy(particles), n * 10))
    print(particle_simulator(copy.deepcopy(particles), n, destroy_on_collision=True))

if __name__ == "__main__":
    example_input = (
        "p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>",
        "p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>",
    )
    run(example_input)
    # 0
    # 2

    real_input = file("input20.txt")
    run(real_input)
    # 91
    # 567