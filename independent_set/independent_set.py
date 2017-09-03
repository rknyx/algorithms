#python3
from sys import stdin
from numpy import ndarray
from collections import deque
import numpy


def process_input(inp):
    lines = stdin.readlines() if inp is None else inp.split("\n")
    vertex_count = int(lines[0])
    weights = list(map(int, lines[1].split(" ")))
    tree_data = [[] for _ in range(vertex_count)]

    for line in lines[2:]:
        left, right = map(int, line.split(" "))
        tree_data[left - 1].append(right - 1)
        tree_data[right - 1].append(left - 1)

    return tree_data, weights


def calc_independent_set(tree, weights):
    root = 0
    EMPTY = -9999999

    res = ndarray(len(tree), numpy.int64)
    res.fill(EMPTY)
    first_visit = numpy.ones(len(tree), numpy.bool_)

    to_visit = deque([(root, None)])
    while len(to_visit) > 0:
        curr, parent = to_visit[-1]

        if res[curr] != EMPTY:
            to_visit.pop()
            continue

        is_leaf = len(tree[curr]) == 1 and tree[curr][0] == parent
        if is_leaf:
            # leaf node
            res[curr] = weights[curr]
            to_visit.pop()
            continue

        if first_visit[curr]:
            # has children but is not calculated and visited first time - continue
            first_visit[curr] = False
            if not is_leaf:
                to_visit.extend((x, curr) for x in reversed(tree[curr]) if x != parent and res[x] == EMPTY)
            continue

        children_are_calculated = all(res[x] != EMPTY for x in tree[curr] if x != parent)
        grandchildren_are_calculated = all(res[g] != EMPTY for x in tree[curr] for g in tree[x] if x != parent and g != curr)

        if children_are_calculated and grandchildren_are_calculated:
            # great, time to calc res[curr]
            children_sum = sum(res[x] for x in tree[curr] if x != parent)
            grandchildren_sum = sum(res[g] for x in tree[curr] for g in tree[x] if x != parent and g != curr)
            curr_sum = max(children_sum, grandchildren_sum + weights[curr])
            res[curr] = curr_sum
            to_visit.pop()

    return res[root]


example_input1 = """1
1000"""

example_input2 = """2
1 2
1 2"""

example_input3 = """5
1 5 3 7 5
5 4
2 3
4 2
1 2"""


def main(_inp=None):
    tree_data, weights = process_input(_inp)
    res = calc_independent_set(tree_data, weights)
    return res

if __name__ == '__main__':
    print(main())