from constants import *


class Solver:
    def __init__(self, cube):
        self.cube = cube

    def solve(self):
        """
            Returns solve sequence steps
        """
        self.solve_daisy()
        self.solve_white_cross()
        self.solve_white_corners()
        self.solve_middle_layer()
        self.solve_yellow_cross()
        self.solve_yellow_corners()
        self.solve_position_yellow_corners()
        #self.solve_final_stage()

        return self.cube.actions

    def solve_daisy(self):
        """
            Solves the daisy portion of the cube and outputs steps taken to solve
        """
        # search face
        while not self.check_daisy():
            front_face = self.cube.get_face_from_orient(FRONT)
            top_face = self.cube.get_face_from_orient(UP)
            down_face = self.cube.get_face_from_orient(DOWN)
            # check for edge already in top layer
            if top_face[2][1] == WHITE:
                self.cube.apply_seq([UP])
            elif front_face[0][1] == WHITE:
                self.cube.apply_seq([CUBE_ROT_RIGHT, RIGHT_PRIME, UP, FRONT_PRIME])
            # middle left edge or  middle right edge
            elif front_face[1][0] == WHITE or front_face[1][2] == WHITE:
                # rotate front not prime
                self.cube.apply_seq([FRONT])
            # bottom edge or down face
            elif front_face[2][1] == WHITE or down_face[0][1] == WHITE:
                # rotate front twice
                self.cube.apply_seq([FRONT, FRONT])
            else:
                # rotate face and break from while loop
                self.cube.apply_seq([CUBE_ROT_LEFT])

    def check_daisy(self):
        """
            Returns True if daisy is solved
        """
        yellow_face = self.cube.get_face_from_color(YELLOW)
        edge1 = yellow_face[0][1] == WHITE
        edge2 = yellow_face[1][0] == WHITE
        edge3 = yellow_face[1][2] == WHITE
        edge4 = yellow_face[2][1] == WHITE

        return edge1 and edge2 and edge3 and edge4

    def solve_white_cross(self):
        for _ in range(4):
            front_color = self.cube.get_color_from_orient(FRONT)
            front_face = self.cube.get_face_from_orient(FRONT)
            top_face = self.cube.get_face_from_orient(UP)

            while front_face[0][1] != front_color or top_face[2][1] != WHITE:
                self.cube.apply_seq([UP])
                front_face = self.cube.get_face_from_orient(FRONT)
                top_face = self.cube.get_face_from_orient(UP)

            self.cube.apply_seq([FRONT, FRONT, CUBE_ROT_LEFT])

    def check_white_cross(self):
        white_face = self.cube.get_face_from_color(WHITE)
        green_face = self.cube.get_face_from_color(GREEN)
        red_face = self.cube.get_face_from_color(RED)
        orange_face = self.cube.get_face_from_color(ORANGE)
        blue_face = self.cube.get_face_from_color(BLUE)

        edge1 = white_face[0][1] == WHITE
        edge2 = white_face[1][0] == WHITE
        edge3 = white_face[1][2] == WHITE
        edge4 = white_face[2][1] == WHITE

        white_cross = edge1 and edge2 and edge3 and edge4

        green_edge = green_face[2][1] == GREEN
        red_edge = red_face[2][1] == RED
        orange_edge = orange_face[2][1] == ORANGE
        blue_edge = blue_face[2][1] == BLUE

        centers_matched = green_edge and red_edge and orange_edge and blue_edge

        return white_cross and centers_matched

    def get_faces(self):
        return self.cube.get_face_from_orient(FRONT), self.cube.get_face_from_orient(
            UP), self.cube.get_face_from_orient(RIGHT), self.cube.get_face_from_orient(
            LEFT), self.cube.get_face_from_orient(DOWN)

    def solve_white_corners(self):

        def move_corner_in_between():
            # corner is in bottom layer, so we need to rotate down until it is in between
            # its two corresponding centers
            front_face, _, right_face, _, down_face = self.get_faces()
            front_color = None

            if front_face[2][2] == WHITE:
                front_color = down_face[0][2]
            if right_face[2][0] == WHITE:
                front_color = front_face[2][2]
            if down_face[0][2] == WHITE:
                front_color = right_face[2][0]
            while front_face[1][1] != front_color:
                self.cube.apply_seq([DOWN, CUBE_ROT_LEFT])
                front_face, _, right_face, _, down_face = self.get_faces()

        def bring_corner_up():
            front_face, _, right_face, _, down_face = self.get_faces()
            # corner piece must be in bottom right corner of front face, so we can bring it up
            if front_face[2][2] == WHITE:
                self.cube.apply_seq([DOWN_PRIME, RIGHT_PRIME, DOWN, RIGHT])
            if right_face[2][0] == WHITE:
                self.cube.apply_seq([CUBE_ROT_LEFT, DOWN, LEFT, DOWN_PRIME, LEFT_PRIME, CUBE_ROT_RIGHT])
            if down_face[0][2] == WHITE:
                self.cube.apply_seq([FRONT, DOWN_PRIME, FRONT_PRIME, DOWN, DOWN])
                bring_corner_up()

        # rotate face up twice so that white cross is on up face
        self.cube.apply_seq([CUBE_ROT_UP, CUBE_ROT_UP])

        # for each corner
        while not self.check_white_corners():
            front_face, top_face, right_face, _, down_face = self.get_faces()

            right_corner = top_face[2][2] == WHITE and front_face[0][2] == front_face[1][1] and right_face[0][0] == \
                           right_face[1][1]

            if top_face[2][2] == WHITE or front_face[0][2] == WHITE or right_face[0][0] == WHITE:
                if not right_corner:
                    # bring her down into bottom right corner
                    self.cube.apply_seq([RIGHT_PRIME, DOWN_PRIME, RIGHT, DOWN])
                    move_corner_in_between()
                    bring_corner_up()
            else:
                # check bottom layer
                for _ in range(4):
                    front_face, top_face, right_face, _, down_face = self.get_faces()
                    if front_face[2][2] == WHITE or right_face[2][0] == WHITE or down_face[0][2] == WHITE:
                        # found a corner
                        # get it in between the proper center pieces
                        move_corner_in_between()
                        bring_corner_up()
                    else:
                        self.cube.apply_seq([DOWN])

            self.cube.apply_seq([CUBE_ROT_LEFT])

    def check_white_corners(self):
        """
        Checks if step 3 is complete assuming orientation, white top, yellow bottom
        """

        white_face = self.cube.get_face_from_color(WHITE)
        white_row_one = white_face[0][0] == WHITE and white_face[0][1] == WHITE and white_face[0][2] == WHITE
        white_row_two = white_face[1][0] == WHITE and white_face[1][1] == WHITE and white_face[1][2] == WHITE
        white_row_three = white_face[2][0] == WHITE and white_face[2][1] == WHITE and white_face[2][2] == WHITE

        white_solved = white_row_one and white_row_two and white_row_three

        f = [ORANGE, GREEN, BLUE, RED]
        solved = []

        for face in f:
            current_face = self.cube.get_face_from_color(face)

            current_solved = current_face[0][0] == face and current_face[0][1] == face and current_face[0][
                2] == face and current_face[1][1] == face
            solved.append(current_solved)
        return sum(solved) == len(solved) and white_solved

    def solve_middle_layer(self):
        """
        1. check for top edge piece that does not have yellow side
            - make piece be on front face
            - make located piece go to correct location by doing up and rotate left enough times
            - when in correct position, move piece down
        2. if no top edge piece is valid
            - check for middle edge piece with no yellow side
        """

        def get_valid_piece(front, right, back, left):
            top_edge_loc = [(2, 1), (1, 2), (0, 1), (1, 0)]
            faces_to_search = [front, right, back, left]
            valid_piece = None
            i = 0
            # attempts to find valid top layer edge piece
            while valid_piece is None and i < 4:
                # if both top and front faces are not yellow, then valid
                if faces_to_search[i][0][1] != YELLOW and top_face[top_edge_loc[i][0]][top_edge_loc[i][1]] != YELLOW:
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
            if front[1][2] != YELLOW and right[1][0] != YELLOW:
                return [UP, RIGHT, UP_PRIME, RIGHT_PRIME, UP_PRIME, FRONT_PRIME, UP, FRONT]
            # valid piece exists on left side of front face
            if front[1][0] != YELLOW and left[1][2] != YELLOW:
                return [CUBE_ROT_RIGHT, UP, RIGHT, UP_PRIME, RIGHT_PRIME, UP_PRIME, FRONT_PRIME, UP, FRONT]
            # valid piece exists on left side of left face
            if left[1][0] != YELLOW and back[1][2] != YELLOW:
                return [CUBE_ROT_RIGHT, CUBE_ROT_RIGHT, UP, RIGHT, UP_PRIME, RIGHT_PRIME, UP_PRIME, FRONT_PRIME, UP,
                        FRONT]
            # valid piece exists on right side of right face
            if right[1][2] != YELLOW and back[1][0] != YELLOW:
                return [CUBE_ROT_LEFT, UP, RIGHT, UP_PRIME, RIGHT_PRIME, UP_PRIME, FRONT_PRIME, UP, FRONT]

        while not self.check_middle_layer():
            front_face, top_face, right_face, left_face, _ = self.get_faces()
            back_face = self.cube.get_face_from_orient(BACK)

            # get valid piece
            valid_piece = get_valid_piece(front_face, right_face, back_face, left_face)

            # piece exists
            if valid_piece is not None:
                # move valid piece to front face
                self.cube.apply_seq(make_front_face(valid_piece))

                front_face, top_face, right_face, left_face, _ = self.get_faces()
                back_face = self.cube.get_face_from_orient(BACK)

                # make piece go to correct location
                while front_face[0][1] != front_face[1][1]:
                    self.cube.apply_seq([UP_PRIME, CUBE_ROT_LEFT])
                    front_face, top_face, right_face, left_face, _ = self.get_faces()
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
        """
        Assuming yellow on top white on bottom, check if middle layer is complete
        """
        # back_face = self.cube.get_face_from_orient(BACK)
        down_face = self.cube.get_face_from_orient(DOWN)

        white_complete = True

        for i in range(3):
            for j in range(3):
                if down_face[i][j] != WHITE:
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

    def solve_yellow_cross(self):

        while not self.check_yellow_cross():
            yellow_face = self.cube.get_face_from_color(YELLOW)
            
            top_edge = yellow_face[0][1] == YELLOW
            right_edge = yellow_face[1][2] == YELLOW
            left_edge = yellow_face[1][0] == YELLOW
            bottom_edge = yellow_face[2][1] == YELLOW

            if top_edge and bottom_edge:
                self.cube.apply_seq([UP])
            elif top_edge and right_edge:
                self.cube.apply_seq([UP_PRIME])
            elif right_edge and bottom_edge:
                self.cube.apply_seq([UP_PRIME, UP_PRIME])
            elif left_edge and bottom_edge:
                self.cube.apply_seq([UP])

            self.cube.apply_seq([FRONT, UP, RIGHT, UP_PRIME, RIGHT_PRIME, FRONT_PRIME])

    def check_yellow_cross(self):
        yellow_face = self.cube.get_face_from_color(YELLOW)

        top_edge = yellow_face[0][1] == YELLOW
        right_edge = yellow_face[1][2] == YELLOW
        left_edge = yellow_face[1][0] == YELLOW
        bottom_edge = yellow_face[2][1] == YELLOW

        return top_edge and right_edge and left_edge and bottom_edge

    def solve_yellow_corners(self):
  
        while not self.check_yellow_corners():
            yellow_face = self.cube.get_face_from_color(YELLOW)

            top_left = yellow_face[0][0] == YELLOW
            top_right = yellow_face[0][2] == YELLOW
            bottom_left = yellow_face[2][0] == YELLOW
            bottom_right = yellow_face[2][2] == YELLOW

            yellow_count = top_right + top_left + bottom_right + bottom_left
            if yellow_count == 0:
                while not self.cube.get_face_from_orient(LEFT)[0][2] == YELLOW:
                    self.cube.apply_seq([UP])
            if yellow_count == 1:
                if top_left:
                    self.cube.apply_seq([UP_PRIME])
                if top_right:
                    self.cube.apply_seq([UP, UP])
                if bottom_right:
                    self.cube.apply_seq([UP])
            if yellow_count == 2:
                while not self.cube.get_face_from_orient(FRONT)[0][0] == YELLOW:
                    self.cube.apply_seq([UP])

            self.cube.apply_seq([RIGHT, UP, RIGHT_PRIME, UP, RIGHT, UP, UP, RIGHT_PRIME])



    def check_yellow_corners(self):
        yellow_face = self.cube.get_face_from_color(YELLOW)

        top_left = yellow_face[0][0] == YELLOW
        top_right = yellow_face[0][2] == YELLOW
        bottom_left = yellow_face[2][0] == YELLOW
        bottom_right = yellow_face[2][2] == YELLOW

        return top_left and top_right and bottom_left and bottom_right


    def solve_position_yellow_corners(self):

        while not self.check_position_yellow_corners():
           
            front_face = self.cube.get_face_from_orient(FRONT)
            left_face = self.cube.get_face_from_orient(LEFT)
            right_face = self.cube.get_face_from_orient(RIGHT)
            back_face = self.cube.get_face_from_orient(BACK)

            front_color = self.cube.get_color_from_orient(FRONT)
            left_color = self.cube.get_color_from_orient(LEFT)
            right_color = self.cube.get_color_from_orient(RIGHT)
            back_color = self.cube.get_color_from_orient(BACK)

            def adjacent_corners():
                '''
                Using the current orientation, returns the front face which contains
                a back with matching corners
                '''
                def check_back_corners(front_face, left_face, right_face, front_color, left_color, right_color):
                    front_left = front_face[0][0] == front_color 
                    front_right = front_face[0][2] == front_color
                    front_match = front_left and front_right

                    right_match = right_face[0][0] == right_color 
                    left_match = left_face[0][2] == left_color 

                    return front_match and right_match and left_match

                def check_front_corners(front_face, left_face, right_face, front_color, left_color, right_color):
                    front_left = front_face[0][0] == right_color 
                    front_right = front_face[0][2] == left_color 
                    front_match = front_left and front_right 

                    right_match = right_face[0][0] == front_color 
                    left_match = left_face[0][2] == front_color

                    return front_match and right_match and left_match 

                # check front case
                front_case_back = check_back_corners(back_face, right_face, left_face, back_color, right_color, left_color)
                front_case_front = check_front_corners(front_face, left_face, right_face, front_color, left_color, right_color)
                print(f'front_case_back: {front_case_back}')
                print(f'front_case_front: {front_case_front}')

                # check right case
                right_case_back = check_back_corners(left_face, back_face, front_face, left_color, back_color, front_face)
                right_case_front = check_front_corners(right_face, front_face, back_face, right_color, front_color, back_color)
                print(f'right_case_back: {right_case_back}')
                print(f'right_case_front: {right_case_front}')

                # check left case
                left_case_back = check_back_corners(right_face, front_face, back_face, right_color, front_color, back_color)
                left_case_front = check_front_corners(left_face, back_face, front_face, left_color, back_color, front_color)
                print(f'left_case_back: {left_case_back}')
                print(f'left_case_front: {left_case_front}')

                # check back case
                back_case_back = check_back_corners(front_face, left_face, right_face, front_color, left_color, right_color)
                back_case_front = check_front_corners(back_face, right_face, left_face, back_color, right_color, left_color)
                print(f'back_case_back: {back_case_back}')
                print(f'back_case_front: {back_case_front}')

                if front_case_back and front_case_front:
                    return FRONT
                elif right_case_back and right_case_front:
                    return RIGHT
                elif left_case_back and left_case_front:
                    return LEFT 
                elif back_case_back and back_case_front:
                    return BACK 
                else:
                    return None
            
            def diagonal_corners():
                def check_corners_five(front_face, right_face, left_face, left_color, back_color):
                    front_left = front_face[0][0] == front_color 
                    front_right = front_face[0][2] == back_color 
                    front_match = front_left and front_right 

                    right_match = right_face[0][0] == left_color
                    left_match = left_face[0][2] == left_color

                    return front_match and right_match and left_match
                
                def check_corners_six(front_face, right_face, left_face, right_color, back_color):
                    front_left = front_face[0][0] == back_color 
                    front_right = front_face[0][2] == front_color  
                    front_match = front_left and front_right 

                    right_match = right_face[0][0] == right_color
                    left_match = left_face[0][2] == right_color

                    return front_match and right_match and left_match

                blue_face = self.cube.get_face_from_color(BLUE)
                green_face = self.cube.get_face_from_color(GREEN)
                orange_face = self.cube.get_face_from_color(ORANGE)
                red_face = self.cube.get_face_from_color(RED)
                
                # check for cube five match
                check_five_front = check_corners_five(blue_face, red_face, orange_face, ORANGE, GREEN)
                check_five_back = check_corners_five(green_face, orange_face, red_face, RED, BLUE)
                cube_five_match = check_five_back and check_five_front

                # check for cube six match
                check_six_front = check_corners_six(blue_face, red_face, orange_face, RED, GREEN)
                check_six_back = check_corners_six(green_face, orange_face, red_face, ORANGE, BLUE)
                cube_six_match = check_six_back and check_six_front

                if cube_five_match or cube_six_match:
                    return self.cube.get_orient_from_color(BLUE)
                else:
                    return None

            def bring_to_front(orientation):
                if orientation == LEFT:
                    return [CUBE_ROT_RIGHT]
                elif orientation == RIGHT:
                    return [CUBE_ROT_LEFT]
                elif orientation == BACK:
                    return [CUBE_ROT_RIGHT, CUBE_ROT_RIGHT]
                elif orientation == FRONT:
                    return []
                
            def apply_sequence():
                seq = [RIGHT_PRIME, FRONT, RIGHT_PRIME, BACK, BACK, RIGHT, FRONT_PRIME, RIGHT_PRIME, BACK, BACK, RIGHT, RIGHT, UP_PRIME]
                self.cube.apply_seq(seq)
            print(self.cube)
            # bring face to front
            adjacent = adjacent_corners()
            diagonal = diagonal_corners()
            if adjacent is not None:
                self.cube.apply_seq(bring_to_front(adjacent))
                apply_sequence()
            elif diagonal is not None:
                self.cube.apply_seq(bring_to_front(diagonal))
                apply_sequence()
            # no match found
            else:
                self.cube.apply_seq([UP])
            

    def check_position_yellow_corners(self):
        blue_face = self.cube.get_face_from_color(BLUE)
        red_face = self.cube.get_face_from_color(RED)
        green_face = self.cube.get_face_from_color(GREEN)
        orange_face = self.cube.get_face_from_color(ORANGE)

        blue_red_corner = blue_face[0][2] == BLUE and red_face[0][0] == RED 
        blue_orange_corner = blue_face[0][0] == BLUE and orange_face[0][2] == ORANGE 
        green_orange_corner = green_face[0][2] == GREEN and orange_face[0][0] == ORANGE 
        green_red_corner = green_face[0][0] == GREEN and red_face[0][2] == RED 

        return blue_red_corner and blue_orange_corner and green_orange_corner and green_red_corner 


    def solve_final_stage(self):

        def put_solved_face_on_back():
            for _ in range(4):
                back_face = self.cube.get_face_from_orient(BACK)
                top_layer = back_face[0]
                if top_layer[0] == top_layer[1] and top_layer[1] == top_layer[2]:
                    break
                else:
                    self.cube.apply_seq(CUBE_ROT_LEFT)

        seq = [FRONT, FRONT, UP, LEFT, RIGHT_PRIME, FRONT, FRONT, LEFT_PRIME, RIGHT, UP, FRONT,FRONT]

        while not check_final_step():
            put_solved_face_on_back()
            self.cube.apply_seq(seq)
    
    def check_final_step(self):
        colors = [RED, ORANGE, GREEN, BLUE]
        final_stage_solved = True
        for color in color:
            face = self.cube.get_face_from_color(color)
            top_layer = face[0]
            face_solved = top_layer[0] == top_layer[1] and top_layer[1] == top_layer[2]
            final_stage_solved = final_stage_solved and face_solved

        return final_stage_solved