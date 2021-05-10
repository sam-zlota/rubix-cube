from model import Cube
from constants import *
from utils import *
from solver import Solver
import random
import time


def get_mixed_cube():
    seq = get_random_seq()
    c = Cube()
    c.apply_seq(seq)
    return c

def test_solve_daisy():

    for i in range(10):
        print("running test: ", i)
        c = get_mixed_cube()
        # print("'start state')
        print(c.print_v2())
        s = Solver(c)
        assert not s.check_daisy()
        sequence = s.solve_daisy()
        print(sequence)
        assert s.check_daisy()
        print(c.print_v2())

    
    print("test passed!")

def test_solve_white_cross():
    start_time = time.time()
    for i in range(1000):
        c = get_mixed_cube()
        s = Solver(c)
        assert not s.check_white_cross()
        sequence = s.solve()
        assert s.check_white_cross()
        if i % 100 == 0:
            print(i, " complete")

    
    print("Success!")
    print("time: ", (time.time() - start_time), "s")

def test_solve_white_corners():
    start_time = time.time()
    for i in range(1000):
        c = get_mixed_cube()
        s = Solver(c)
        assert not s.check_white_corners()
        sequence = s.solve()
        assert s.check_white_corners()
        if i % 250 == 0:
            print(len(sequence), sequence)
            print(s.cube)

            print(i, " complete")

    
    print("Success!")
    print("time: ", (time.time() - start_time), "s")
    

def test_solve_middle_layer():
    start_time = time.time()
    for i in range(1000):
        c = get_mixed_cube()
        s = Solver(c)
        assert not s.check_middle_layer()
        sequence = s.solve()
        assert s.check_middle_layer()
        print(s.cube)
        if i % 250 == 0:
            print(len(sequence), sequence)
            print(s.cube)

            print(i, " complete")

    
    print("Success!")
    print("time: ", (time.time() - start_time), "s")


if __name__ == "__main__":
    #test_reorient('down')
    test_solve_middle_layer()