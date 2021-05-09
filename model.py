from constants import *
from utils import *

'''
Represents data structure for cube with dictionary containing orientation based on color. Orientation dict has 
keys of up, down, front, back, left, and right and values of the corresponding colors for the sides. Contains 
dictionary containing cube arrays with color as keys and array as values.
'''
class Cube:    
    def __init__(self):
        self.__orient_dict = {UP:y, DOWN:w, FRONT:b, BACK:g, LEFT:o, RIGHT:r}
        self.__color_dict = {y:fill(3,y),w:fill(3,w),g:fill(3,g), b:fill(3,b), r:fill(3,r), o:fill(3,o)}
        self.actions = []                    
    def __str__(self):
        '''
        Prints current state of rubik's cube
        ''' 
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
            out += "         " + down_face[i][0] + "  " + down_face[i][1] + "  " + down_face[i][2] + "            " + "\n"

        return out

    def __eq__(self, other):
        if not isinstance(other, Cube):
            return False
        else:
            equal = True
            for color, face in self.__color_dict.items():
                other_face = other.__color_dict[color]
                face_equal = True
                for i in range(3):
                    for j in range(3):
                        face_equal = face_equal and (face[i][j] == other_face[i][j])
                equal = equal and face_equal      
            return equal

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):

        color_map = {w: 163 ,y:113,g:151,b:173, r:193, o:239}
        # color_map = {w: 2 ,y:4,g:8,b:16, r:32, o:64}

        # h = 17

        # for x, face in enumerate(list(self.color_dict.values())):
            
        #     sub_hash = 7
        #     ctr = 1
        #     for i in range(3):
        #         for j in range(3):
        #             sub_hash += ((i+1) * (j+9) * color_map[face[i][j]])

        #             # print("sub: ", sub_hash)
        #             ctr+=1
        #     h *= ( (x+67) * sub_hash)
        #     # print("h: ", h)
        # # print("h: ", h)
        # return h\
        s = ''.join(self.__str__().split())
        # print(s)
        h = hash(s)
        # print(h)
        return h
    
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
    
    def __cube_rot_left(self):
        '''
        Rotates a rubik's cube left one face
        '''
        # reorient sides
        self.__reorient(self.__orient_dict[UP], self.__orient_dict[RIGHT], self.__orient_dict[FRONT])
        
        # rotate top clockwise
        self.__face_rotate(self.__orient_dict[UP], True)
        # rotate bottom counterclockwise
        self.__face_rotate(self.__orient_dict[DOWN], False)

    def __cube_rot_right(self):
        '''
        Rotates a rubik's cube right one face
        '''
        # reorient sides
        self.__reorient(self.__orient_dict[UP], self.__orient_dict[LEFT], self.__orient_dict[BACK])

        # rotate top counterclockwise
        self.__face_rotate(self.__orient_dict[UP], False)
        # rotate down clockwise
        self.__face_rotate(self.__orient_dict[DOWN], True)

    def __cube_rot_up(self):
        '''
        Rotates a rubik's cube up one face
        '''
        # reorient sides
        self.__reorient(self.__orient_dict[FRONT], self.__orient_dict[DOWN], self.__orient_dict[LEFT])

        # rotate left counterclockwise
        self.__face_rotate(self.__orient_dict[LEFT], False)
        # rotate right clockwise
        self.__face_rotate(self.__orient_dict[RIGHT], True)
        # rotate down clockwise twice (180 degrees)
        self.__face_rotate(self.__orient_dict[DOWN], True)
        self.__face_rotate(self.__orient_dict[DOWN], True)
        # rotate back clockwise twice (180 degrees)
        self.__face_rotate(self.__orient_dict[BACK], True)
        self.__face_rotate(self.__orient_dict[BACK], True)

    def __cube_rot_down(self):
        '''
        Rotates a rubik's cube down one face
        '''
        # reorient sides
        self.__reorient(self.__orient_dict[BACK], self.__orient_dict[UP], self.__orient_dict[LEFT])

        # rotate left clockwise
        self.__face_rotate(self.__orient_dict[LEFT], True)
        # rotate right counterclockwise
        self.__face_rotate(self.__orient_dict[RIGHT], False)
        # rotate up clockwise twice (180 degrees)
        self.__face_rotate(self.__orient_dict[UP], True)
        self.__face_rotate(self.__orient_dict[UP], True)
        # rotate back clockwise twice (180 degrees)
        self.__face_rotate(self.__orient_dict[BACK], True)
        self.__face_rotate(self.__orient_dict[BACK], True)
        
    def __face_rotate(self, color, clockwise):
        ''' rotates a face 90 degrees clockwise or counterclockwise
        '''
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
           
    def __rot_U(self, prime):
        top_front = self.__color_dict[self.__orient_dict[FRONT]][0].copy()
        top_left = self.__color_dict[self.__orient_dict[LEFT]][0].copy()
        top_back = self.__color_dict[self.__orient_dict[BACK]][0].copy()
        top_right = self.__color_dict[self.__orient_dict[RIGHT]][0].copy()
        
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
    
    def __rot_D(self, prime):
        self.__cube_rot_up()
        self.__cube_rot_up()
        self.__rot_U(prime)
        self.__cube_rot_down()
        self.__cube_rot_down()

    def __rot_L(self, prime):
        self.__cube_rot_right()
        self.__cube_rot_up()
        self.__rot_U(prime)
        self.__cube_rot_down()
        self.__cube_rot_left()
        
    def __rot_R(self, prime):
        self.__cube_rot_left()
        self.__cube_rot_up()
        self.__rot_U(prime)
        self.__cube_rot_down()
        self.__cube_rot_right()
        
    def __rot_F(self, prime):
        self.__cube_rot_up()
        self.__rot_U(prime)
        self.__cube_rot_down()
        
    def __rot_B(self, prime):
        self.__cube_rot_down()
        self.__rot_U(prime)
        self.__cube_rot_up()

    def __rotate(self, direction, prime):
        if direction == UP:
            self.__rot_U(prime)
        if direction == DOWN:
            self.__rot_D(prime)
        if direction == LEFT:
            self.__rot_L(prime)
        if direction == RIGHT:
            self.__rot_R(prime)
        if direction == FRONT:
            self.__rot_F(prime)
        if direction == BACK:
            self.__rot_B(prime)

    def __apply(self, action):
        self.actions.append(action)
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
        elif action == CUBE_ROT_LEFT:
            self.__cube_rot_left()
        elif action == CUBE_ROT_RIGHT:
            self.__cube_rot_right()
        elif action == CUBE_ROT_DOWN:
            self.__cube_rot_down()
        elif action == CUBE_ROT_UP:
            self.__cube_rot_up()
        else:
            raise Error

    def get_face_from_color(self, color):
        return self.__color_dict[color]

    def get_color_from_orient(self, orient):
        return self.__orient_dict[orient] 

    def get_face_from_orient(self, orient):
        return self.__color_dict[self.__orient_dict[orient]]

    def apply_seq(self, seq):
        for action in seq:
            self.__apply(action)

    def undo(self):
        assert len(self.actions) > 0
        self.__apply(get_inverse(self.actions[-1:]))