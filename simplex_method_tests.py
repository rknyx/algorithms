from simplex_method import stupid_simplex

inputs = [(
    """3 2
-1 -1
1 0
0 1
-1 2 2
-1 2""", """Bounded solution
0.000000000000000 2.000000000000000
"""), ("""2 2
1 1
-1 -1
1 -2
1 1""", """No solution"""), ("""1 3
0 0 1
3
1 1 1""", """Infinity""")]

inputs = [(x.split("\n"), y) for x,y in inputs]

if __name__ == '__main__':
    for _input, res_expected in inputs:
        res_actual = stupid_simplex(_input).strip()
        res_expected = res_expected.strip()
        if stupid_simplex(_input) != res_expected:
            raise Exception("Input: '%s', res expected is '%s', but actual: '%s'" % (_input, res_expected, res_actual))
    print("Tests passed")