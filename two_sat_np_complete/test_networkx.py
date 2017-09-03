from two_sat_np_complete.two_sat import *
from networkx.generators.random_graphs import gnm_random_graph
from networkx import DiGraph
from networkx.algorithms.components import strongly_connected_components


def networkx_to_my(other, vertex_count):
    edges = other.edges()
    _data = [[] for _ in range(vertex_count)]
    for left, right in edges:
        _data[left].append(right)
    my_graph = Graph(1)
    my_graph._data = _data
    my_graph._size = vertex_count
    return my_graph


def compare_scc(my, other):
    my_by_set = [set(x) for x in my]
    for _set in my_by_set:
        if _set not in other:
            return False
    return True


def problem_graph1():
    ntx = DiGraph()
    edges = [(0, 7), (1, 2), (1, 0), (2, 5), (3, 2), (3, 4), (4, 3), (4, 0), (4, 5), (5, 4), (5, 0), (5, 6), (6, 2), (6, 0)]
    data = [[] for _ in range(8)]
    for edge in edges:
        ntx.add_edge(*edge)
        data[edge[0]].append(edge[1])

    my_graph = Graph(1)
    my_graph._data = data
    my_graph._size = 8
    scc_networkx = list(strongly_connected_components(ntx))
    scc_my = calc_scc(my_graph)
    assert compare_scc(scc_my, scc_networkx)


def problem_graph2():
    ntx = DiGraph()
    edges = [(0, 6), (1, 2), (1, 0), (2, 6), (2, 1), (2, 3), (3, 4), (4, 1), (4, 2), (5, 0), (5, 2), (7, 4), (7, 6), (7, 2)]
    data = [[] for _ in range(8)]
    for edge in edges:
        ntx.add_edge(*edge)
        data[edge[0]].append(edge[1])

    my_graph = Graph(1)
    my_graph._data = data
    my_graph._size = 8
    scc_networkx = list(strongly_connected_components(ntx))
    scc_my = calc_scc(my_graph)
    assert compare_scc(scc_my, scc_networkx)


def test_scc():
    vertex_count = 8
    edges_count = 14
    tests_count = 5

    for _ in range(tests_count):
        ntx_graph = gnm_random_graph(vertex_count, edges_count, directed=True)
        my_graph = networkx_to_my(ntx_graph, vertex_count)
        scc_networkx = list(strongly_connected_components(ntx_graph))
        scc_my = calc_scc(my_graph)
        res = compare_scc(scc_my, scc_networkx)
        assert res


if __name__ == '__main__':
    test_scc()
    problem_graph2()
    problem_graph1()