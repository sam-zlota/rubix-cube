from constants import up, down, left, right, front, back, y, w, r, o, g, b

import random

def get_random_seq():
    '''
    Returns a mixed up rubik's cube sequence
    '''
    
    actions = ["U", "U'", "F","F'","L", "L'", "R", "R'", "B", "B'", "D", "D'"]
    seq = []
    for i in range(100):
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

def face_solved(color, face):
    """
        Determines if face is solved.
    """
    solved = True
    for row in face:
        for square in row:
            solved = solved and square == color
    return solved

def cube_solved(cube):
    """
        Determines if cube is solved.
    """
    solved = True
    for color, face in cube.color_dict.items():
        solved = solved and face_solved(color, face)
    return solved

def face_equal(face1, face2):
    """
        Determines if two faces are equal.
    """
    equal = True
    n = len(face1)
    for i in range(n):
        for j in range(n):
            equal = equal and (face1[i][j] == face2[i][j])
    return equal

def cube_equal(cube1, cube2):
    """
        Determines if two cubes are equal.
    """
    equal = True
    cube1_faces = list(cube1.color_dict.values())
    cube2_faces = list(cube2.color_dict.values())
    n = len(cube1_faces)

    for i in range(n):
        equal = equal and (face_equal(cube1_faces[i], cube2_faces[i]))
    return equal

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




