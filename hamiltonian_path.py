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
ALL_VERTICES = {}


def get_counts():
    return tuple(map(int, sys.stdin.readline().split(" ")))


def process_input(lines=None):
    global VERTEX_COUNT
    if lines is None:
        lines = sys.stdin.readlines()
    counts = tuple(map(int, lines[0].split(" ")))
    VERTEX_COUNT = counts[0]
    return counts, (tuple(map(int, x.split(" "))) for x in lines[1:])


def get_variable(vertex_num, position):
    return vertex_num + VERTEX_COUNT * position


def get_bunch_of_variables(vertex_nums, positions):
    return starmap(get_variable, product(vertex_nums, positions))


def neighbors(pos, num):
    if pos == 0:
        return pos + 1,
    elif pos == num - 1:
        return pos - 1,
    else:
        return pos - 1, pos + 1


def neighboring_positions(_num):
    return (neighbors(pos, _num) for pos in range(_num))


def res_to_string(res):
    _res = "%s %s\n" % (len(res), VERTEX_COUNT * VERTEX_COUNT)
    _res += "\n".join((" ".join(map(str, expression + [0])) for expression in res))
    return _res


def generate_expressions(counts, input_generator):
    vertices_count, edges_count = counts
    res = []
    _g = get_variable

    # each vertex has at least one position
    res += [list(get_bunch_of_variables([vertex_num], range(vertices_count))) for vertex_num in range(1, vertices_count+1)]

    # vertex can't have two positions
    for vertex_num in range(1, vertices_count + 1):
        res += ([[-_g(vertex_num, pair[0]), -_g(vertex_num, pair[1])] for pair in combinations(range(vertices_count), 2)])

    # each position is occupied by one vertex
    for position_num in range(vertices_count):
        pairwise_combs = combinations((_g(x, position_num) for x in range(1, vertices_count + 1)), 2)
        res += ([-x[0], -x[1]] for x in pairwise_combs)

    # only neighbors can lead one after another
    neighbors = {}
    all_vertices = set()

    for left, right in input_generator:
        all_vertices.add(left)
        all_vertices.add(right)
        if left not in neighbors:
            neighbors[left] = {right}
        else:
            neighbors[left].add(right)
        if right not in neighbors:
            neighbors[right] = {left}
        else:
            neighbors[right].add(left)

    for vertex in (_v for _v in all_vertices if _v in neighbors):
        for position_num, neighbors_positions in enumerate(neighboring_positions(vertices_count)):
            curr_variable = get_variable(vertex, position_num)
            non_neighbor_variables = get_bunch_of_variables(all_vertices - neighbors[vertex] - {vertex}, neighbors_positions)
            res += ([-curr_variable, -non_neighbor] for non_neighbor in non_neighbor_variables)

    return res


def test_lines_1():
    return """30 80
1 9
1 10
1 16
1 20
2 23
3 7
3 22
4 22
4 30
5 3
5 9
5 18
5 25
6 4
6 22
6 27
7 2
7 20
7 26
8 16
8 26
9 5
9 6
9 13
10 24
11 2
11 16
11 17
11 27
12 8
12 29
13 4
13 6
13 9
13 12
13 15
13 18
14 22
15 6
15 28
16 15
16 18
17 6
17 14
17 22
18 3
19 6
19 12
19 24
20 4
20 7
20 11
21 13
21 14
22 4
22 17
23 4
23 16
23 20
23 29
24 1
24 20
24 27
24 28
25 10
25 18
26 9
26 29
27 10
27 18
28 8
28 11
28 27
29 11
29 17
29 21
30 9
30 11
30 16
30 19""".split("\n")

if __name__ == '__main__':
    # res = generate_expressions(*process_input(test_lines_1()))
    res = generate_expressions(*process_input())
    print(res_to_string(res))