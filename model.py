from utils import *
'''
    Cube Definition:

        A color is one of {YELLOW, WHITE, BLUE, GREEN, RED, ORANGE}

        An orientation is one of {UP, DOWN, LEFT, RIGHT, FRONT, BACK}

        A twist is one of {UP, DOWN, LEFT, RIGHT, FRONT, BACK, UP_PRIME, DOWN_PRIME, 
                            LEFT_PRIME, RIGHT_PRIME, FRONT_PRIME, BACK_PRIME}

        A rotation is one of {X_ROT, Y_ROT, Z_ROT, XPRIME, YPRIME, ZPRIME}

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
    def __init__(self, *args, **kwargs):
        """
            Initializes a solved cube with orientation yellow up and blue front.
        """
        self._orient_dict = kwargs.get(
            "orient_dict", {
                UP: YELLOW,
                DOWN: WHITE,
                FRONT: BLUE,
                BACK: GREEN,
                LEFT: ORANGE,
                RIGHT: RED
            })

        self._color_dict = kwargs.get(
            "color_dict", {
                YELLOW: face_init(YELLOW),
                WHITE: face_init(WHITE),
                GREEN: face_init(GREEN),
                BLUE: face_init(BLUE),
                RED: face_init(RED),
                ORANGE: face_init(ORANGE)
            })
        self.actions = []

    def print_orient_dict(self):
        print(f'orient dict: {self._orient_dict}')

    def print_color_dict(self):
        print(f'color dict {self._color_dict}')

    def set_state(self, data):
        self._color_dict[YELLOW] = data["Up Face"]
        self._color_dict[DOWN] = data["Down Face"]
        self._color_dict[LEFT] = data["Left Face"]
        self._color_dict[RIGHT] = data["Right Face"]
        self._color_dict[BACK] = data["Back Face"]
        self._color_dict[FRONT] = data["Front Face"]

    def __str__(self):
        """
        Returns current state of rubik's cube as a string.
        """
        up_face = self[UP]
        down_face = self[DOWN]
        left_face = self[LEFT]
        right_face = self[RIGHT]
        back_face = self[BACK]
        front_face = self[FRONT]

        key = {1: "y", 2: "w", 4: "r", 8: "o", 16: "g", 32: "b"}
        out = ""

        # prints up
        for i in range(3):
            out += "         " + key[up_face[i][0]] + "  " + key[up_face[i][
                1]] + "  " + key[up_face[i][2]] + "            " + "\n"

        # prints middle section
        for i in range(3):
            out += key[left_face[i][0]] + "  " + key[left_face[i][1]] + "  " + key[left_face[
                i][2]] + "  "
            out += key[front_face[i][0]] + "  " + key[front_face[i][
                1]] + "  " + key[front_face[i][2]] + "  "
            out += key[right_face[i][0]] + "  " + key[right_face[i][
                1]] + "  " + key[right_face[i][2]] + "  "
            out += key[back_face[i][0]] + "  " + key[back_face[i][1]] + "  " + key[back_face[
                i][2]] + "  " + "\n"

        # prints bottom section
        for i in range(3):
            out += "         " + key[down_face[i][0]] + "  " + key[down_face[i][
                1]] + "  " + key[down_face[i][2]] + "            " + "\n"

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
            for orient in list(self._orient_dict.keys()):
                #determines if two cubes have faces in the same orientation
                equal = equal and (self._orient_dict[orient] == other._orient_dict[orient])
                # equal = equal and (
                #     self.get_color_from_orient(orient)
                #     == other.get_color_from_orient(orient))

            if equal:
                #now check the actual contents of each face which need to match for the cubes to be equal
                for color, face in self._color_dict.items():
                    other_face = other._color_dict[color]
                    # other_face = other.get_face_from_color(color)
                    face_equal = True
                    for i in range(3):
                        for j in range(3):
                            face_equal = face_equal and (
                                face[i][j] == other_face[i][j])
                    equal = equal and face_equal
            return equal

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        s = ''.join(self.__str__().split())
        return hash(s)

    def _reorient(self, up_face, front_face, left_face):
        ''' reorient the cube by assigning the given up, front, and left colors to self.orient_dict. 
        The other faces are determined from the given face colors.
        '''
        back_face = OPPOSITE[front_face]
        down_face = OPPOSITE[up_face]
        right_face = OPPOSITE[left_face]

        self._orient_dict[UP] = up_face
        self._orient_dict[DOWN] = down_face
        self._orient_dict[FRONT] = front_face
        self._orient_dict[BACK] = back_face
        self._orient_dict[LEFT] = left_face
        self._orient_dict[RIGHT] = right_face

    def _face_rotate(self, color, clockwise, k=1):
        ''' rotates a face 90 degrees clockwise or counterclockwise
        '''
        for _ in range(k):
            new_top = []
            new_middle = []
            new_bottom = []

            # clockwise rotation
            if clockwise:
                for row in self._color_dict[color]:
                    new_top.append(row[0])
                    new_middle.append(row[1])
                    new_bottom.append(row[2])

                new_top.reverse()
                new_middle.reverse()
                new_bottom.reverse()
            else:
                for row in self._color_dict[color]:
                    new_bottom.append(row[0])
                    new_middle.append(row[1])
                    new_top.append(row[2])

            self._color_dict[color] = [new_top, new_middle, new_bottom]

    def __getitem__(self, index):
        face = None
        row = None
        col = None
        if type(index) is not tuple:
            try:
                return self._color_dict[index]
            except KeyError:
                return self._color_dict[self._orient_dict[index]]
        elif len(index) == 2:
            face = index[0]
            row, col = index[1]
        else:
            face, row, col = index
    
        try:
            return self._color_dict[face][row][col]
        except KeyError:
            return self._color_dict[self._orient_dict[face]][row][col]
        
    #FIXME
    def Z(self, prime):
        pass
        # if prime:
        #     #-->
        #     self.Y(False)
        #     self.X(False)
        #     self.Y(True)
        # else:
        #     # self.Y(True)
        #     # self.X(False)
        #     self.Y(True)
        #     self.X(False)

    def Y(self, prime):
        """
            Rotates entire cube about the Y axis.
        """
        if prime:
            #ll
            # reorient sides
            self._reorient(
                self._orient_dict[UP], self._orient_dict[RIGHT],
                self._orient_dict[FRONT])
            # rotate top clockwise
            self._face_rotate(self._orient_dict[UP], True)
            # rotate bottom counterclockwise
            self._face_rotate(self._orient_dict[DOWN], False)
        else:
            #rr
            # reorient sides
            self._reorient(
                self._orient_dict[UP], self._orient_dict[LEFT],
                self._orient_dict[BACK])
            # rotate top counterclockwise
            self._face_rotate(self._orient_dict[UP], False)
            # rotate down clockwise
            self._face_rotate(self._orient_dict[DOWN], True)

    def X(self, prime):
        """
            Rotates entire cube about the X axis.
        """
        if prime:
            #down
            # reorient sides
            self._reorient(
                self._orient_dict[BACK], self._orient_dict[UP],
                self._orient_dict[LEFT])
            # rotate left clockwise
            self._face_rotate(self._orient_dict[LEFT], True)
            # rotate right counterclockwise
            self._face_rotate(self._orient_dict[RIGHT], False)
            # rotate up clockwise twice (180 degrees)
            self._face_rotate(self._orient_dict[UP], True, k=2)
            # rotate back clockwise twice (180 degrees)
            self._face_rotate(self._orient_dict[BACK], True, k=2)
        else:
            #up
            # reorient sides
            self._reorient(
                self._orient_dict[FRONT], self._orient_dict[DOWN],
                self._orient_dict[LEFT])
            # rotate left counterclockwise
            self._face_rotate(self._orient_dict[LEFT], False)
            # rotate right clockwise
            self._face_rotate(self._orient_dict[RIGHT], True)
            # rotate down clockwise twice (180 degrees)
            self._face_rotate(self._orient_dict[DOWN], True, k=2)
            # rotate back clockwise twice (180 degrees)
            self._face_rotate(self._orient_dict[BACK], True, k=2)

    def U(self, prime):
        """
            Rotates the top layer
        """
        top_front = self._color_dict[self._orient_dict[FRONT]][0]
        top_left = self._color_dict[self._orient_dict[LEFT]][0]
        top_back = self._color_dict[self._orient_dict[BACK]][0]
        top_right = self._color_dict[self._orient_dict[RIGHT]][0]

        if prime:
            self._color_dict[self._orient_dict[FRONT]][0] = top_left
            self._color_dict[self._orient_dict[LEFT]][0] = top_back
            self._color_dict[self._orient_dict[BACK]][0] = top_right
            self._color_dict[self._orient_dict[RIGHT]][0] = top_front
            self._face_rotate(self._orient_dict[UP], False)
        else:
            self._color_dict[self._orient_dict[FRONT]][0] = top_right
            self._color_dict[self._orient_dict[LEFT]][0] = top_front
            self._color_dict[self._orient_dict[BACK]][0] = top_left
            self._color_dict[self._orient_dict[RIGHT]][0] = top_back
            self._face_rotate(self._orient_dict[UP], True)

    def D(self, prime):
        """
            Rotates the bottom face
        """
        self.X(False)
        self.X(False)
        self.U(prime)
        self.X(True)
        self.X(True)

    def L(self, prime):
        """
            Rotates the left face
        """
        self.Y(False)
        self.X(False)
        self.U(prime)
        self.X(True)
        self.Y(True)

    def R(self, prime):
        """
            Rotates the right face
        """
        self.Y(True)
        self.X(False)
        self.U(prime)
        self.X(True)
        self.Y(False)

    def F(self, prime):
        """
            Rotates the front face
        """
        self.X(False)
        self.U(prime)
        self.X(True)

    def B(self, prime):
        """
            Rotates the back face
        """
        self.X(True)
        self.U(prime)
        self.X(False)

    def apply(self, action):
        """
            Applies the specified action to the cube and appends to action list field.
        """
        if action == LEFT:
            self.L(False)
        elif action == LEFT_PRIME:
            self.L(True)
        elif action == RIGHT:
            self.R(False)
        elif action == RIGHT_PRIME:
            self.R(True)
        elif action == FRONT:
            self.F(False)
        elif action == FRONT_PRIME:
            self.F(True)
        elif action == BACK:
            self.B(False)
        elif action == BACK_PRIME:
            self.B(True)
        elif action == UP:
            self.U(False)
        elif action == UP_PRIME:
            self.U(True)
        elif action == DOWN:
            self.D(False)
        elif action == DOWN_PRIME:
            self.D(True)
        elif action == Y_ROT_PRIME:
            self.Y(True)
        elif action == Y_ROT:
            self.Y(False)
        elif action == X_ROT_PRIME:
            self.X(True)
        elif action == X_ROT:
            self.X(False)
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
        self.apply(INVERSE[self.actions[-1:]])

    # def get_face_from_color(self, color):
    #     for key in self._color_dict.keys():
    #         if self._color_dict[key] == color:
    #             return key

    # def get_face_from_orient(self, orient):
    #     return self._color_dict[self._orient_dict[orient]]

