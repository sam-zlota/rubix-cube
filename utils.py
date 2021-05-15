from __future__ import print_function
from constants import *
import random
from sys import getsizeof, stderr
from itertools import chain
from collections import deque
from reprlib import repr


def get_random_seq(n=100):
    '''
        Returns a mixed up rubik's cube sequence
    '''
    actions = [
        UP, UP_PRIME, FRONT, FRONT_PRIME, LEFT, LEFT_PRIME, RIGHT, RIGHT_PRIME,
        BACK, BACK_PRIME, DOWN, DOWN_PRIME
    ]
    seq = []
    for _ in range(n):
        seq.append(random.choice(actions))
    return seq


def is_solved(cube):
    """
        Determines if the cube is solved in any orientation.
    """
    for color in [RED, ORANGE, YELLOW, WHITE, GREEN, BLUE]:
        for i in range(3):
            for j in range(3):
                if cube[color, i, j] != color:
                    return False
    return True


def face_init(color):
    '''
        Creates a three dimensional array with the given color . 
    '''
    arr = []
    sub_arr = []
    n = 3
    for _ in range(n):
        for _ in range(n):
            sub_arr.append(color)
        arr.append(sub_arr)
        sub_arr = []

    return arr


def get_inverse_sequence(steps):
    """
        Returns the sequence of moves that will undo the specified sequence of moves.
        
        ["U'", "L", "F"] ==> ["F'", "L'", "U"]
    """
    res = []
    for step in steps:
        res.append(INVERSE[step])
    res.reverse()
    return res


def handle_repeats(steps):
    """
        Returns the sequence of moves with repeat moves handled in the following manner.

        Where x is any move:
            [x] ==> [x]
            [x, x] ==> [x, x]
            [x, x, x] ==> [x']
            [x, x, x, x] ==> []
        This applies to repeated sequences > 4, whre only the last n % 4 moves are considered for a
        sequence of length n.
        
    """
    res = []
    curr = steps[0]
    ctr = 1
    for step in steps[1:]:
        if step == curr:
            ctr += 1
        else:
            repeats = ctr % 4
            if repeats == 1:
                res.append(curr)
            if repeats == 2:
                res.append(curr)
                res.append(curr)
            if repeats == 3:
                res.append(get_inverse(curr))
            curr = step
            ctr = 1
    repeats = ctr % 4
    if repeats == 1:
        res.append(curr)
    if repeats == 2:
        res.append(curr)
        res.append(curr)
    if repeats == 3:
        res.append(get_inverse(curr))
    return res


def handle_inverses(steps):
    """
        Handles succesive commutative moves by removing them.

        ["U", "U'"] ==> []
    """
    res = []
    res.append(steps[0])
    for step in steps[1:]:
        if len(res) > 0 and step == INVERSE[res[-1:][0]]:
            res = res[:-1]
        else:
            res.append(step)
    return res


def handle_cube_rots(steps):
    #FIXME
    return steps


def clean(steps):
    """
        Cleans the sequence of steps by handling repeats and commutative moves.
    """
    return handle_cube_rots(handle_inverses(handle_repeats(steps)))


# #FIXME
# INT_BITS = 64

# # Function to left
# # rotate n by d bits
# def leftRotate(n, d):

#     # In n<<d, last d bits are 0.
#     # To put first 3 bits of n at
#     # last, do bitwise or of n<<d
#     # with n >>(INT_BITS - d)
#     return (n << d) | (n >> (INT_BITS - d))


# # Function to right
# # rotate n by d bits
# def rightRotate(n, d):

#     # In n>>d, first d bits are 0.
#     # To put last 3 bits of at
#     # first, do bitwise or of n>>d
#     # with n <<(INT_BITS - d)
#     return (n >> d) | (n << (INT_BITS - d)) & 0xFFFFFFFF
