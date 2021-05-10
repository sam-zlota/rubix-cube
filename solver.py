from constants import *

class Solver:
    def __init__(self, cube):
        self.cube = cube
    
    def solve(self):
        '''
            Returns solve sequence steps
        '''
        self.solve_daisy()
        self.solve_white_cross()
        self.solve_white_corners()
        self.solve_middle_layer()

        return self.cube.actions

    def solve_daisy(self):
        '''
            Solves the daisy portion of the cube and outputs steps taken to solve
        '''
        # search face
        while not self.check_daisy():
            front_face = self.cube.get_face_from_orient(FRONT)
            top_face = self.cube.get_face_from_orient(UP)
            down_face = self.cube.get_face_from_orient(DOWN)
            # check for edge already in top layer
            if top_face[2][1] == w: 
                self.cube.apply_seq([UP])
            elif front_face[0][1] == w:
                self.cube.apply_seq([CUBE_ROT_RIGHT, RIGHT_PRIME, UP, FRONT_PRIME] )
            # middle left edge or  middle right edge
            elif front_face[1][0] == w or front_face[1][2] == w:
                # rotate front not prime
                self.cube.apply_seq([FRONT])
            # bottom edge or down face
            elif front_face[2][1] == w or down_face[0][1] == w:
                # rotate front twice
                self.cube.apply_seq([FRONT, FRONT])
            else:
                # rotate face and break from while loop
                self.cube.apply_seq( [CUBE_ROT_LEFT] )

    def check_daisy(self):
        '''
            Returns True if daisy is solved
        '''
        yellow_face = self.cube.get_face_from_color(y)
        edge1 = yellow_face[0][1] == w
        edge2 = yellow_face[1][0] == w
        edge3 = yellow_face[1][2] == w
        edge4 = yellow_face[2][1] == w 

        return edge1 and edge2 and edge3 and edge4

    def solve_white_cross(self):
        for i in range(4):
            front_color = self.cube.get_color_from_orient(FRONT)
            front_face = self.cube.get_face_from_orient(FRONT)

            top_face = self.cube.get_face_from_orient(UP)

            while front_face[0][1] != front_color or top_face[2][1] != w:
                self.cube.apply_seq([UP])
                front_face = self.cube.get_face_from_orient(FRONT)
                top_face = self.cube.get_face_from_orient(UP)
        
            self.cube.apply_seq([FRONT, FRONT, CUBE_ROT_LEFT])

    def check_white_cross(self):
        white_face = self.cube.get_face_from_color(w)
        green_face = self.cube.get_face_from_color(g)
        red_face = self.cube.get_face_from_color(r)
        orange_face = self.cube.get_face_from_color(o)
        blue_face = self.cube.get_face_from_color(b)

        edge1 = white_face[0][1] == w
        edge2 = white_face[1][0] == w
        edge3 = white_face[1][2] == w
        edge4 = white_face[2][1] == w 

        white_cross = edge1 and edge2 and edge3 and edge4

        green_edge = green_face[2][1] == g
        red_edge = red_face[2][1] == r
        orange_edge = orange_face[2][1] == o
        blue_edge = blue_face[2][1] == b 

        centers_matched = green_edge and red_edge and orange_edge and blue_edge

        return white_cross and centers_matched

    def get_faces(self):
        return self.cube.get_face_from_orient(FRONT) , self.cube.get_face_from_orient(UP), self.cube.get_face_from_orient(RIGHT), self.cube.get_face_from_orient(LEFT), self.cube.get_face_from_orient(DOWN)

    def solve_white_corners(self):        

        def move_corner_in_between():
            #corner is in bottom layer, so we need to rotate down until it is in between
            #its two corresponding centers
            front_face, top_face, right_face, left_face, down_face = self.get_faces()
            front_color = None

            if front_face[2][2] == w:
                front_color = down_face[0][2]
            if right_face[2][0] == w:
                front_color = front_face[2][2]
            if down_face[0][2] == w:
                front_color = right_face[2][0]
            while front_face[1][1] != front_color:
                self.cube.apply_seq([DOWN, CUBE_ROT_LEFT])
                front_face, top_face, right_face, left_face, down_face = self.get_faces()

        
        def bring_corner_up():
            front_face, top_face, right_face, left_face, down_face = self.get_faces()
            #corner piece must be in bottom right corner of front face, so we can bring it up
            if front_face[2][2] == w:
                self.cube.apply_seq([DOWN_PRIME, RIGHT_PRIME, DOWN, RIGHT])
            if right_face[2][0] == w:
                
                self.cube.apply_seq([CUBE_ROT_LEFT, DOWN, LEFT, DOWN_PRIME, LEFT_PRIME, CUBE_ROT_RIGHT])
            if down_face[0][2] == w:
                self.cube.apply_seq([FRONT, DOWN_PRIME, FRONT_PRIME, DOWN, DOWN])
                bring_corner_up()

        #rotate face up twice so that white cross is on up face
        self.cube.apply_seq([CUBE_ROT_UP, CUBE_ROT_UP])
        
        #for each corner
        while not self.check_white_corners():
            front_face, top_face, right_face, left_face, down_face = self.get_faces()

            right_corner = top_face[2][2] == w and front_face[0][2] == front_face[1][1] and right_face[0][0] == right_face[1][1]

            if top_face[2][2] == w or front_face[0][2] == w or right_face[0][0] == w:
                if not right_corner:
                    #bring her down into bottom right corner
                    self.cube.apply_seq([RIGHT_PRIME, DOWN_PRIME, RIGHT, DOWN])
                    move_corner_in_between()
                    bring_corner_up()
            else:
                # check bottom layer
                for _ in range(4):
                    front_face, top_face, right_face, left_face, down_face = self.get_faces()
                    if front_face[2][2] == w or right_face[2][0] == w or down_face[0][2] == w:
                        #found a corner
                        #get it in between the proper center pieces
                        move_corner_in_between()
                        bring_corner_up()
                    else:
                      self.cube.apply_seq([DOWN])
     
            self.cube.apply_seq([CUBE_ROT_LEFT])

    def check_white_corners(self):
        '''
        Checks if step 3 is complete assuming orientation, white top, yellow bottom
        '''

        white_face = self.cube.get_face_from_color(w)
        white_row_one = white_face[0][0] == w and white_face[0][1] == w and white_face[0][2] == w
        white_row_two = white_face[1][0] == w and white_face[1][1] == w and white_face[1][2] == w
        white_row_three = white_face[2][0] == w and white_face[2][1] == w and white_face[2][2] == w

        white_solved = white_row_one and white_row_two and white_row_three

        f = [o, g, b, r]
        solved = []

        for face in f:
            current_face = self.cube.get_face_from_color(face)

            current_solved = current_face[0][0] == face and current_face[0][1] == face and current_face[0][2] == face and current_face[1][1] == face
            solved.append(current_solved)
        return sum(solved) == len(solved) and white_solved

    def solve_middle_layer(self):
        '''
        1. check for top edge piece that does not have yellow side
            - make piece be on front face
            - make located piece go to correct location by doing up and rotate left enough times
            - when in correct position, move piece down
        2. if no top edge piece is valid
            - check for middle edge piece with no yellow side
        '''
        def get_valid_piece(front, right, back, left):
            top_edge_loc = [(2, 1), (1, 2), (0, 1), (1, 0)]
            faces_to_search = [front, right, back, left]
            valid_piece = None
            i = 0
            # attempts to find valid top layer edge piece
            while valid_piece is None and i < 4:
                # if both top and front faces are not yellow, then valid
                if faces_to_search[i][0][1] != y and top_face[top_edge_loc[i][0]][top_edge_loc[i][1]] != y:
                    valid_piece = i
                    break
                i += 1

            return valid_piece
       
        # make white face down and yellow up
        self.cube.apply_seq([CUBE_ROT_UP, CUBE_ROT_UP])

        def make_front_face(valid):
            # make piece be on front face
            seq = []
            for _ in range(valid):
                seq.append(CUBE_ROT_LEFT)
            return seq

        def get_not_exists_sequence(front, right, left, back):
            # valid piece exists on right side of front face
            if front[1][2] != y and right[1][0] != y:
                return [UP, RIGHT, UP_PRIME, RIGHT_PRIME, UP_PRIME, FRONT_PRIME, UP, FRONT]
            # valid piece exists on left side of front face
            if front[1][0] != y and left[1][2] != y:
                return [CUBE_ROT_RIGHT, UP, RIGHT, UP_PRIME, RIGHT_PRIME, UP_PRIME, FRONT_PRIME, UP, FRONT]
            # valid piece exists on left side of left face
            if left[1][0] != y and back[1][2] != y:
                return [CUBE_ROT_RIGHT, CUBE_ROT_RIGHT, UP, RIGHT, UP_PRIME, RIGHT_PRIME, UP_PRIME, FRONT_PRIME, UP, FRONT]
            # valid piece exists on right side of right face
            if right[1][2] != y and back[1][0] != y:
                return [CUBE_ROT_LEFT, UP, RIGHT, UP_PRIME, RIGHT_PRIME, UP_PRIME, FRONT_PRIME, UP, FRONT]


        while not self.check_middle_layer():
            front_face, top_face, right_face, left_face, down_face = self.get_faces()
            back_face = self.cube.get_face_from_orient(BACK)

            # get valid piece
            valid_piece = get_valid_piece(front_face, right_face, back_face, left_face)

            # piece exists
            if valid_piece is not None:
                # move valid piece to front face
                self.cube.apply_seq(make_front_face(valid_piece))

                front_face, top_face, right_face, left_face, down_face = self.get_faces()
                back_face = self.cube.get_face_from_orient(BACK)

                # make piece go to correct location
                while front_face[0][1] != front_face[1][1]:
                    self.cube.apply_seq([UP_PRIME, CUBE_ROT_LEFT])
                    front_face, top_face, right_face, left_face, down_face = self.get_faces()
                    back_face = self.cube.get_face_from_orient(BACK)

                # move piece down right
                if top_face[2][1] == right_face[1][1]:
                    self.cube.apply_seq([UP, RIGHT, UP_PRIME, RIGHT_PRIME, UP_PRIME, FRONT_PRIME, UP, FRONT])
                # move piece down left
                else:
                    self.cube.apply_seq([UP_PRIME, LEFT_PRIME, UP, LEFT, UP, FRONT, UP_PRIME, FRONT_PRIME])
            # piece does not exist
            else:
                # apply sequence for this case
                self.cube.apply_seq(get_not_exists_sequence(front_face, right_face, left_face, back_face))


    def check_middle_layer(self):
        '''
        Assuming yellow on top white on bottom, check if middle layer is complete
        '''
        back_face = self.cube.get_face_from_orient(BACK)
        down_face = self.cube.get_face_from_orient(DOWN)

        white_complete = True

        for i in range(3):
            for j in range(3):
                if down_face[i][j] != w:
                    white_complete = False

        other_faces = [FRONT, RIGHT, LEFT, BACK]

        other_solved = True

        for face in other_faces:
            current_color = self.cube.get_color_from_orient(face)
            current_face = self.cube.get_face_from_orient(face)
            for i in range(1, 3):
                for j in range(3):
                    if current_face[i][j] != current_color:
                        other_solved = False

        return white_complete and other_solved
