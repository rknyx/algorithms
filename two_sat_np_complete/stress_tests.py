import os, sys
from itertools import combinations
import time
from two_sat_np_complete.two_sat import main

inputs_sat = [
    """3 3
1 -3
-1 2
-2 -3""",
    """2 7
1 1
1 2
1 2
1 2
2 1
2 1
2 1""",
    """4 4
1 -1
2 -2
3 -3
4 -4""",
    """1 1
-1 -1""",
    """2 1
1 2""",
    """2 1
1 -2""",
    """1 3
1 1
1 1
1 1""",
    """3 11
1 1
1 1
-2 -2
1 1
-2 -2
1 1
3 3
-2 -2
1 1
3 3
3 3""",
    """1 2
-1 -1
-1 -1""",
    """5 5
5 -5
4 4
3 3
2 2
1 1""",
    """4 4
-1 2
-3 4
-2 3
-1 4
3 3""", """14 7
1 2
3 4
5 6
7 8
9 10
11 12
13 14""",
    """4 16
1 1
1 2
1 3
1 4
2 1
2 2
2 3
2 4
3 1
3 2
3 3
3 4
4 1
4 2
4 3
4 4""",
    """4 11
-2 1
-2 -3
-2 -4
3 -1
-3 2
3 -3
3 4
-4 -1
-4 -3
-1 2
1 4"""]

inputs_unsat = [
    """2 4
1 2
-1 -2
-1 2
1 -2""",
    """1 2
1 1
-1 -1""",
    """3 4
1 2
-2 3
-1 -1
-3 -3""",
    """5 6
5 5
4 4
3 3
2 2
1 1
-5 -5""",
    """4 12
-2 1
-2 -3
-2 -4
3 -1
-3 2
3 -3
3 4
-4 -1
-4 -3
-1 2
1 4
1 3"""
]

graph1 = [[1], [2], [3], [4], [5], [6], [7], [0], [7, 10], [8], [9]]


class GraphGenerator:
    def __init__(self):
        self._vertex_counter = 0
        self._data = []

    def weak_scc(self, count):
        one_per_scc_vertex = []
        for _ in range(count):
            num1 = self._vertex_counter
            num2, num3 = num1 + 1, num1 + 2
            self._data += [[num2], [num3], [num1]]
            self._vertex_counter += 3
            one_per_scc_vertex.append(num1)
        return one_per_scc_vertex

    def pairwise_connected_scc(self, count):
        res = self._vertex_counter
        numbers = range(self._vertex_counter, self._vertex_counter + count)
        self._data = self._data + [None] * count
        combs = combinations(numbers, 2)
        for left, right in combs:
            self._data[left] = [] if self._data[left] is None else self._data[left]
            self._data[right] = [] if self._data[right] is None else self._data[right]
            self._data[left].append(right)
            self._data[right].append(left)
        self._vertex_counter += count
        return res

    def connect(self, num1, num2):
        self._data[num1].append(num2)

    def get_data(self):
        return self._data

    def reset(self):
        self._data = []
        self._vertex_counter = 0


def test_main():
    try:
        for inp in inputs_sat:
            res = main(inp)
            print("=== new test ===")
            print("test input: '%s'" % inp)
            print("res: \n'%s'\n" % res)
            assert "UNSATISFIABLE" not in res

        for inp in inputs_unsat:
            res = main(inp)
            print("=== new test ===")
            print("test input: '%s'" % inp)
            print("res: \n'%s'\n" % res)
            assert "UNSATISFIABLE" in res
    except:
        print("fail during testcase")


def test_stress():
    print("test stress")
    _filename = os.path.join(os.getcwd(), "case_1000_100.txt")
    with open(_filename, 'r') as f:
        inp = f.read()
        res = main(inp)
        assert "UNSATISFIABLE" not in res
        assert "SATISFIABLE" in res

    _filename = os.path.join(os.getcwd(), "case_400_1000.txt")
    with open(_filename, 'r') as f:
        inp = f.read()
        res = main(inp)
        assert "UNSATISFIABLE" not in res
        assert "SATISFIABLE" in res


def test_large_stress():
    print("large stress")
    _filename = os.path.join(os.getcwd(), "stress_400000_1000000.txt")
    with open(_filename, 'r') as f:
        inp = f.read()
        res = main(inp)
        assert "UNSATISFIABLE" not in res
        assert "SATISFIABLE" in res


if __name__ == '__main__':
    test_main()
    test_stress()
    prev = time.time()
    test_large_stress()
    print("time is '%s'" % (time.time() - prev))
