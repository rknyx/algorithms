#python3
# Problem description
# 2SAT problem is special case of n-sat problem and is reduced to linear graph-algorithm
# We should introduce implication for each "or" clause: x || y. The implication is x => y.
# we build implicaitons in form: !x => y  which means "if x is zero, y should be one"
# now we build directed graph: each edge corresponds to an implication.
# After than - determine if any strongly connected component (SCC) contains both variable and it's negation
# if such component exists - formula is unsatisfiable. Else - sort SCC in topological order and for each SCC
# assign 1 for variables and 0 for their negations. Solution is ready.
from sys import stdin
import sys
import threading
from collections import deque
import numpy
import warnings
import resource
warnings.filterwarnings("ignore")

sys.setrecursionlimit(10**9) # max depth of recursion
threading.stack_size(2**26)
resource.setrlimit(resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))

EMPTY = -999999999
GLOBAL_DATA = None
GLOBAL_POST_NUMBERS = None
GLOBAL_VISITED = None
GLOBAL_LAST_POST_NUMBER = None


def dfs_recursive(vertex_num):
    global GLOBAL_DATA
    global GLOBAL_POST_NUMBERS
    global GLOBAL_VISITED
    global GLOBAL_LAST_POST_NUMBER
    GLOBAL_VISITED[vertex_num] = True
    for child in (c for c in GLOBAL_DATA[vertex_num] if not GLOBAL_VISITED[c]):
        dfs_recursive(child)

    GLOBAL_LAST_POST_NUMBER += 1
    GLOBAL_POST_NUMBERS[vertex_num] = GLOBAL_LAST_POST_NUMBER


def explore_non_recursive(data, vertex_num, visited):
    scc = []
    stack = deque([vertex_num])
    while len(stack) > 0:
        curr = stack.pop()
        if visited[curr]:
            continue
        scc.append(curr)
        visited[curr] = True
        stack.extend(reversed(data[curr]))
    return scc


def bulk_deadress(vertices, base_size):
    return [num + 1 if num < base_size else -(num - base_size + 1) for num in vertices]


class Graph:
    def __init__(self, size=None):
        if size is not None:
            self._data = [[] for _ in range(size * 2)]
            self._size = size

    def _address(self, num):
        return num - 1 if num > 0 else abs(num) + self._size - 1

    def _bulk_address(self, nums):
        return (x - 1 if x > 0 else abs(x) + self._size - 1 for x in nums)

    def deaddress(self, num):
        return num + 1 if num < self._size else -(num - self._size + 1)

    def add_implication(self, source, dest):
        minus_addr_source, minus_addr_dest, addr_source, addr_dest = self._bulk_address([-source, -dest, source, dest])
        data = self._data
        if source != dest:
            data[minus_addr_source].append(addr_dest)
            data[minus_addr_dest].append(addr_source)
        else:
            data[minus_addr_source].append(addr_source)

    @staticmethod
    def reversed_of(other):
        graph = Graph()
        graph._size = other._size
        other_data = other._data
        curr_data = [[] for _ in range(len(other_data))]
        graph._data = curr_data

        for vertex_num in (x for x in range(len(other_data)) if len(other_data[x]) > 0):
            neighbors = other_data[vertex_num]
            for neighbor in neighbors:
                curr_data[neighbor].append(vertex_num)
        return graph

    def build_topological_paths(self):
        global GLOBAL_DATA
        global GLOBAL_POST_NUMBERS
        global GLOBAL_VISITED
        global GLOBAL_LAST_POST_NUMBER
        data = self._data
        data_len = len(data)
        post_numbers = numpy.ndarray(data_len, numpy.int64)
        post_numbers.fill(EMPTY)
        visited = numpy.zeros(data_len, numpy.bool_)
        max_post_number = -1

        GLOBAL_DATA = data
        GLOBAL_POST_NUMBERS = post_numbers
        GLOBAL_VISITED = visited
        GLOBAL_LAST_POST_NUMBER = max_post_number

        for curr_vertex in range(data_len):
            if visited[curr_vertex]:
                continue
            dfs_recursive(curr_vertex)

        vertices_by_post_numbers = numpy.ndarray(len(post_numbers), numpy.int64)
        for vertex_number, post_number in enumerate(post_numbers):
            vertices_by_post_numbers[post_number] = vertex_number
        return reversed(vertices_by_post_numbers)


def process_input(inp):
    lines = stdin.readlines() if inp is None else inp.split("\n")
    variables_count, clauses_count = map(int, lines[0].split(" "))
    graph = Graph(variables_count)
    max_vertex = 0
    for clause in lines[1:]:
        left, right = map(int, clause.split(" "))
        graph.add_implication(left, right)
        max_vertex = max(max_vertex, abs(left), abs(right))
    return graph


def calc_scc(graph):
    scc = []
    reversed_graph = Graph.reversed_of(graph)
    vertices_to_traverse = reversed_graph.build_topological_paths()
    visited = numpy.zeros(len(graph._data), numpy.bool_)
    for vertex in vertices_to_traverse:
        if visited[vertex]:
            continue
        curr_css = explore_non_recursive(graph._data, vertex, visited)
        scc.append(curr_css)
    return scc


def calc_satisfaibility(graph):
    data_size = len(graph._data)
    result = numpy.ndarray(data_size, numpy.int64)
    result.fill(EMPTY)
    processed_in_other_scc = numpy.zeros(data_size, numpy.bool_)
    scc = calc_scc(graph)

    for component in scc:
        deadressed = bulk_deadress(component, graph._size)
        for vertex in deadressed:
            index = abs(vertex) - 1
            if processed_in_other_scc[index]:
                continue
            if result[index] == -vertex:
                return "UNSATISFIABLE"
            result[index] = vertex

        for vertex in deadressed:
            processed_in_other_scc[abs(vertex) - 1] = True
    return result


def main(inp=None):
    graph = process_input(inp)
    if "UNSATISFIABLE" == graph:
        return graph
    res = calc_satisfaibility(graph)
    if "UNSATISFIABLE" == res:
        return res

    return "SATISFIABLE\n" + " ".join(map(str, res[res != EMPTY]))

if __name__ == '__main__':
    print(main())