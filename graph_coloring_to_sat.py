#python3
from sys import stdin
from itertools import combinations

VERTEX_COUNT = None
VARS_SET = set()

# for each vertex compose a clause that it has different color
# xij = means vertex i has color j
# x11 || x12 || x13 <- x1 has one of the colors
# x21 || x22 || x23 <- x2 has one of the colors and so on for each x
# next - how to restrict common colors


def _str_plus_one(_int):
    return str(_int + 1)


def pairwise_distinct_colors(connected_vertices):
    pairwise_combinations = combinations(connected_vertices, 2)
    return [[-a, -b] for (a, b) in pairwise_combinations]


def calc(data):
    clauses = []
    # each vertex has color
    for vertex_num in range(VERTEX_COUNT):
        clauses.append([get_variable(vertex_num, color) for color in range(3)])

    for source, dest in data:
        for color in range(3):
            clauses.append((-get_variable(source, color), -get_variable(dest, color)))

    return clauses


test_input_3 = """5 6
1 2
1 4
1 5
2 5
2 3
3 5
3 4
4 5""".split("\n")


def process_input():
    global VERTEX_COUNT
    lines = stdin.readlines()
    # lines = test_input_3
    vertices_num, edges_num = map(int, lines[0].split(" "))
    VERTEX_COUNT = vertices_num

    data = []
    for line in lines[1:]:
        source, dest = map(int, line.split(" "))
        data.append((source-1, dest-1))
    return data


def to_string(res):
    vars_count = len(VARS_SET)
    clauses_count = len(res)
    output = "%s %s\n" % (clauses_count, vars_count)

    for clause in res:
        output += " ".join(map(str, clause)) + " 0\n"
    return output


def get_variable(vertex, color):
    global VERTEX_COUNT, VARS_SET
    var = VERTEX_COUNT * color + vertex + 1
    VARS_SET.add(var)
    return var

if __name__ == '__main__':
    res = (calc(process_input()))
    print(to_string(res))