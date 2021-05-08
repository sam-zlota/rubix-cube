from constants import up, down, left, right, front, back, y, w, r, o, g, b

class Solver:
    def __init__(self, cube):
        self.cube = cube
    
    def solve(self):
        '''
            Returns solve sequence steps
        '''
        self.solve_daisy()
        self.solve_white_cross()
        # self.solve_white_corners()

        return self.cube.actions

    def solve_daisy(self):
        '''
            Solves the daisy portion of the cube and outputs steps taken to solve
        '''
        # search face
        while not self.check_daisy():
            front_face = self.cube.get_face_from_orient(front)
            top_face = self.cube.get_face_from_orient(up)
            down_face = self.cube.get_face_from_orient(down)
            # check for edge already in top layer
            if top_face[2][1] == w: 
                self.cube.apply_seq(["U"])
            elif front_face[0][1] == w:
                self.cube.apply_seq(["RR", "R'", "U", "F'"] )
            # middle left edge or  middle right edge
            elif front_face[1][0] == w or front_face[1][2] == w:
                # rotate front not prime
                self.cube.apply_seq(["F"])
            # bottom edge or down face
            elif front_face[2][1] == w or down_face[0][1] == w:
                # rotate front twice
                self.cube.apply_seq(["F", "F"] )
            else:
                # rotate face and break from while loop
                self.cube.apply_seq( ["LL"] )

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
            front_color = self.cube.get_color_from_orient(front)
            front_face = self.cube.get_face_from_orient(front)

            top_face = self.cube.get_face_from_orient(up)

            while front_face[0][1] != front_color or top_face[2][1] != w:
                self.cube.apply_seq(["U"])
                front_face = self.cube.get_face_from_orient(front)
                top_face = self.cube.get_face_from_orient(up)
        
            self.cube.apply_seq(["F", "F", "LL"])

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

    def solve_white_corners(self):
        # rotate face up twice so that white cross is on up face
        self.cube.cube_rot_up()
        self.cube.cube_rot_up()
        assert(self.cube.orient_dict[up] == w)

        # bring all incorrect white tiles to the bottom layer
        for _ in range(3):
            front_color = self.cube.orient_dict[front]
            front_face = self.cube.color_dict[front_color]

            top_color = self.cube.orient_dict[up]
            top_face = self.cube.color_dict[top_color]

            right_color = self.cube.orient_dict[right]
            right_face = self.cube.color_dict[right_color]

            left_color = self.cube.orient_dict[left]
            left_face = self.cube.color_dict[left_color]

            down_color = self.cube.orient_dict[down]
            down_face = self.cube.color_dict[down_color]

            # top right corner is correct
            right_corner = top_face[2][2] == w and front_face[0][2] == front_face[1][1] and right_face[0][0] == right_face[1][1]

            if not right_corner:
                #right corner not correct
                if top_face[2][2] == w or front_face[0][2] == w or right_face[0][0] == w:
                    #while top_face[2][2] == w or front_face[0][2] == w or right_face[0][0] == w:
                    # while face to come to top is white, rotate bottom until it is not white
                    while down_face[2][0] == w:
                        
                        self.cube.rotate(down, False)

                        front_color = self.cube.orient_dict[front]
                        front_face = self.cube.color_dict[front_color]

                        top_color = self.cube.orient_dict[up]
                        top_face = self.cube.color_dict[top_color]

                        right_color = self.cube.orient_dict[right]
                        right_face = self.cube.color_dict[right_color]

                        left_color = self.cube.orient_dict[left]
                        left_face = self.cube.color_dict[left_color]

                        down_color = self.cube.orient_dict[down]
                        down_face = self.cube.color_dict[down_color]
                        
                    # but there is a white tile in the top right corner somewhere
                    # then bring it down
                    self.cube.rotate(right, True)
                    self.cube.rotate(down, True)
                    self.cube.rotate(right, False)

                    front_color = self.cube.orient_dict[front]
                    front_face = self.cube.color_dict[front_color]

                    top_color = self.cube.orient_dict[up]
                    top_face = self.cube.color_dict[top_color]

                    right_color = self.cube.orient_dict[right]
                    right_face = self.cube.color_dict[right_color]

                    left_color = self.cube.orient_dict[left]
                    left_face = self.cube.color_dict[left_color]

                    down_color = self.cube.orient_dict[down]
                    down_face = self.cube.color_dict[down_color]
                    
                    
                    
            #now rotate and reset variables
            self.cube.cube_rot_left()
        

        # while step is not solved
        while not self.check_white_corners():
        #for i in range(20):
            print(self.cube)
            front_color = self.cube.orient_dict[front]
            front_face = self.cube.color_dict[front_color]

            top_color = self.cube.orient_dict[up]
            top_face = self.cube.color_dict[top_color]

            right_color = self.cube.orient_dict[right]
            right_face = self.cube.color_dict[right_color]

            down_color = self.cube.orient_dict[down]
            down_face = self.cube.color_dict[down_color]

            '''
            # check if corner piece is in top layer but wrong location
            corner_correct = front_face[0][2] == front_face[0][1] and right_face[0][0] == right_face[0][1]
            if (top_face[2][2] == w and not corner_correct) or front_face[0][2] == w or right_face[0][0]:
                # R' D' R
                self.cube.rotate(right, True)
                self.cube.rotate(down, True)
                self.cube.rotate(right, False)

                #self.cube.cube_rot_left()
            '''

            # check for corner piece with white tile in bottom layer and right side front face
            if front_face[2][2] == w: 
                # check for corner piece in correct position (other face colors match)
                if down_face[0][2] == front_face[1][1] and right_face[2][0] == right_face[1][1]:
                    # D' R' D R
                    self.cube.rotate(down, True)
                    self.cube.rotate(right, True)
                    self.cube.rotate(down, False)
                    self.cube.rotate(right, False)
                else:
                    # D
                    self.cube.rotate(down, False)
                    # face rotate right
                    self.cube.cube_rot_left()
            # check for corner piece with white tile in bottom layer and left side right face
            elif right_face[2][0] == w:
                # check for corner piece in correct position (other face colors match)
                if front_face[2][2] == front_face[1][1] and down_face[0][2] == right_face[1][1]:
                    # rotate face left
                    self.cube.cube_rot_left()
                    
                    # D L D' L'
                    self.cube.rotate(down, False)
                    self.cube.rotate(left, False)
                    self.cube.rotate(down, True)
                    self.cube.rotate(left, True)
                else:
                    # D
                    self.cube.rotate(down, False)
                    # face rotate left
                    self.cube.cube_rot_left()
            # check for corner piece with white tile in bottom layer and right side down face
            elif down_face[0][2] == w:
                if top_face[2][2] != w:
                    # move so facing front
                    # F D' F' D2
                    self.cube.rotate(front, False)
                    self.cube.rotate(down, True)
                    self.cube.rotate(front, True)
                    self.cube.rotate(down, False)
                    self.cube.rotate(down, False)
                else:
                    self.cube.rotate(down, False)
                    self.cube.cube_rot_left()
            
            # rotate face
            else:
                self.cube.cube_rot_left()

        return ''

        def check_white_corners(self):
            '''
            Checks if step 3 is complete assuming orientation, white top, yellow bottom
            '''
            # assert self.check_daisy() and self.check_white_cross()
            # assert self.cube.orient_dict[up] == w and self.cube.orient_dict[down] == y
            white_face = self.cube.color_dict[w]
            white_row_one = white_face[0][0] == w and white_face[0][1] == w and white_face[0][2] == w
            white_row_two = white_face[1][0] == w and white_face[1][1] == w and white_face[1][2] == w
            white_row_three = white_face[2][0] == w and white_face[2][1] == w and white_face[2][2] == w

            white_solved = white_row_one and white_row_two and white_row_three

            f = [o, g, b, r]
            solved = []

            for face in f:
                current_face = self.cube.color_dict[face]

                current_solved = current_face[0][0] == face and current_face[0][1] == face and current_face[0][2] == face and current_face[1][1] == face
                solved.append(current_solved)
            print(sum(solved))
            return sum(solved) == len(solved) and white_solved



