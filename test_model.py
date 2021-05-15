from constants import *
from utils import *
from solver import Solver
from model import Cube

test_w = [['b', 'o', 'r'], ['r', 'w', 'w'], ['g', 'y', 'y']]
test_y = [['w', 'y', 'b'], ['o', 'y', 'b'], ['r', 'r', 'r']]
tets_g = [['o', 'o', 'g'], ['y', 'g', 'w'], ['g', 'r', 'o']]
test_b = [['w', 'g', 'y'], ['y', 'b', 'w'], ['o', 'g', 'y']]
test_r = [['b', 'r', 'y'], ['g', 'r', 'g'], ['g', 'b', 'o']]
test_o = [['r', 'b', 'b'], ['o', 'o', 'b'], ['w', 'w', 'w']]


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
        c.reorient(
            c.orient_dict[up], c.orient_dict[right], c.orient_dict[front])

        # print new state
        print(c.print_v2())
    elif move == 'up':
        # rotate up one face
        c.reorient(
            c.orient_dict[front], c.orient_dict[down], c.orient_dict[left])

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


def test_rotate(direction, prime):
    c = get_mixed_cube()

    # print original state
    print(c.print_v2())

    # rotate down
    c.rotate(direction, prime)

    # print new state
    print(c.print_v2())


def test_get_orient_from_color():
    c = Cube()

    print(c)

    print(c.get_orient_from_color(WHITE))


def test_cube_rot():

    c = Cube()
    random_seq = get_random_seq()
    c.apply_seq(random_seq)
    print("Before")
    print(c)
    for i in range(4):
        print(i + 1)
        c.apply_seq([Y_ROT])
        print(c)
    print("After")
    print(c)
    z = Cube()
    z.apply_seq(random_seq)
    assert c == z
    # print("Right")
    # c.apply_seq([Y_ROT])
    # print(c)


if __name__ == "__main__":
    test_cube_rot()
