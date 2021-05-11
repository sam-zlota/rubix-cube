
from constants import *
from model import *
from solver import *
from utils import *
import time
import multiprocessing


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
        assert a == b
        random_sequence = get_random_seq()
        a.apply_seq(random_sequence)
        b.apply_seq(random_sequence)
        assert a == b
        inverse_sequence = get_inverse_sequence(random_sequence)
        a.apply_seq(inverse_sequence)
        b.apply_seq(inverse_sequence)
    
    print("Success!")
    print("time: ", (time.time() - start_time)*1000, "ms")

def test_handle_inverses():
    start_time = time.time()

    for i in range(3000):
        test = get_random_seq()
        test.extend(get_random_seq())
        random.shuffle(test)
        before = len(test)
        c = Cube()
        d = Cube()

        shorter = handle_inverses(test)
        # shorter = handle_repeats(test)
        after = len(shorter)
        if i % 100 == 0:
            print(i, "completed")
            print("sample: ", before, "===>", after, "| diff: ", before - after)
        c.apply_seq(test)
        d.apply_seq(shorter)
        assert c == d
    print("Success!")
    print("time: ", (time.time() - start_time), "s")

def test_handle_repeats():
    start_time = time.time()

    for i in range(1000):
        test = get_random_seq()
        test.extend(get_random_seq())
        random.shuffle(test)

        before = len(test)
        c = Cube()
        d = Cube()

        # shorter = handle_inverses(test)
        shorter = handle_repeats(test)
        after = len(shorter)
        if i % 100 == 0:
            print(i, "completed")
            print("sample: ", before, "===>", after, "| diff: ", before - after)
        c.apply_seq(test)
        d.apply_seq(shorter)
        assert c == d
    print("Success!")
    print("time: ", (time.time() - start_time), "s")

    

def test_builtins():
    start_time = time.time()
    seen = []
    for i in range(100000):
        a = Cube()
        a.apply_seq(get_random_seq())

        hash_a = a.__hash__()
        
        if hash_a in seen:
            print(">>>>>>>>>>>>>>>COLLISION<<<<<<<<<<<<<<<<")
        seen.append(hash_a)
        # try:
        # except AssertionError as E:
        #     print(a)
        #     print(b)
        #     raise AssertionError

    print("Success!")
    print("time: ", (time.time() - start_time), "s")

if __name__ == "__main__":
    # test_cube_solved()
    # test_cube_equal()
    # test_handle_repeats()
    # test_builtins()
    # test_handle_inverses()

    test_handle_repeats()