from constants import up, down, left, right, front, back, y, w, r, o, g, b

import random

def get_random_seq():
    '''
    Returns a mixed up rubik's cube sequence
    '''
    
    actions = ["U", "U'", "F","F'","L", "L'", "R", "R'", "B", "B'", "D", "D'"]
    seq = []
    for i in range(50):
        seq.append(random.choice(actions))
    return seq

def fill(n, color):
    '''
    Creates a three dimensional array with the given color string. 
    Array represents the solved state of a rubik's cube.
    '''
    arr = []
    sub_arr = []

    for i in range(n):
        for j in range(n):
            sub_arr.append(color)
        arr.append(sub_arr)
        sub_arr = []

    return arr

def get_opposite(color):
    '''
    Returns the opposite color to the given one on a 
    Rubik's cube.
    '''
    if color == y:
        return w
    if color == w:
        return y
    if color == r:
        return o
    if color == o:
        return r
    if color == b:
        return g
    if color == g:
        return b

def get_inverse(step):
    """
        Returns the inverse move for the given step. 
        (Ex.) get_inverse("U") ->  "U'"
    """
    if len(step) == 1:
        return step + "'"
    elif step[1] == "'":
        return step[0]
    elif step == "UU":
        return "DD"
    elif step == "DD":
        return "UU"
    elif step == "LL":
        return "RR"
    elif step == "RR":
        return "LL"
    else:
        raise Error 

def get_inverse_sequence(steps):
    
    res = []
    for step in steps:
        res.append(get_inverse(step))
    res.reverse()
    return res

def handle_repeats(steps):
    res = []
    curr = steps[0]
    ctr = 1
    for step in steps[1:]:
        if step == curr:
            ctr+=1
        else:
            repeats = ctr % 4
            # print("reps", repeats)
            if repeats == 1:
                res.append(curr)
            if repeats == 2:
                # print("HERE")
                res.append(curr)
                res.append(curr)
            if repeats == 3:
                res.append(get_inverse(curr))
            curr = step
            ctr = 1
    # 
    repeats = ctr % 4
    # print("reps", repeats)
    if repeats == 1:
        res.append(curr)
    if repeats == 2:
        res.append(curr)
        res.append(curr)
    if repeats == 3:
        res.append(get_inverse(curr))
    return res

def handle_inverses(steps):
    res = []
    res.append(steps[0])
    for step in steps[1:]:
        if len(res) > 0 and step == get_inverse(res[-1:][0]):
            res = res[:-1]
        else:
            res.append(step)
    return res

