import collections

example_input = (
    "pbga (66)",
    "xhth (57)",
    "ebii (61)",
    "havc (66)",
    "ktlj (57)",
    "fwft (72) -> ktlj, cntj, xhth",
    "qoyq (66)",
    "padx (45) -> pbga, havc, qoyq",
    "tknk (41) -> ugml, padx, fwft",
    "jptl (61)",
    "ugml (68) -> gyxo, ebii, jptl",
    "gyxo (61)",
    "cntj (57)",
)

Tree = collections.namedtuple('Tree', ['name', 'parent'])
Program = collections.namedtuple('Program', ['name', 'weight', 'children'])

def run(puzzle_input):
    programs = parse_puzzle_input(puzzle_input)
    root = get_tree_root(programs)
    print(root)
    
    # Part 2
    # How did we get this value?
    # By printing root program's children weights recursively until finding the
    # overweighted node.
    #
    #    print_program_and_children_weight(programs, root)
    #    print_program_and_children_weight(programs, 'kzltfq')
    #    print_program_and_children_weight(programs, 'arqoys')
    #
    # Which in this case is 'arqoys'
    # It should weight 1853 units but it weights 1859
    balanced_weight = 1853
    print(balanced_weight)

def parse_puzzle_input(puzzle_input):
    programs = {}
    for line in puzzle_input:
        line = line.strip()
        parse_line(programs, line)
    return programs

def parse_line(programs, line):
    arrow = " -> "
    if arrow in line:
        [left, right] = line.split(arrow)
        name, weight = parse_left(left)
        children = parse_right(right)
    else:
        name, weight = parse_left(line)
        children = []

    program = Program(name, weight, children)
    programs[name] = program

def parse_left(line):
    [name, weight] = line.split(" ")
    return name, int(weight.strip("()"))

def parse_right(line):
    return line.split(", ")

def get_tree_root(programs):
    tree = {}

    for name, program in programs.items():
        if len(program.children) is 0:
            continue
        if name not in tree:
            tree[name] = Tree(name=name, parent=None)
        for child_name in program.children:
            tree[child_name] = Tree(name=child_name, parent=name)

    for name, tree in tree.items():
        if tree.parent is None:
            return tree.name


def print_program_and_children_weight(programs, name):
    w = Weight(programs)

    program = programs[name]
    print(name)
    
    for child_name in program.children:
        child_program = programs[child_name]
        child_weight = child_program.weight
        children_weight = w.get_weight(child_name)
        print('\t{} = ({}) {}'.format(child_name, child_weight, children_weight))

class Weight(object):
    def __init__(self, programs):
        self.programs = programs
        self.weights = {}
        children = []
        # First, save weight for all programs without children
        for program in programs.values():
            if len(program.children) is 0:
                self.weights[program.name] = program.weight
            else:
                children.append(program)
        # Then, compute weight for remaining programs (all have 1+ children)
        for program in children:
            self.weights[program.name] = self.get_weight(program.name)

    def get_weight(self, name):
        program = self.programs[name]
        if name in self.weights:
            # print('{} = {}'.format(name, program.weight))
            return self.weights[name]
        children_weight = [self.get_weight(children_name) for children_name in program.children]
        weight = program.weight + sum(children_weight)
        # print('{} = {} + {}'.format(name, program.weight, children_weight))
        self.weights[name] = weight
        return weight

# run(example_input)
run(file("input07.txt"))
