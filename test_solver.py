# from efficent_model import EfficentCube
from matplotlib.pyplot import title
from model import Cube
from constants import *
from utils import *
from solver import Solver
import random
import time
import numpy as np


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
            print(
                len(concise), len(concise_2), "| diff: ",
                len(concise) - len(concise_2))
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
    actions_list = []
    times_list = []
    solved = Cube()
    for i in range(10000):
        shuffle = get_random_seq()
        c = Cube()
        c.apply_seq(shuffle)
        if i % 25000 == 0:
            print(
                "-------------------------------------------------------------------------------------------------------------------------------------------------------------"
            )
            print("Shuffle Sequence: ", shuffle)
            print(c)
        s = Solver(c)
        assert not c == solved
        start = time.time()
        s.solve()
        total = time.time() - start
        times_list.append(total * 1000)
        assert c == solved
        actions = clean(c.actions)
        actions_list.append(len(actions))
        if i % 25000 == 0:
            print(i, "Solved!")
            print(total * 1000, "ms")
            print(len(actions), "moves")
            print("Solved Sequence: ", actions)
            print(
                "-------------------------------------------------------------------------------------------------------------------------------------------------------------"
            )

        # print(len(actions), "diff", len(c.actions) - len(actions))
    print("\n\n***Final Report(N=10,000)***\n")
    import seaborn as sns
    import pandas as pd
    import matplotlib.pyplot as plt
    from scipy.stats import mode

    times_list = np.round(times_list, decimals=3)
    print("\t\t\tTime")
    print(
        "Average: ", round(sum(times_list) / len(times_list), 3), "ms",
        ", std: ", round(np.std(times_list), 3))
    print("Median: ", np.median(times_list), "ms")
    mode_arr, count = mode(times_list)
    print("Mode: ", mode_arr[0], ", n:", count[0])
    print("Max: ", max(times_list), "ms")
    print("Min: ", min(times_list), "ms")

    new_list = []
    std = round(np.std(times_list), 3)
    avg = round(sum(times_list) / len(times_list), 3)
    for time_ in times_list:
        if time_ <= (3 * std + avg) and time_ >= (avg - 3 * std):
            new_list.append(time_)
    times_list = new_list
    fig, axs = plt.subplots(figsize=(10, 7))
    sns.distplot(
        pd.Series(times_list, name="Times(ms)"),
        ax=axs)  # sns.distplot(actions_list)
    plt.show()
    print()
    print("\t\t\tActions")
    print(
        "Average: ", round(sum(actions_list) / len(actions_list), 3),
        ", std: ", round(np.std(actions_list), 3))
    print("Median: ", np.median(actions_list))
    mode_arr, count = mode(actions_list)
    print("Mode: ", mode_arr[0], ", n:", count[0])
    # print()

    print("Max: ", max(actions_list))
    print("Min: ", min(actions_list))
    print()
    fig, axs = plt.subplots(figsize=(10, 7))
    sns.distplot(
        pd.Series(actions_list, name="Actions(quarter-turn metric)"), ax=axs)
    # sns.distplot(actions_list)
    plt.show()

    # print("time: ", ( "s")


def speed_test(n):
    cube_list = []
    for i in range(n):
        c = Cube()
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
    c = speed_test(10)

    # print(total_size(c))
