from utils import *

'''
    Represents data structure for cube with dictionary containing orientation based on color. Orientation dict has 
    keys of up, down, front, back, left, and right and values of the corresponding colors for the sides. Contains 
    dictionary containing cube arrays with color as keys and array as values.

    Data Definition:

        A color is one of {YELLOW, WHITE, BLUE, GREEN, RED, ORANGE}

        An orientation is one of {UP, DOWN, LEFT, RIGHT, FRONT, BACK}

        A twist is one of {UP, DOWN, LEFT, RIGHT, FRONT, BACK, UP_PRIME, DOWN_PRIME, 
                            LEFT_PRIME, RIGHT_PRIME, FRONT_PRIME, BACK_PRIME}

        A rotation is one of {X_ROT, Y_ROT, Z_ROT, X_ROT_PRIME, Y_ROT_PRIME, Z_ROT_PRIME}

        A face is a 3x3 array of colors and can be identified by a unique pair (color, orientation) pair.
            - the color identity of a face will NOT change, it is the center square at (1,1) 
            - the orientation identity of a face may change

        A cube is a collection of 6 faces (a unique bijective mapping of color<->orientation)
            - at any point in time, if you know the color of a face, then you can determine the spatial position
            of that face, and at any time, if you know the spatial position of a face, then you can determine the
            color of that face.
                - for example: both yellow and green cannot both be up at the same time and yellow cannot both be up
                    and down at the same time

        A cube can be mutated by twists and rotations
            - a twist will rotate a face clockwise or counterclockwise
            - a rotation will reorient the cube in space along a specified axis x, y, z

'''

class Cube:
    def __init__(self):
        """
            Initializes a solved cube with orientation yellow up and blue front.
        """
        self.__orient_dict = {UP: YELLOW, DOWN: WHITE, FRONT: BLUE, BACK: GREEN, LEFT: ORANGE, RIGHT: RED}
        self.__color_dict = {YELLOW: face_init(YELLOW), WHITE: face_init(WHITE), GREEN: face_init(GREEN),
                             BLUE: face_init(BLUE), RED: face_init(RED), ORANGE: face_init(ORANGE)}
        self.actions = []

    def set_state(self, data):
        self.__color_dict[self.__orient_dict[FRONT]] = data["Front Face"]
        self.__color_dict[self.__orient_dict[UP]] = data["Up Face"]
        self.__color_dict[self.__orient_dict[DOWN]] = data["Down Face"]
        self.__color_dict[self.__orient_dict[BACK]] = data["Back Face"]
        self.__color_dict[self.__orient_dict[LEFT]] = data["Left Face"]
        self.__color_dict[self.__orient_dict[RIGHT]] = data["Right Face"]


    def __str__(self):
        """
        Returns current state of rubik's cube as a string.
        """
        up_face = self.get_face_from_orient(UP)
        down_face = self.get_face_from_orient(DOWN)
        left_face = self.get_face_from_orient(LEFT)
        right_face = self.get_face_from_orient(RIGHT)
        back_face = self.get_face_from_orient(BACK)
        front_face = self.get_face_from_orient(FRONT)

        out = ""

        # prints up
        for i in range(3):
            out += "         " + up_face[i][0] + "  " + up_face[i][1] + "  " + up_face[i][2] + "            " + "\n"

        # prints middle section
        for i in range(3):
            out += left_face[i][0] + "  " + left_face[i][1] + "  " + left_face[i][2] + "  "
            out += front_face[i][0] + "  " + front_face[i][1] + "  " + front_face[i][2] + "  "
            out += right_face[i][0] + "  " + right_face[i][1] + "  " + right_face[i][2] + "  "
            out += back_face[i][0] + "  " + back_face[i][1] + "  " + back_face[i][2] + "  " + "\n"

        # prints bottom section
        for i in range(3):
            out += "         " + down_face[i][0] + "  " + down_face[i][1] + "  " + down_face[i][
                2] + "            " + "\n"

        return out

    def __eq__(self, other):
        """
            Determines if two cubes are equal. Two cubes are equal iff. they have the same 
            orientation and equal faces. Two faces are equal if they have the same color
            at each location in the 3x3 array.
        """
        if not isinstance(other, Cube):
            return False
        else:
            equal = True
            for orient in list(self.__orient_dict.keys()):
                #determines if two cubes have faces in the same orientation
                equal = equal and (self.get_color_from_orient(orient) == other.get_color_from_orient(orient))
            
            if equal:
                #now check the actual contents of each face which need to match for the cubes to be equal
                for color, face in self.__color_dict.items():
                    other_face = other.get_face_from_color(color)
                    face_equal = True
                    for i in range(3):
                        for j in range(3):
                            face_equal = face_equal and (face[i][j] == other_face[i][j])
                    equal = equal and face_equal
            return equal

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        s = ''.join(self.__str__().split())
        return hash(s)

    def __reorient(self, up_face, front_face, left_face):
        ''' reorient the cube by assigning the given up, front, and left colors to self.orient_dict. 
        The other faces are determined from the given face colors.
        '''
        back_face = get_opposite(front_face)
        down_face = get_opposite(up_face)
        right_face = get_opposite(left_face)

        self.__orient_dict[UP] = up_face
        self.__orient_dict[DOWN] = down_face
        self.__orient_dict[FRONT] = front_face
        self.__orient_dict[BACK] = back_face
        self.__orient_dict[LEFT] = left_face
        self.__orient_dict[RIGHT] = right_face

    def __face_rotate(self, color, clockwise, k=1):
        ''' rotates a face 90 degrees clockwise or counterclockwise
        '''
        for _ in range(k):   
            new_top = []
            new_middle = []
            new_bottom = []

            # clockwise rotation
            if clockwise:
                for row in self.__color_dict[color]:
                    new_top.append(row[0])
                    new_middle.append(row[1])
                    new_bottom.append(row[2])

                new_top.reverse()
                new_middle.reverse()
                new_bottom.reverse()
            else:
                for row in self.__color_dict[color]:
                    new_bottom.append(row[0])
                    new_middle.append(row[1])
                    new_top.append(row[2])

            self.__color_dict[color] = [new_top, new_middle, new_bottom]

    #TODO
    def __rot_Z(self, prime, k=1):

        for _ in range(k):
            if prime:
                #-->
                self.__rot_Y(False)
                self.__rot_X(False)
                self.__rot_Y(True)
            else:   
                # self.__rot_Y(True)
                # self.__rot_X(False)
                self.__rot_Y(True)
                self.__rot_X(False)

    def __rot_Y(self, prime, k=1):
        """
            Rotates entire cube about the Y axis.
        """
        for _ in range(k):
            if prime:
                #ll
                # reorient sides
                self.__reorient(self.__orient_dict[UP], self.__orient_dict[RIGHT], self.__orient_dict[FRONT])
                # rotate top clockwise
                self.__face_rotate(self.__orient_dict[UP], True)
                # rotate bottom counterclockwise
                self.__face_rotate(self.__orient_dict[DOWN], False)
            else:   
                #rr
                # reorient sides
                self.__reorient(self.__orient_dict[UP], self.__orient_dict[LEFT], self.__orient_dict[BACK])
                # rotate top counterclockwise
                self.__face_rotate(self.__orient_dict[UP], False)
                # rotate down clockwise
                self.__face_rotate(self.__orient_dict[DOWN], True)

    def __rot_X(self, prime, k=1):
        """
            Rotates entire cube about the X axis.
        """
        for _ in range(k):
            if prime:
                #down
                # reorient sides
                self.__reorient(self.__orient_dict[BACK], self.__orient_dict[UP], self.__orient_dict[LEFT])

                # rotate left clockwise
                self.__face_rotate(self.__orient_dict[LEFT], True)
                # rotate right counterclockwise
                self.__face_rotate(self.__orient_dict[RIGHT], False)
                # rotate up clockwise twice (180 degrees)
                self.__face_rotate(self.__orient_dict[UP], True, k = 2)
                # self.__face_rotate(self.__orient_dict[UP], True)
                # rotate back clockwise twice (180 degrees)
                self.__face_rotate(self.__orient_dict[BACK], True, k = 2)
                # self.__face_rotate(self.__orient_dict[BACK], True)
            else:
                #up
                # reorient sides
                self.__reorient(self.__orient_dict[FRONT], self.__orient_dict[DOWN], self.__orient_dict[LEFT])

                # rotate left counterclockwise
                self.__face_rotate(self.__orient_dict[LEFT], False)
                # rotate right clockwise
                self.__face_rotate(self.__orient_dict[RIGHT], True)
                # rotate down clockwise twice (180 degrees)
                self.__face_rotate(self.__orient_dict[DOWN], True, k = 2)
                # self.__face_rotate(self.__orient_dict[DOWN], True)
                # rotate back clockwise twice (180 degrees)
                self.__face_rotate(self.__orient_dict[BACK], True, k = 2)
                # self.__face_rotate(self.__orient_dict[BACK], True)

    def __rot_U(self, prime, k=1):
        """
            Rotates the top layer
        """
        for _ in range(k):
            top_front = self.__color_dict[self.__orient_dict[FRONT]][0]
            top_left = self.__color_dict[self.__orient_dict[LEFT]][0]
            top_back = self.__color_dict[self.__orient_dict[BACK]][0]
            top_right = self.__color_dict[self.__orient_dict[RIGHT]][0]

            if prime:
                self.__color_dict[self.__orient_dict[FRONT]][0] = top_left
                self.__color_dict[self.__orient_dict[LEFT]][0] = top_back
                self.__color_dict[self.__orient_dict[BACK]][0] = top_right
                self.__color_dict[self.__orient_dict[RIGHT]][0] = top_front
                self.__face_rotate(self.__orient_dict[UP], False)
            else:
                self.__color_dict[self.__orient_dict[FRONT]][0] = top_right
                self.__color_dict[self.__orient_dict[LEFT]][0] = top_front
                self.__color_dict[self.__orient_dict[BACK]][0] = top_left
                self.__color_dict[self.__orient_dict[RIGHT]][0] = top_back
                self.__face_rotate(self.__orient_dict[UP], True)

    def __rot_D(self, prime, k=1):
        """
            Rotates the bottom face
        """
        for _ in range(k):
            self.__rot_X(False, k = 2)
            self.__rot_U(prime)
            self.__rot_X(True, k = 2)

    def __rot_L(self, prime, k=1):
        """
            Rotates the left face
        """
        for _ in range(k):
            self.__rot_Y(False)
            self.__rot_X(False)
            # self.__rot_Z(False)
            self.__rot_U(prime)
            # self.__rot_Z(True)
            self.__rot_X(True)
            self.__rot_Y(True)

    def __rot_R(self, prime, k=1):
        """
            Rotates the right face
        """
        for _ in range(k):
            # self.__rot_Z(True)
            # self.__rot_U(prime)
            # self.__rot_Z(False)
            self.__rot_Y(True)
            self.__rot_X(False)
            self.__rot_U(prime)
            self.__rot_X(True)
            self.__rot_Y(False)

    def __rot_F(self, prime, k=1):
        """
            Rotates the front face
        """
        for _ in range(k):
            self.__rot_X(False)
            self.__rot_U(prime)
            self.__rot_X(True)

    def __rot_B(self, prime, k=1):
        """
            Rotates the back face
        """
        for _ in range(k):
            self.__rot_X(True)
            self.__rot_U(prime)
            self.__rot_X(False)

    def get_face_from_color(self, color):
        """
            Returns the 3x3 array face where the center square is of the specified color
        """
        return self.__color_dict[color]

    def get_color_from_orient(self, orient):
        """
            Returns the color of the specified face orientation. 
        """
        return self.__orient_dict[orient]

    def get_face_from_orient(self, orient):
        """
            Returns the face array of the specified face orientation.
        """
        return self.__color_dict[self.__orient_dict[orient]]

    def get_orient_from_color(self, c):
        """
            Returns the color of the face at the given orientation
        """
        for orient, color in self.__orient_dict.items():
            if color == c:
                return orient

    def apply(self, action):
        """
            Applies the specified action to the cube and appends to action list field.
        """
        if action == LEFT:
            self.__rot_L(False)
        elif action == LEFT_PRIME:
            self.__rot_L(True)
        elif action == RIGHT:
            self.__rot_R(False)
        elif action == RIGHT_PRIME:
            self.__rot_R(True)
        elif action == FRONT:
            self.__rot_F(False)
        elif action == FRONT_PRIME:
            self.__rot_F(True)
        elif action == BACK:
            self.__rot_B(False)
        elif action == BACK_PRIME:
            self.__rot_B(True)
        elif action == UP:
            self.__rot_U(False)
        elif action == UP_PRIME:
            self.__rot_U(True)
        elif action == DOWN:
            self.__rot_D(False)
        elif action == DOWN_PRIME:
            self.__rot_D(True)
        elif action == Y_ROT_PRIME:
            self.__rot_Y(True)
        elif action == Y_ROT:
            self.__rot_Y(False)
        elif action == X_ROT_PRIME:
            self.__rot_X(True)
        elif action == X_ROT:
            self.__rot_X(False)
        else:
            raise ValueError
        self.actions.append(action)

    def apply_seq(self, seq):
        """
            Applies the sequence of actions to the cube.
        """
        for action in seq:
            self.apply(action)

    def undo(self):
        """
            Undoes the most recent move. 
        """
        assert len(self.actions) > 0
        self.__apply(get_inverse(self.actions[-1:]))
