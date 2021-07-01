from model import Cube
from constants import *
from utils import *


class Solver:
    def __init__(self, cube):
        self.cube = cube

    def solve(self):
        """
            Solves cube and returns solve sequence steps.
        """
        self.solve_daisy()
        self.solve_white_cross()
        self.solve_white_corners()
        self.solve_middle_layer()
        self.solve_yellow_cross()
        self.solve_yellow_corners()
        self.solve_position_yellow_corners()
        self.solve_final_stage()

        return self.cube.actions

    def solve_daisy(self):
        """
            Solves the daisy portion of the cube and outputs steps taken to solve
        """
        # search face
        while not self.check_daisy():
            print("daisy")
            if self.cube[UP, 2, 1] == WHITE:
                self.cube.apply(UP)
            elif self.cube[FRONT, 0, 1] == WHITE:
                self.cube.apply_seq([Y_ROT, RIGHT_PRIME, UP, FRONT_PRIME])
            elif self.cube[FRONT, 1, 0] == WHITE or self.cube[FRONT, 1, 2] == WHITE:
                self.cube.apply(FRONT)
            elif self.cube[FRONT, 2, 1] == WHITE or self.cube[DOWN, 0, 1] == WHITE:
                self.cube.apply_seq([FRONT, FRONT])
            else:
                self.cube.apply(Y_ROT_PRIME)

    def check_daisy(self):
        """
            Returns True if daisy is solved
        """
        return self.cube[YELLOW, 0, 1] == WHITE and self.cube[YELLOW, 1, 0] == WHITE and self.cube[YELLOW, 1, 2] == WHITE and self.cube[YELLOW, 2, 1] == WHITE

    def solve_white_cross(self):
        for _ in range(4):
            while self.cube[FRONT, 0, 1] != self.cube[FRONT, 1, 1] or self.cube[UP, 2, 1] != WHITE:
                self.cube.apply(UP)
            self.cube.apply_seq([FRONT, FRONT, Y_ROT_PRIME])

    def check_white_cross(self):

        white_cross = self.cube[WHITE, 0, 1] == WHITE and self.cube[WHITE, 1, 0] == WHITE and self.cube[WHITE, 1, 2] == WHITE and self.cube[WHITE, 2, 1] == WHITE

        centers_matched = self.cube[GREEN, 2, 1] == GREEN and self.cube[RED, 2, 1] == RED and self.cube[ORANGE, 2, 1] == ORANGE and self.cube[BLUE, 2, 1] == BLUE

        return white_cross and centers_matched

    def solve_white_corners(self):
        def move_corner_in_between():
            # corner is in bottom layer, so we need to rotate down until it is in between
            # its two corresponding centers
            front_color = None

            if self.cube[FRONT, 2, 2] == WHITE:
                front_color = self.cube[DOWN, 0, 2]
            if self.cube[RIGHT, 2, 0] == WHITE:
                front_color = self.cube[FRONT, 2, 2]
            if self.cube[DOWN, 0, 2] == WHITE:
                front_color = self.cube[RIGHT, 2, 0]

            while self.cube[FRONT, 1, 1] != front_color:
                self.cube.apply_seq([DOWN, Y_ROT_PRIME])

        def bring_corner_up():
            # corner piece must be in bottom right corner of front face, so we can bring it up
            if self.cube[FRONT, 2, 2] == WHITE:
                self.cube.apply_seq([DOWN_PRIME, RIGHT_PRIME, DOWN, RIGHT])
            elif self.cube[RIGHT, 2, 0] == WHITE:
                self.cube.apply_seq([Y_ROT_PRIME, DOWN, LEFT, DOWN_PRIME, LEFT_PRIME, Y_ROT])
            elif self.cube[DOWN, 0, 2] == WHITE:
                self.cube.apply_seq([FRONT, DOWN_PRIME, FRONT_PRIME, DOWN, DOWN])
                bring_corner_up()

        # rotate face up twice so that white cross is on up face
        self.cube.apply_seq([X_ROT, X_ROT])

        # for each corner
        while not self.check_white_corners():
            right_corner = self.cube[UP, 2, 2] == WHITE and self.cube[FRONT, 0, 2] == self.cube[FRONT, 1, 1] \
                and self.cube[RIGHT, 0, 0] == self.cube[RIGHT, 1, 1] 

            if self.cube[UP, 2, 2] == WHITE or self.cube[FRONT, 0, 2] == WHITE or self.cube[RIGHT, 0, 0] == WHITE:
                if not right_corner:
                    # bring her down into bottom right corner
                    self.cube.apply_seq([RIGHT_PRIME, DOWN_PRIME, RIGHT, DOWN])
                    move_corner_in_between()
                    bring_corner_up()
            else:
                # check bottom layer
                for _ in range(4):
                    if self.cube[FRONT, 2, 2] == WHITE or self.cube[RIGHT, 2, 0] == WHITE or self.cube[DOWN, 0, 2] == WHITE:
                        # found a corner
                        # get it in between the proper center pieces
                        move_corner_in_between()
                        bring_corner_up()
                    else:
                        self.cube.apply(DOWN)
            self.cube.apply(Y_ROT_PRIME)

    def check_white_corners(self):
        """
        Checks if step 3 is complete assuming orientation, white top, yellow bottom
        """

        white_row_one = self.cube[WHITE, 0, 0] == WHITE and self.cube[WHITE, 0, 1] == WHITE and self.cube[WHITE, 0, 2] == WHITE

        white_row_two = self.cube[WHITE, 1, 0] == WHITE and self.cube[WHITE, 1, 1] == WHITE and self.cube[WHITE, 1, 2] == WHITE

        white_row_three = self.cube[WHITE, 2, 0] == WHITE and self.cube[WHITE, 2, 1] == WHITE and self.cube[WHITE, 2, 2] == WHITE

        white_solved = white_row_one and white_row_two and white_row_three

        colors = [ORANGE, GREEN, BLUE, RED]
        solved = []

        for c in colors:
            current_solved = self.cube[c, 0, 0] == c and self.cube[c, 0, 1] == c and self.cube[c, 0, 2] == c and self.cube[c, 1, 1] == c
            solved.append(current_solved)
        return sum(solved) == len(solved) and white_solved

    def get_faces(self):
            return self.cube[FRONT], self.cube[UP], self.cube[RIGHT], self.cube[LEFT], self.cube[DOWN]
            
    def solve_middle_layer(self):
        #FIXME
        """
        1. check for top edge piece that does not have yellow side
            - make piece be on front face
            - make located piece go to correct location by doing up and rotate left enough times
            - when in correct position, move piece down
        2. if no top edge piece is valid
            - check for middle edge piece with no yellow side
        """
        def get_valid_piece():
            top_edge_loc = [(2, 1), (1, 2), (0, 1), (1, 0)]
            faces_to_search = [FRONT, RIGHT, BACK, LEFT]
            valid_piece = None
            i = 0
            # attempts to find valid top layer edge piece
            while valid_piece is None and i < 4:
                # if both top and front faces are not yellow, then valid
                if self.cube[faces_to_search[i], 0, 1] != YELLOW and self.cube[UP, top_edge_loc[i][0], top_edge_loc[i][1]] != YELLOW:
                    valid_piece = i
                    break
                i += 1

            return valid_piece

        # make white face down and yellow up
        self.cube.apply_seq([X_ROT, X_ROT])

        def make_front_face(valid):
            # make piece be on front face
            seq = []
            for _ in range(valid):
                seq.append(Y_ROT_PRIME)
            return seq

        def get_not_exists_sequence():
            # valid piece exists on right side of front face
            if self.cube[FRONT, 1, 2] != YELLOW and self.cube[RIGHT, 1, 0] != YELLOW:
                return [
                    UP, RIGHT, UP_PRIME, RIGHT_PRIME, UP_PRIME, FRONT_PRIME,
                    UP, FRONT
                ]
            if self.cube[FRONT, 1, 0] != YELLOW and self.cube[LEFT, 1, 2] != YELLOW:
                return [
                    Y_ROT, UP, RIGHT, UP_PRIME, RIGHT_PRIME, UP_PRIME,
                    FRONT_PRIME, UP, FRONT
                ]
            if self.cube[LEFT, 1, 0] != YELLOW and self.cube[BACK, 1, 2] != YELLOW:
                return [
                    Y_ROT, Y_ROT, UP, RIGHT, UP_PRIME, RIGHT_PRIME, UP_PRIME,
                    FRONT_PRIME, UP, FRONT
                ]
            if self.cube[RIGHT, 1, 2] != YELLOW and self.cube[BACK, 1, 0] != YELLOW:
                return [
                    Y_ROT_PRIME, UP, RIGHT, UP_PRIME, RIGHT_PRIME, UP_PRIME,
                    FRONT_PRIME, UP, FRONT
                ]

        while not self.check_middle_layer():
            #front_face, top_face, right_face, left_face, _ = self.get_faces()
            # back_face = self.cube.get_face_from_orient(BACK)

            # get valid piece
            valid_piece = get_valid_piece()

            # piece exists
            if valid_piece is not None:
                # move valid piece to front face
                self.cube.apply_seq(make_front_face(valid_piece))

                # make piece go to correct location
                while self.cube[FRONT, 0, 1] != self.cube[FRONT, 1, 1]:
                    self.cube.apply_seq([UP_PRIME, Y_ROT_PRIME])



                # move piece down right
                if self.cube[UP, 2, 1] == self.cube[RIGHT, 1, 1]:
                    self.cube.apply_seq(
                        [
                            UP, RIGHT, UP_PRIME, RIGHT_PRIME, UP_PRIME,
                            FRONT_PRIME, UP, FRONT
                        ])
                # move piece down left
                else:
                    self.cube.apply_seq(
                        [
                            UP_PRIME, LEFT_PRIME, UP, LEFT, UP, FRONT,
                            UP_PRIME, FRONT_PRIME
                        ])

            # piece does not exist
            else:
                # apply sequence for this case
                self.cube.apply_seq(
                    get_not_exists_sequence())


    def check_middle_layer(self):
        """
        Assuming yellow on top white on bottom, check if middle layer is complete
        """

        white_complete = True

        for i in range(3):
            for j in range(3):
                if self.cube[DOWN, i, j] != WHITE:
                    white_complete = False

        other_faces = [FRONT, RIGHT, LEFT, BACK]

        other_solved = True

        for face in other_faces:
            current_color = self.cube[face, 1, 1]
            for i in range(1, 3):
                for j in range(3):
                    if self.cube[face, i, j] != current_color:
                        other_solved = False

        return white_complete and other_solved

    def solve_yellow_cross(self):

        while not self.check_yellow_cross():

            top_edge = self.cube[YELLOW, 0, 1] == YELLOW
            right_edge = self.cube[YELLOW, 1, 2] == YELLOW
            left_edge = self.cube[YELLOW, 1, 0] == YELLOW
            bottom_edge = self.cube[YELLOW, 2, 1] == YELLOW

            if (top_edge and bottom_edge) or (left_edge and bottom_edge):
                self.cube.apply(UP)
            elif top_edge and right_edge:
                self.cube.apply(UP_PRIME)
            elif right_edge and bottom_edge:
                self.cube.apply_seq([UP_PRIME, UP_PRIME])

            self.cube.apply_seq(
                [FRONT, UP, RIGHT, UP_PRIME, RIGHT_PRIME, FRONT_PRIME])

    def check_yellow_cross(self):
        top_edge = self.cube[YELLOW, 0, 1] == YELLOW
        right_edge = self.cube[YELLOW, 1, 2] == YELLOW
        left_edge = self.cube[YELLOW, 1, 0] == YELLOW
        bottom_edge = self.cube[YELLOW, 2, 1] == YELLOW
        return top_edge and right_edge and left_edge and bottom_edge

    def solve_yellow_corners(self):

        while not self.check_yellow_corners():
            top_left = self.cube[YELLOW, 0, 0] == YELLOW
            top_right = self.cube[YELLOW, 0, 2] == YELLOW
            bottom_left = self.cube[YELLOW, 2, 0] == YELLOW
            bottom_right = self.cube[YELLOW, 2, 2] == YELLOW

            yellow_count = top_right + top_left + bottom_right + bottom_left
            if yellow_count == 0:
                # while not self.cube.get_face_from_orient(LEFT)[0][2] == YELLOW:
                while not self.cube[LEFT, 0, 2] == YELLOW:
                    self.cube.apply(UP)
            if yellow_count == 1:
                if top_left:
                    self.cube.apply(UP_PRIME)
                if top_right:
                    self.cube.apply_seq([UP, UP])
                if bottom_right:
                    self.cube.apply(UP)
            if yellow_count == 2:
                while not self.cube[FRONT, 0, 0] == YELLOW:
                    self.cube.apply(UP)

            self.cube.apply_seq(
                [RIGHT, UP, RIGHT_PRIME, UP, RIGHT, UP, UP, RIGHT_PRIME])

    def check_yellow_corners(self):

        top_left = self.cube[YELLOW, 0, 0] == YELLOW
        top_right = self.cube[YELLOW, 0, 2] == YELLOW
        bottom_left = self.cube[YELLOW, 2, 0] == YELLOW
        bottom_right = self.cube[YELLOW, 2, 2] == YELLOW
        return top_left and top_right and bottom_left and bottom_right

    def solve_position_yellow_corners(self):
        seq = [
            RIGHT_PRIME, FRONT, RIGHT_PRIME, BACK, BACK, RIGHT, FRONT_PRIME,
            RIGHT_PRIME, BACK, BACK, RIGHT, RIGHT, UP_PRIME
        ]

        while not self.check_position_yellow_corners():
            back_color = None
            for _ in range(4):
                if self.cube[FRONT, 0, 0] == self.cube[FRONT, 0, 2]:
                    back_color = self.cube[FRONT, 0, 0]
                else:
                    self.cube.apply(UP)

            for _ in range(4):
                if self.cube[BACK, 1, 1] != back_color:
                    self.cube.apply(Y_ROT_PRIME)

            for _ in range(4):
                if not (self.cube[BACK, 0, 0] == self.cube[BACK, 0, 2]
                        and self.cube[BACK, 0, 0] == back_color):
                    self.cube.apply(UP)
            self.cube.apply_seq(seq)

    def check_position_yellow_corners(self):

        blue_red_corner = (
            (self.cube[BLUE, 0, 2] == BLUE) and (self.cube[RED, 0, 0] == RED))
        blue_orange_corner = (
            (self.cube[BLUE, 0, 0] == BLUE)
            and (self.cube[ORANGE, 0, 2] == ORANGE))
        green_orange_corner = (
            (self.cube[GREEN, 0, 2] == GREEN)
            and (self.cube[ORANGE, 0, 0] == ORANGE))
        green_red_corner = (
            (self.cube[GREEN, 0, 0] == GREEN)
            and (self.cube[RED, 0, 2] == RED))

        return blue_red_corner and blue_orange_corner and green_orange_corner and green_red_corner

    def solve_final_stage(self):

        for _ in range(3):
            if self.check_final_step():
                break
            solved_color = None
            for color in [ORANGE, GREEN, RED, BLUE]:
                # face = self.cube.get_face_from_color(color)
                center = self.cube[color, 1, 1]
                if ((self.cube[color, 0, 0] == center)
                        and (self.cube[color, 0, 1] == center)
                        and (self.cube[color, 0, 2] == center)):
                    solved_color = center
                else:
                    self.cube.apply(Y_ROT_PRIME)

            if solved_color is not None:
                for _ in range(4):
                    if self.cube[BACK, 1, 1] != solved_color:
                        self.cube.apply(Y_ROT_PRIME)

            if self.cube[FRONT, 0, 1] == self.cube[FRONT, 1, 1]:
                self.cube.apply_seq(
                    [
                        FRONT, FRONT, UP_PRIME, LEFT, RIGHT_PRIME, FRONT,
                        FRONT, LEFT_PRIME, RIGHT, UP_PRIME, FRONT, FRONT
                    ])
            else:
                self.cube.apply_seq(
                    [
                        FRONT, FRONT, UP, LEFT, RIGHT_PRIME, FRONT, FRONT,
                        LEFT_PRIME, RIGHT, UP, FRONT, FRONT
                    ])

    def check_final_step(self):
        return is_solved(self.cube)
