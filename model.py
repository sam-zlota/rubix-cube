from constants import up, down, left, right, front, back, y, w, r, o, g, b
from utils import get_opposite, fill

'''
Represents data structure for cube with dictionary containing orientation based on color. Orientation dict has 
keys of up, down, front, back, left, and right and values of the corresponding colors for the sides. Contains 
dictionary containing cube arrays with color as keys and array as values.
'''
class Cube:    
    def __init__(self):
        self.orient_dict = {up:y, down:w, front:b, back:g, left:o, right:r}
        self.color_dict = {y:fill(3,y),w:fill(3,w),g:fill(3,g), b:fill(3,b), r:fill(3,r), o:fill(3,o)}
      
    def print_out(self):
        for color in colors:
            face = self.color_dict[color]
            for i in range(3):
                print(face[i][0], face[i][1], face[i][2])
                            
    def print_v2(self):
        '''
        Prints current state of rubik's cube
        ''' 
        up_face = self.color_dict[self.orient_dict[up]]
        down_face = self.color_dict[self.orient_dict[down]]
        left_face = self.color_dict[self.orient_dict[left]]
        right_face = self.color_dict[self.orient_dict[right]]
        back_face = self.color_dict[self.orient_dict[back]]
        front_face = self.color_dict[self.orient_dict[front]]
        
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

    def reorient(self, up_face, front_face, left_face):
        ''' reorient the cube by assigning the given up, front, and left colors to self.orient_dict. 
        The other faces are determined from the given face colors.
        '''
       
        if self.orient_dict[up] == up_face and self.orient_dict[front] == front_face:
            return
        
        back_face = get_opposite(front_face)
        down_face = get_opposite(up_face)
        right_face = get_opposite(left_face)
        
        self.orient_dict[up] = up_face
        self.orient_dict[down] = down_face
        self.orient_dict[front] = front_face
        self.orient_dict[back] = back_face
        self.orient_dict[left] = left_face
        self.orient_dict[right] = right_face
    
    def cube_rot_left(self):
        '''
        Rotates a rubik's cube left one face
        '''
        # reorient sides
        self.reorient(self.orient_dict[up], self.orient_dict[right], self.orient_dict[front])
        
        # rotate top clockwise
        self.face_rotate(self.orient_dict[up], True)
        # rotate bottom counterclockwise
        self.face_rotate(self.orient_dict[down], False)


    def cube_rot_right(self):
        '''
        Rotates a rubik's cube right one face
        '''
        # reorient sides
        self.reorient(self.orient_dict[up], self.orient_dict[left], self.orient_dict[back])

        # rotate top counterclockwise
        self.face_rotate(self.orient_dict[up], False)
        # rotate down clockwise
        self.face_rotate(self.orient_dict[down], True)

        return 'rotate right'

    def cube_rot_up(self):
        '''
        Rotates a rubik's cube up one face
        '''
        # reorient sides
        self.reorient(self.orient_dict[front], self.orient_dict[down], self.orient_dict[left])

        # rotate left counterclockwise
        self.face_rotate(self.orient_dict[left], False)
        # rotate right clockwise
        self.face_rotate(self.orient_dict[right], True)
        # rotate down clockwise twice (180 degrees)
        self.face_rotate(self.orient_dict[down], True)
        self.face_rotate(self.orient_dict[down], True)
        # rotate back clockwise twice (180 degrees)
        self.face_rotate(self.orient_dict[back], True)
        self.face_rotate(self.orient_dict[back], True)

    def cube_rot_down(self):
        '''
        Rotates a rubik's cube down one face
        '''
        # reorient sides
        self.reorient(self.orient_dict[back], self.orient_dict[up], self.orient_dict[left])

        # rotate left clockwise
        self.face_rotate(self.orient_dict[left], True)
        # rotate right counterclockwise
        self.face_rotate(self.orient_dict[right], False)
        # rotate up clockwise twice (180 degrees)
        self.face_rotate(self.orient_dict[up], True)
        self.face_rotate(self.orient_dict[up], True)
        # rotate back clockwise twice (180 degrees)
        self.face_rotate(self.orient_dict[back], True)
        self.face_rotate(self.orient_dict[back], True)
        
    def face_rotate(self, color, clockwise):
        ''' rotates a face 90 degrees clockwise or counterclockwise
        '''
        new_top = []
        new_middle = []
        new_bottom = []

        # clockwise rotation
        if clockwise:
            for row in self.color_dict[color]:
                new_top.append(row[0])
                new_middle.append(row[1])
                new_bottom.append(row[2])

            new_top.reverse()
            new_middle.reverse()
            new_bottom.reverse()
        else:
            for row in self.color_dict[color]:
                new_bottom.append(row[0])
                new_middle.append(row[1])
                new_top.append(row[2])
                

        self.color_dict[color] = [new_top, new_middle, new_bottom]
           
    def rot_U(self, prime):
        top_front = self.color_dict[self.orient_dict[front]][0].copy()
        top_left = self.color_dict[self.orient_dict[left]][0].copy()
        top_back = self.color_dict[self.orient_dict[back]][0].copy()
        top_right = self.color_dict[self.orient_dict[right]][0].copy()
        
        if prime:        
            self.color_dict[self.orient_dict[front]][0] = top_left
            self.color_dict[self.orient_dict[left]][0] = top_back
            self.color_dict[self.orient_dict[back]][0] = top_right
            self.color_dict[self.orient_dict[right]][0] = top_front
            self.face_rotate(self.orient_dict[up], False)
        else:
            self.color_dict[self.orient_dict[front]][0] = top_right
            self.color_dict[self.orient_dict[left]][0] = top_front
            self.color_dict[self.orient_dict[back]][0] = top_left
            self.color_dict[self.orient_dict[right]][0] = top_back
            self.face_rotate(self.orient_dict[up], True)
    
    def rot_D(self, prime):
        self.cube_rot_up()
        self.cube_rot_up()
        self.rot_U(prime)
        self.cube_rot_down()
        self.cube_rot_down()

    def rot_L(self, prime):
        self.cube_rot_right()
        self.cube_rot_up()
        self.rot_U(prime)
        self.cube_rot_down()
        self.cube_rot_left()
        
    def rot_R(self, prime):
        self.cube_rot_left()
        self.cube_rot_up()
        self.rot_U(prime)
        self.cube_rot_down()
        self.cube_rot_right()
        
    def rot_F(self, prime):
        self.cube_rot_up()
        self.rot_U(prime)
        self.cube_rot_down()
        
    def rot_B(self, prime):
        self.cube_rot_down()
        self.rot_U(prime)
        self.cube_rot_up()

    def rotate(self, direction, prime):
        if direction == up:
            self.rot_U(prime)
            if prime:
                return "U'"
            else:
                return "U"
        if direction == down:
            self.rot_D(prime)
            if prime:
                return "D'"
            else:
                return "D"
        if direction == left:
            self.rot_L(prime)
            if prime:
                return "L'"
            else:
                return "L"
        if direction == right:
            self.rot_R(prime)
            if prime:
                return "R'"
            else:
                return "R"
        if direction == front:
            self.rot_F(prime)
            if prime:
                return "F'"
            else:
                return "F"
        if direction == back:
            self.rot_B(prime)
            if prime:
                return "B'"
            else:
                return "B"

    def apply(self, action):
        #legal moves
        if action == "U":
            self.rot_U(False)
        elif action == "U'":
            self.rot_U(True)
        elif action == "D":
            self.rot_D(False)
        elif action == "D'":
            self.rot_D(True)
        elif action == "L":
            self.rot_L(False)
        elif action == "L'":
            self.rot_L(True)
        elif action == "R":
            self.rot_R(False)
        elif action == "R'":
            self.rot_R(True)
        elif action == "F":
            self.rot_F(False)
        elif action == "F'":
            self.rot_F(True)
        elif action == "B":
            self.rot_B(False)
        elif action == "B'":
            self.rot_B(True)
        #cube rots
        elif action == "LL":
            self.cube_rot_left()
        elif action == "RR":
            self.cube_rot_right()
        elif action == "DD":
            self.cube_rot_down()
        elif action == "UU":
            self.cube_rot_up()
        else:
            raise Error
            
    def apply_seq(self, seq):
        actions = seq.split()
        for action in actions:
            self.apply(action)

    def solve(self, solver):
        seq = solver.solve()
        #self.apply_seq(seq)
        return seq