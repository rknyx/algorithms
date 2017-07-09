#python3

from sys import stdin


def read_real_input():
    return stdin.readlines()


def test_input_1():
    return """4
1 0 0 0 5
0 1 0 0 6
0 0 0 1 6
0 0 1 0 7"""


def format_float(fl):
    return "{0:.3f}".format(fl)


def print_array(data):
    print("\n".join([" ".join(map(format_float, data[i])) for i in range(len(data))]))


def read_input():
    lines = stdin.readlines()
    # lines = test_input_1().split("\n")
    size = int(lines[0])
    if size == 0:
        return None
    lines = lines[1:]
    data = [[None] * (size + 1) for _ in range(size)]

    for i in range(size):
        line_int = list(map(float, lines[i].split(" ")))
        for k in range(size + 1):
            data[i][k] = line_int[k]
    return data


def swap_lines(data, a, b):
    data[a], data[b] = data[b], data[a]


def divide_line(data, line_num, number):
    if number != 1.0:
        number = float(number)
        data[line_num] = [x / number for x in data[line_num]]


def subtract(data, subtract_what_num, subtract_from_num, factor=1.0):
    data[subtract_from_num] = [pair[0] - (pair[1]*factor) for pair in zip(data[subtract_from_num], data[subtract_what_num])]


def solve(data):
    data_size = len(data)

    for equation_num in range(data_size):
        line_to_swap = equation_num + 1
        while data[equation_num][equation_num] == 0:
            swap_lines(data, equation_num, line_to_swap)
            line_to_swap += 1
        if data[equation_num][equation_num] == 0:
            return None

        divide_line(data, equation_num, data[equation_num][equation_num])
        for line_from_to_subtract in range(data_size):
            if line_from_to_subtract == equation_num:
                continue
            factor = data[line_from_to_subtract][equation_num] / data[equation_num][equation_num]
            if factor != 0.0:
                subtract(data, equation_num, line_from_to_subtract, factor)

    return " ".join(map(format_float, (line[-1] for line in data)))

if __name__ == '__main__':
    input = read_input()
    if input is None:
        exit(0)

    print(solve(input))