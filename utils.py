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
    """
        If the steps to a solution have consecutive repeats of the same move, then this function
        will filter them out appropriately.

        (Ex.)
        "L" -> "L"
        "L L" -> "L L"
        "L L L" -> "L'"
        "L L L L" -> ""
    """
    # steps = steps.split()
    soln = []

    if len(steps) == 1:
        return " ".join(steps)
    if len(steps) > 1 and steps[1] != steps[0]:
        soln.append(steps[0])

    repeats = 1

    # if len(steps) > 1 and steps[1] == steps[0]:
    #     repeats = 2

    i = 1
    while i < len(steps):
        if steps[i] != steps[i-1]:
            soln.append(steps[i])
            i+=1
            continue
    
        while i < len(steps) and steps[i] == steps[i-1]:
            repeats+=1
            i+=1  
        repeats = repeats % 4
        # soln = soln[:-1]
        if repeats == 1:
            soln.append(steps[i - 1])
        if repeats == 2:
            soln.append(steps[i-1])
            soln.append(steps[i-1])
        if repeats == 3:
            soln.append(get_inverse(steps[i-1]))
        repeats = 1 
    return soln




