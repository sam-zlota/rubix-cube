from model import Cube
from constants import *
from utils import *
from solver import Solver
import random


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

    for i in range(1):
        # print("running test: ", i)
        c = get_mixed_cube()
        # print("'start state')
        # print(c.print_v2())
        s = Solver(c)
        assert not s.check_white_cross()
        sequence = s.solve_daisy()
        sequence+= s.solve_white_cross()
        print(sequence)
        assert s.check_white_cross()
        print("success")

    
    print("test passed!")

def test_solve_white_corners():
    for i in range(10):
        # print("running test: ", i)
        c = get_mixed_cube()
        # print("'start state')
        # print(c.print_v2())
        s = Solver(c)
        assert not s.check_white_corners()
        sequence = s.solve()
        print(sequence)
        print(s.cube)
        assert s.check_white_corners()
        print("success")

    
    print("test passed!")
    


if __name__ == "__main__":
    #test_reorient('down')
    test_solve_white_corners()