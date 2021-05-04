from model import Cube
from constants import up, down, left, right, front, back, y, w, r, o, g, b

test_w = [['w', 'o', 'b'], ['y', 'w', 'b'], ['o', 'w', 'b']]
test_y = [['b', 'g', 'y'], ['y', 'y', 'w'], ['y', 'b', 'r']]
tets_g = [['g', 'o', 'o'], ['o', 'g', 'g'], ['r', 'r', 'w']]
test_b = [['o', 'r', 'b'], ['r', 'b', 'r'], ['g', 'b', 'o']]
test_r = [['w', 'o', 'r'], ['g', 'r', 'y'], ['y', 'w', 'y']]
test_o = [['w', 'g', 'g'], ['w', 'o', 'y'], ['g', 'b', 'r']]

def get_mixed_cube():
    '''
    Returns a mixed up rubik's cube
    '''
    c = Cube()

    c.color_dict['w'] = [['w', 'o', 'b'], ['y', 'w', 'b'], ['o', 'w', 'b']]
    c.color_dict['y'] = [['b', 'g', 'y'], ['y', 'y', 'w'], ['y', 'b', 'r']]
    c.color_dict['g'] = [['g', 'o', 'o'], ['o', 'g', 'g'], ['r', 'r', 'w']]
    c.color_dict['b'] = [['o', 'r', 'b'], ['r', 'b', 'r'], ['g', 'b', 'o']]
    c.color_dict['r'] = [['w', 'o', 'r'], ['g', 'r', 'y'], ['y', 'w', 'y']]
    c.color_dict['o'] = [['w', 'g', 'g'], ['w', 'o', 'y'], ['g', 'b', 'r']]

    return c


def test_print_v2():
    c = Cube()
    # solved state
    print(c.print_v2())

    c = get_mixed_cube()

    # new state
    print(c.print_v2())


def test_reorient(move):
    c = get_mixed_cube()

    # print original state
    print(c.print_v2())

    if move == 'right':
        # rotate right one face
        c.reorient(c.orient_dict[up], c.orient_dict[left], c.orient_dict[back])

        # print new state
        print(c.print_v2())
    elif move == 'left':
        # rotate left one face
        c.reorient(c.orient_dict[up], c.orient_dict[right], c.orient_dict[front])

        # print new state
        print(c.print_v2())
    elif move == 'up':
        # rotate up one face
        c.reorient(c.orient_dict[front], c.orient_dict[down], c.orient_dict[left])

        # print new state
        print(c.print_v2())
    elif move == 'down':
        # rotate down one face
        c.reorient(c.orient_dict[back], c.orient_dict[up], c.orient_dict[left])

        # print new state
        print(c.print_v2())

def test_face_rotate(clockwise):
    c = get_mixed_cube()

    # print original state
    print(c.print_v2())

    # rotate face
    c.face_rotate(b, clockwise)

    # print new state
    print(c.print_v2())

def test_cube_rot_left():
    c = get_mixed_cube()

    # print original state 
    print(c.print_v2())

    # rotate left
    c.cube_rot_left()

    # print new state
    print(c.print_v2())

def test_cube_rot_right():
    c = get_mixed_cube()

    # print original state 
    print(c.print_v2())

    # rotate left
    c.cube_rot_right()

    # print new state
    print(c.print_v2())

def test_cube_rot_up():
    c = get_mixed_cube()

    # print original state 
    print(c.print_v2())

    # rotate up
    c.cube_rot_up()

    # print new state
    print(c.print_v2())

def test_cube_rot_down():
    c = get_mixed_cube()

    # print original state 
    print(c.print_v2())

    # rotate down
    c.cube_rot_down()

    # print new state
    print(c.print_v2())

if __name__ == "__main__":
    #test_reorient('down')
    test_cube_rot_down()