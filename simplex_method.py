#python3

from operator import mul
from sys import stdin
from itertools import chain, combinations

FLOAT_EQUALITY_THRESHOLD = 0.0001


def multiply(left_trans, right):
    return map(mul, left_trans, right)


def scalar_multiply(a, b):
    return sum(multiply(a, b))


def float_equal(a, b):
    global FLOAT_EQUALITY_THRESHOLD
    return abs(a - b) < FLOAT_EQUALITY_THRESHOLD


def less(a, b):
    return b - a > FLOAT_EQUALITY_THRESHOLD


def more(a, b):
    return a - b > FLOAT_EQUALITY_THRESHOLD


def float_zero(a):
    return float_equal(a, 0.0)


def less_or_equal(a, b):
    return float_equal(a, b) or b - a > FLOAT_EQUALITY_THRESHOLD


def more_or_equal(a, b):
    return float_equal(a, b) or a - b > FLOAT_EQUALITY_THRESHOLD


def gaussian_elimination(data):
    data_size = len(data)

    for equation_num in range(data_size):
        line_to_swap = equation_num + 1
        while float_zero(data[equation_num][equation_num]) and line_to_swap < data_size:
            swap_lines(data, equation_num, line_to_swap)
            line_to_swap += 1
        if float_zero(data[equation_num][equation_num]):
            return None

        divide_line(data, equation_num, data[equation_num][equation_num])
        for line_from_to_subtract in range(data_size):
            if line_from_to_subtract == equation_num:
                continue
            factor = data[line_from_to_subtract][equation_num] / data[equation_num][equation_num]
            if factor != 0.0:
                subtract(data, equation_num, line_from_to_subtract, factor)

    return [line[-1] for line in data]


def subtract(data, subtract_what_num, subtract_from_num, factor=1.0):
    data[subtract_from_num] = [pair[0] - (pair[1]*factor) for pair in zip(data[subtract_from_num], data[subtract_what_num])]


def swap_lines(data, a, b):
    data[a], data[b] = data[b], data[a]


def divide_line(data, line_num, number):
    if number != 1.0:
        number = float(number)
        data[line_num] = [x / number for x in data[line_num]]


def normalize(vector):
    mod = float(sum(map(mul, vector, vector)))
    return [x / mod for x in vector]


def read_test_example1():
    return """3 2
-1 -1
1 0
0 1
-1 2 2
-1 2"""

NO_SOLUTION = -1
INFINITY_SOLUTION = -2
INFINITY_NUM = 9999999999


def format_float(fl):
    return "{0:.15f}".format(fl)


def array_to_string(data):
    return " ".join(map(format_float, data))


def is_suitable_solution(vector, inequalities):
    more_than_inequalities = inequalities[-len(vector):]
    less_than_inequalities = inequalities[:-len(vector)]
    scm = scalar_multiply
    all_less_then = all(less_or_equal(scm(vector, inequality[:-1]), inequality[-1]) for inequality in less_than_inequalities)
    all_more_then = all(more_or_equal(scm(vector, inequality[:-1]), inequality[-1]) for inequality in more_than_inequalities)
    return all_less_then and all_more_then


def is_infinity_check_vector(vector):
    all_are_ones = all(float_equal(x, 1.0) for x in vector[:-1])
    last_is_inf = float_equal(vector[-1], INFINITY_NUM)
    return all_are_ones and last_is_inf


def _stupid_simplex(inequalities, pleasures, dishes_count):
    inequalities_count = len(inequalities)
    combs = combinations(range(inequalities_count), dishes_count)

    max_target_function = float("-inf")
    best_vector = None
    # res_count = 0
    final_inf_solution = False
    for comb in combs:
        gauss_res = gaussian_elimination([list(inequalities[x]) for x in comb])
        # res_count += 1 if gauss_res is not None else 0
        if gauss_res is None or not is_suitable_solution(gauss_res, inequalities):
            continue
        target_function = scalar_multiply(pleasures, gauss_res)
        local_inf_solution = any(is_infinity_check_vector(vector) for vector in (inequalities[x] for x in comb))
        if more(target_function, max_target_function) or (float_equal(target_function, max_target_function) and not local_inf_solution):
            max_target_function, best_vector = target_function, gauss_res
            final_inf_solution = local_inf_solution

    if final_inf_solution:
        return "Infinity"
    elif best_vector is None:
        return "No solution"
    else:
        return "Bounded solution\n" + array_to_string(best_vector)


def process_input(lines):
    # lines = stdin.readlines()
    # lines = read_test_example1()
    # lines = lines.split("\n")
    restrictions_count, variables_count = map(int, lines[0].split(" "))
    lines = lines[1:]

    inequalities = [None for _ in range(restrictions_count + variables_count + 1)]
    pleasures = list(map(float, lines[restrictions_count + 1].split(" ")))
    right_parts = list(map(float, lines[restrictions_count].split(" ")))

    i = 0
    for _ in range(restrictions_count):
        inequalities[i] = list(chain(map(float, lines[i].split(" ")), [right_parts[i]]))
        i += 1

    # special inequality to check infinity solution
    inequalities[i] = [1] * variables_count + [INFINITY_NUM]
    i += 1

    # add non-negative restrictions
    for k in range(variables_count):
        inequalities[i] = [0] * k + [1] + [0] * (variables_count - k)
        i += 1
    return inequalities, pleasures, variables_count


def stupid_simplex(_input=None):
    _input = stdin.readlines() if _input is None else _input
    inequalities, pleasures, variables_count = process_input(_input)
    return _stupid_simplex(inequalities, pleasures, variables_count)

if __name__ == '__main__':
    print(stupid_simplex())