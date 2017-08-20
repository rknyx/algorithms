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
from collections import deque

# should i reverse graph at the beginning?
# think no?

def dfs(data, start_from, pre=None, post=None):
    to_process = deque()
    visited = set()

    to_process.append(start_from)
    while len(to_process) > 0:
        curr = to_process.popleft()
        if curr in visited:
            continue
        if pre is not None:
            pre(curr)
        if data[curr] is None:
            continue
        to_process.extend(data[curr])
        if post is not None:
            post(curr)
    return visited

class Graph:
    def __init__(self, size):
        self._data = [None] * (size * 2)
        self._size = size
        self._scc = []
        self._post_numbers = [None] * (size * 2)
        self.post_order_counter = 0
        self.largest_post_order = None

    def _address(self, num):
        return num - 1 if num > 0 else num + self._size - 1

    def deaddress(self, num):
        return num + 1 if num < self._size else num - self._size + 1

    def _init_address(self, address):
        address = self._address(address)
        negated_address = self._address(-address)
        data = self._data

        data[address] = [] if data[address] is None else data[address]
        data[negated_address] = [] if data[negated_address] is None else data[negated_address]
        return address

    def add_implication(self, source, dest):
        to_process = [(-source, dest), (-dest, source)] if source != dest else [(-source, source)]
        for source, dest in to_process:
            address_source = self._init_address(self._address(source))
            address_dest = self._init_address(self._address(dest))
            self._data[address_source].append(address_dest)

    @staticmethod
    def reversed_of(other):
        size = other._size
        graph = Graph(size)
        other_data = other._data
        curr_data = graph._data

        for vertex_num in range(other_data):
            neighbors = other_data[vertex_num]
            if neighbors is None or len(neighbors) == 0:
                continue
            for neighbor in neighbors:
                curr_data[neighbor].append(vertex_num)
        return graph

    def largest_post_vertex(self):
        """returns vertex num with the largest postnumber"""
        last_post_number = 0
        max_post_number, max_post_vertex = last_post_number, 0
        visited = set()

        def assign_post_number(vertex):
            nonlocal last_post_number, max_post_number, max_post_vertex
            last_post_number += 1
            max_post_vertex, max_post_number = (vertex, last_post_number) if last_post_number > max_post_number else (max_post_vertex, max_post_number)

        for vertex_num in range(len(self._data)):
            if vertex_num in visited:
                continue
            visited += dfs(self._data, post=assign_post_number)
        return max_post_vertex

    def explore(self, vertex_num):
        res = []
        dfs(self._data, start_from=vertex_num, pre=lambda vertex: res.append(vertex))
        return res

    def remove(self, vertices):
        for vertex_num in range(len(self._data)):
            if vertex_num in vertices:
                self._data[vertex_num] = None
            else:
                self._data[vertex_num] = [x for x in self._data[vertex_num] if x not in vertices]


def read_test_example():
    return """3 3
1 -3
-1 2
-2 -3"""


def process_input():
    # lines = stdin.readlines()
    lines = read_test_example().split("\n")
    variables_count, clauses_count = lines[0]
    graph = Graph(variables_count)
    for clause in lines[1:]:
        left, right = map(int, clause.split(" "))
        graph.add_implication(left, right)
    return graph


def calc_satisfaibility(graph):
    scc = []
    processed_count = 0
    reversed_graph = Graph.reversed_of(graph)
    while processed_count < len(graph._data):
        sink = reversed_graph.largest_post_vertex()
        sink_vertices = graph.explore(sink)
        processed_count += len(sink_vertices)
        scc.append(set(map(graph.deaddress, sink_vertices)))
        graph.remove(sink_vertices)
        reversed_graph.remove(sink_vertices)

    for component in scc:
        for vertex in component:
            if -vertex in component:
                return "UNSATISFIABLE"

    result = [None] * graph._size
    # solution is satisfiable here, need only to return satisfying assignment
    for component in scc:
        for vertex in (x for x in component if result[x] is None):
            result[vertex] = vertex if vertex > 0 else -vertex
    return result

if __name__ == '__main__':
    graph = process_input()
    res = calc_satisfaibility(graph)
    if "UNSATISFIABLE" == res:
        print(res)
        exit(0)

    print("SATISFIABLE")
    print(" ".join(map(str, res)))
