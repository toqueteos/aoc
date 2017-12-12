def run(puzzle_input):
    pipes = {}
    nodes = set()
    for line in puzzle_input:
        line = line.strip()
        left, right = parse_line(line)
        # Save pipe for next pass
        pipes[left] = right
        nodes.add(left)
    groups = compute_groups(pipes, nodes)
    print(group_size_for(groups, 0))
    print(len(groups))

def compute_groups(pipes, nodes):
    groups = []
    for left, right in pipes.items():
        if is_in_a_group(groups, left):
            continue
        group = compute_group(pipes, nodes, left)
        groups.append(group)
        # Remove computed group nodes from nodes
        nodes = nodes.difference(group)
    return groups

def compute_group(pipes, nodes, node):
    to_follow = set()
    visited = set()
    group = set([node])
    # Find direct connections with node
    for n in nodes:
        connected_to = pipes[n]
        if node not in connected_to:
            continue
        # Both sides of the pipe belong to the group!
        group.add(n)
        group.update(connected_to)
        # No need to follow n
        to_follow.update(connected_to)
    # Find non-direct connection with node
    while len(to_follow) > 0:
        new_to_follow = set()
        for follow_number in to_follow:
            for pipe_num in pipes[follow_number]:
                if pipe_num not in visited:
                    new_to_follow.add(pipe_num)
                    group.add(pipe_num)
            visited.add(follow_number)
        to_follow = new_to_follow
    return group

def is_in_a_group(groups, to_find):
    for group in groups:
        if to_find in group:
            return True
    return False

def group_size_for(groups, to_find):
    for group in groups:
        if to_find in group:
            return len(group)
    return 0
       
def parse_line(line):
    left, right = line.split(" <-> ")
    return int(left), map(int, right.split(", "))

example_input = (
    "0 <-> 2",
    "1 <-> 1",
    "2 <-> 0, 3, 4",
    "3 <-> 2, 4",
    "4 <-> 2, 3, 6",
    "5 <-> 6",
    "6 <-> 4, 5",
)
real_input = file("input12.txt")

# run(example_input)
run(real_input)
