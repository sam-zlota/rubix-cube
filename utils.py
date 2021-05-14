from constants import *
import random

def get_random_seq():
    '''
    Returns a mixed up rubik's cube sequence
    '''
    
    actions = [UP, UP_PRIME, FRONT,FRONT_PRIME,LEFT, LEFT_PRIME, RIGHT, RIGHT_PRIME, BACK, BACK_PRIME, DOWN, DOWN_PRIME]
    seq = []
    for _ in range(100):
        seq.append(random.choice(actions))
    return seq

def face_init(color):
    '''
    Creates a three dimensional array with the given color string. 
    Array represents the solved state of a rubik's cube.
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

def get_opposite(color):
    '''
    Returns the opposite color to the given one on a 
    Rubik's cube.
    '''
    if color == YELLOW:
        return WHITE
    if color == WHITE:
        return YELLOW
    if color == RED:
        return ORANGE
    if color == ORANGE:
        return RED
    if color == BLUE:
        return GREEN
    if color == GREEN:
        return BLUE

def get_inverse(step):
    """
        Returns the inverse move for the given step. 
        (Ex.) get_inverse(UP) ->  UP_PRIME
    """
    if len(step) == 1:
        return step + "'"
    elif step[1] == "'":
        return step[0]
    elif step == X_ROT:
        return X_ROT_PRIME
    elif step == X_ROT_PRIME:
        return X_ROT
    elif step == Y_ROT_PRIME:
        return Y_ROT
    elif step == Y_ROT:
        return Y_ROT_PRIME
    else:
        raise ValueError 

def get_inverse_sequence(steps):
    """
        Returns the sequence of moves that will undo the specified sequence of moves.
        
        ["U'", "L", "F"] ==> ["F'", "L'", "U"]
    """
    res = []
    for step in steps:
        res.append(get_inverse(step))
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
            ctr+=1
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
        if len(res) > 0 and step == get_inverse(res[-1:][0]):
            res = res[:-1]
        else:
            res.append(step)
    return res
def handle_cube_rots(steps):
    res = []
    for step in steps:
        if not(len(step) > 1 and step[0]==step[1]):
            res.append(step)
    return res
    
def clean(steps):
    """
        Cleans the sequence of steps by handling repeats and commutative moves.
    """
    return handle_cube_rots(handle_inverses(handle_repeats(steps)))


