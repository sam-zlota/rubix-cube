
from constants import *
from model import *
from solver import *
from utils import *
import time


def test_cube_solved():  
    c = Cube()
    start_time = time.time()
    for _ in range(100):
        assert cube_solved(c)
        random_sequence = get_random_seq()
        c.apply_seq(random_sequence)

        assert not cube_solved(c)

        inverse_sequence = get_inverse_sequence(random_sequence)
        c.apply_seq(inverse_sequence)
        assert cube_solved(c)
    
    print("Success!")
    print("time: ", (time.time() - start_time)*1000, "ms")

def test_cube_equal():  
    a = Cube()
    b = Cube()
    start_time = time.time()
    for _ in range(100):
        assert cube_equal(a, b)
        random_sequence = get_random_seq()
        a.apply_seq(random_sequence)
        b.apply_seq(random_sequence)
        assert cube_equal(a, b)
        inverse_sequence = get_inverse_sequence(random_sequence)
        a.apply_seq(inverse_sequence)
        b.apply_seq(inverse_sequence)
    
    print("Success!")
    print("time: ", (time.time() - start_time)*1000, "ms")


def test_handle_repeats():

    a = Cube()
    b = Cube()
    start_time = time.time()

    for _ in range(100):
        random_sequence = get_random_seq()
        pruned_sequence = handle_repeats(random_sequence)
        a.apply_seq(random_sequence)
        b.apply_seq(pruned_sequence)
        assert cube_equal(a, b)

        a = Cube()
        b = Cube()


    a = Cube()
    b = Cube()
    s_a = Solver(a)
    s_b = Solver(b)

    for _ in range(100):
        random_sequence = get_random_seq()
        print(random_sequence)
        a.apply_seq(random_sequence)
        b.apply_seq(random_sequence)
        assert cube_equal(a, b)

        s_a = Solver(a)
        s_b = Solver(b)
        white_cross_sequence = s_a.solve()
        pruned = handle_repeats(white_cross_sequence)
        print(white_cross_sequence)
        print(pruned)

        print("Diff: ", len(white_cross_sequence) - len(pruned))
        a.apply_seq(white_cross_sequence)
        b.apply_seq(pruned)
        assert s_a.check_white_cross()
        assert cube_equal(a, b) 
        
        a = Cube()
        b = Cube()

    
    print("Success!")
    print("time: ", (time.time() - start_time)*1000, "ms")


if __name__ == "__main__":
    test_cube_solved()
    test_cube_equal()
    test_handle_repeats()
