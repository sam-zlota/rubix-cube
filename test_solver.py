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
        concise = handle_inverses(handle_repeats(sequence))
        concise_2 = handle_repeats(handle_repeats(sequence))
        if len(concise) > len(concise_2):
            print(len(concise), len(concise_2), "| diff: ", len(concise) - len(concise_2))
            print(">>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<")
        z = Cube()
        z.apply_seq(concise)
        assert z == s.cube
        assert s.check_white_corners()
        if i % 250 == 0:
            print(len(sequence), sequence)
            print(len(concise), concise)

            ctr = 0
            for act in sequence:
                if len(act) > 1 and act[1] == act[0]:
                    ctr += 1
            print("found cube rots: ", ctr)
            print("diff: ", len(sequence) - len(concise))
            print(s.cube)

            print(i, " complete")

    print("Success!")
    print("time: ", (time.time() - start_time), "s")

def stress_test():
    start_time = time.time()
    for i in range(5000):
        c = get_mixed_cube()
        s = Solver(c)
        assert not s.check_white_corners()
        sequence = s.solve()
        assert s.check_white_corners()
        if i % 250 == 0:
            print(i, "complete")
    print("Success!")
    print("time: ", (time.time() - start_time), "s")

def test_solve_middle_layer():
    start_time = time.time()
    diff_sum = diff_prct = 0
    n = 10000
    for i in range(n + 1):
        c = get_mixed_cube()

        s = Solver(c)
        assert not s.check_middle_layer()
        sequence = s.solve()
        assert s.check_middle_layer()
        if i % (n / 5) == 0:
            print(len(sequence), sequence)
            # print(len(cleaned), cleaned)
            print(s.cube)

            print(i, " complete")

    print("average diff:", diff_sum / n)
    print("average percent diff:", diff_prct / n)

    print("Success!")
    print("time: ", (time.time() - start_time), "s")

def test_hash():
    start = time.time()
    iters = 100_000
    samp = iters / 10
    for i in range(iters):
        c = Cube()
        random_seq = get_random_seq()
        c.apply_seq(random_seq)
        h = c.__hash__()
        if i % samp == 0:
            print(i, "complete")
            print(h)
    print("Finished!")
    print(iters, "iters\n ", "time: ", (time.time() - start), "s")

def test_solve_yellow_cross():
    start = time.time()
    for i in range(100):
        c = get_mixed_cube()
        s = Solver(c)
        assert not s.check_yellow_cross()
        s.solve()
        assert s.check_yellow_cross()
        if i % 20 == 0:
            print(s.cube)
    print("Success!")
    print("time: ", (time.time() - start), "s")

def test_solve_yellow_corners():
    start = time.time()
    for i in range(100):
        c = get_mixed_cube()
        s = Solver(c)
        assert not s.check_yellow_corners()
        s.solve()
        assert s.check_yellow_corners()
        if i % 20 == 0:
            print(s.cube)
    print("Success!")
    print("time: ", (time.time() - start), "s")

def test_solve_position_yellow_corners():
    start = time.time()
    for i in range(1):
        c = get_mixed_cube()
        s = Solver(c)
        # print(s.cube)
        assert not s.check_position_yellow_corners()
        s.solve()
        assert s.check_position_yellow_corners()
        # print(s.cube)
        if i % 100 == 0:
            print(s.cube)
    print("Success!")
    print("time: ", (time.time() - start), "s")

def test_solve_cube():
    start = time.time()
    solved = Cube()
    for i in range(50):
        c = get_mixed_cube()
        s = Solver(c)
        assert not c == solved
        s.solve()
        assert c == solved
        actions = clean(c.actions)
        print(len(actions), "diff", len(c.actions) - len(actions))
    print("Success!")
    print("time: ", (time.time() - start), "s")

def speed_test(n):
    cube_list = []
    for i in range(n):
        c = Cube()
        c.apply_seq(get_random_seq())
        c.apply_seq(get_random_seq())
        cube_list.append(c)
    start_time = time.time()
    for cube in cube_list:
        s = Solver(cube)
        s.solve()
    print("Finished solving", n, "cubes")
    finish_time = time.time() - start_time
    print(finish_time, "seconds")

if __name__ == "__main__":
    speed_test(1)
