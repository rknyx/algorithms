#python3
# Problem Description
# Task. You’ve just had a huge party in your parents’ house, and they are returning tomorrow. You need
# to not only clean the apartment, but leave no trace of the party. To do that, you need to clean all
# the rooms in some order. After finishing a thorough cleaning of some room, you cannot return to it
# anymore: you are afraid you’ll ruin everything accidentally and will have to start over. So, you need to
# move from room to room, visit each room exactly once and clean it. You can only move from a room
# to the neighboring rooms. You want to determine whether this is possible at all.
# This can be reduced to a classic Hamiltonian Path problem: given a graph, determine whether there is
# a route visiting each vertex exactly once. Rooms are vertices of the graph, and neighboring rooms are
# connected by edges. Hamiltonian Path problem is NP-complete, so we don’t know an efficient algorithm
# to solve it. You need to reduce it to SAT, so that it can be solved efficiently by a SAT-solver.
# Input Format. The first line contains two integers 𝑛 and 𝑚 — the number of rooms and the number of
# corridors connecting the rooms respectively. Each of the next 𝑚 lines contains two integers 𝑢 and 𝑣
# describing the corridor going from room 𝑢 to room 𝑣. The corridors are two-way, that is, you can go
# both from 𝑢 to 𝑣 and from 𝑣 to 𝑢. No two corridors have a common part, that is, every corridor only
# allows you to go from one room to one other room. Of course, no corridor connects a room to itself.
# Note that a corridor from 𝑢 to 𝑣 can be listed several times, and there can be listed both a corridor
# from 𝑢 to 𝑣 and a corridor from 𝑣 to 𝑢.
# variable Xij = vertex i stays at position j in hamiltonian path
import sys
from itertools import combinations, product, starmap

VERTEX_COUNT = None

UNSATISFIABLE_SOLUTION = "2 1\n1 0\n-1 0"
SATISFIABLE_SOLUTION = "1 1\n1 -1 0"
PREDEFINED_SOLUTIONS = [UNSATISFIABLE_SOLUTION, SATISFIABLE_SOLUTION]

def process_input(lines=None):
    global VERTEX_COUNT
    if lines is None:
        lines = sys.stdin.readlines()
    counts = tuple(map(int, lines[0].split(" ")))
    VERTEX_COUNT = counts[0]

    # filter duplicated or reversed edges (small optimization of clauses count)
    edges = set()
    res = []
    for line in lines[1:]:
        left, right = map(int, line.split(" "))
        _set = frozenset([left, right])
        if _set in edges:
            continue
        res.append((left, right))
    return counts, res


def get_variable(vertex_num, position):
    return vertex_num + VERTEX_COUNT * position


def get_bunch_of_variables(vertex_nums, positions):
    return starmap(get_variable, product(vertex_nums, positions))


def res_to_string(res):
    _res = "%s %s\n" % (len(res), VERTEX_COUNT * VERTEX_COUNT)
    # _res = "%s %s\n" % (VERTEX_COUNT * VERTEX_COUNT, len(res))
    _res += "\n".join((" ".join(map(str, expression + [0])) for expression in res))
    return _res


def generate_expressions(counts, input_generator):
    vertices_count, edges_count = counts
    if edges_count == 0:
        return UNSATISFIABLE_SOLUTION if vertices_count > 1 else SATISFIABLE_SOLUTION

    res = []
    _g = get_variable

    # each vertex has at least one position (1)
    res += [list(get_bunch_of_variables([vertex_num], range(vertices_count))) for vertex_num in range(1, vertices_count + 1)]

    # vertex can't have two positions (max 435 * 30 = 13000)
    for vertex_num in range(1, vertices_count + 1):
        res += ([[-_g(vertex_num, pair[0]), -_g(vertex_num, pair[1])] for pair in combinations(range(vertices_count), 2)])

    # each position is occupied by at least one vertex
    for pos_num in range(vertices_count):
        res.append([get_variable(vertex_num, pos_num) for vertex_num in range(1, vertices_count + 1)])


    adjacency = {}
    all_vertices = set()

    for left, right in input_generator:
        all_vertices.add(left)
        all_vertices.add(right)
        if left not in adjacency:
            adjacency[left] = {right}
        else:
            adjacency[left].add(right)
        if right not in adjacency:
            adjacency[right] = {left}
        else:
            adjacency[right].add(left)

    # neighbors should follow neighbors
    for vertex_num in range(1, vertices_count + 1):
        if vertex_num not in adjacency:
            return UNSATISFIABLE_SOLUTION
        adjacent = adjacency[vertex_num]
        for pos_num in range(vertices_count - 1):
            curr_variable = get_variable(vertex_num, pos_num)
            res.append([-curr_variable] + [get_variable(x, pos_num + 1) for x in adjacent])
    return res


if __name__ == '__main__':
    res = generate_expressions(*process_input())
    if res in PREDEFINED_SOLUTIONS:
        print(res)
    else:
        print(res_to_string(res))