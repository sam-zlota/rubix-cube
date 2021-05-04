from constants import up, down, left, right, front, back, y, w, r, o, g, b

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