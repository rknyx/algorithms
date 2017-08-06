import os
import sys
from subprocess import check_output, call, Popen, PIPE

INPUT_FILES_DIR = "input_data"
UNSATISFIABLE_SOLUTION = "2 1\n1 0\n-1 0"
SATISFIABLE_SOLUTION = "1 1\n1 -1 0"
EXECUTABLE = "hamiltonian_path.py"
EXCHANGER = "exchange.txt"

path_join = os.path.join


def readfile(_file):
    open(_file, "r").readlines()


def minisat(cmd):
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    p.wait()
    output, err = p.communicate()
    return str(output)


def test(_file, excepted_sat):
    call("/bin/echo -n 'p cnf ' > exchange.txt", shell=True)
    check_output("python %s < %s >> exchange.txt" % (EXECUTABLE, path_join(INPUT_FILES_DIR, _file)), stderr=sys.stderr, shell=True)
    minisat_output = minisat("minisat exchange.txt")
    actual = "UNSATISFIABLE" not in str(minisat_output)
    if actual != excepted_sat:
        raise Exception("File '%s', expected: '%s', but actual is '%s'" % (_file, excepted_sat, actual))
    print(minisat_output)


if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_to_search = path_join(dir_path, INPUT_FILES_DIR)
    # try:
    for _file in os.listdir(dir_to_search):
        test(_file, "unsat" not in _file)
    # except Exception as e:
    #     print(e)

