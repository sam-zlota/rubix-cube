from constants import up, down, left, right, front, back, y, w, r, o, g, b

class Solver:
    def __init__(self, cube):
        self.cube = cube
    def solve(self):
        '''
            Returns solve sequence steps
        '''
        #sequence = [] # to contain solve sequence
        seq = self.solve_daisy()
        seq += self.solve_white_cross()

        return seq

    def solve_daisy(self):
        '''
            Solves the daisy portion of the cube and outputs steps taken to solve
        '''
        steps = [] # to contain steps taken to solve

        # search face
        while not self.check_daisy():
            cube_orient = self.cube.orient_dict
            cube_dict = self.cube.color_dict 
            front_face = cube_dict[cube_orient[front]]
            top_face = cube_dict[cube_orient[up]]
            down_face = cube_dict[cube_orient[down]]

            # check for edge already in top layer

            if top_face[2][1] == w: 
                step = self.cube.rotate(up, False)
                steps.append(step)
                continue
   
            if front_face[0][1] == w:
                step = self.cube.cube_rot_right()
                steps.append(step)

                # rotate right prime
                step = self.cube.rotate(right, True)
                steps.append(step)
                # rotate up not prime
                step = self.cube.rotate(up, False)
                steps.append(step)
                # rotate front prime
                step = self.cube.rotate(front, True)
                steps.append(step)

            # middle left edge
            elif front_face[1][0] == w:
                # rotate front not prime
                step = self.cube.rotate(front, False)
                steps.append(step)
            # middle right edge
            elif front_face[1][2] == w:
                # rotate front prime
                step = self.cube.rotate(front, True)
                steps.append(step)
            # bottom edge
            elif front_face[2][1] == w:
                # rotate front twice
                step = self.cube.rotate(front, False)
                steps.append(step)
                step = self.cube.rotate(front, False)
                steps.append(step)
            # down face
            elif down_face[0][1] == w:
                # print('down face')    
                # rotate front twice
                step = self.cube.rotate(front, False)
                steps.append(step)
                step = self.cube.rotate(front, False)
                steps.append(step)
            else:
                # rotate face and break from while loop
                step = self.cube.cube_rot_left()
                steps.append(step)

        return steps

    def check_daisy(self):
        '''
            Returns True if daisy is solved
        '''
        yellow_face = self.cube.color_dict[y]
        edge1 = yellow_face[0][1] == w
        edge2 = yellow_face[1][0] == w
        edge3 = yellow_face[1][2] == w
        edge4 = yellow_face[2][1] == w 

        return edge1 and edge2 and edge3 and edge4

    def solve_white_cross(self):
        steps = []
        for i in range(4):
            front_color = self.cube.orient_dict[front]
            front_face = self.cube.color_dict[front_color]

            top_face = self.cube.color_dict[self.cube.orient_dict[up]]

            while front_face[0][1] != front_color or top_face[2][1] != w:
                steps.append(self.cube.rotate(up, False))
                front_face = self.cube.color_dict[front_color]
                top_face = self.cube.color_dict[self.cube.orient_dict[up]]
        
            steps.append(self.cube.rotate(front, False))
            steps.append(self.cube.rotate(front, False))
            steps.append(self.cube.cube_rot_left())

        return steps

    def check_white_cross(self):
        white_face = self.cube.color_dict[w]
        green_face = self.cube.color_dict[g]
        red_face = self.cube.color_dict[r]
        orange_face = self.cube.color_dict[o]
        blue_face = self.cube.color_dict[b]

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
        # while step is not solved
        while not self.check_white_corners():
            front_color = self.cube.orient_dict[front]
            front_face = self.cube.color_dict[front_color]

            top_color = self.cube.orient_dict[top]
            top_face = self.cube.color_dict[top_color]

            right_color = self.cube.orient_dict[right]
            right_face = self.cube.color_dict[right_color]

            down_color = self.cube.orient_dict[down]
            down_face = self.cube.color_dict[down_color]

            # check if corner piece is in top layer but wrong location
            corner_correct = front_face[0][2] == front_face[0][1] and right_face[0][0] == right_face[0][1]
            if top_face[2][0] == w and not corner_correct:
                # R' D' R
                pass 
                
            # check for corner piece with white tile in bottom layer and right side front face
            if front_face[2][2] == w: 
                # check for corner piece in correct position (other face colors match)
                if down_face[0][2] == front_face[1][1] and right_face[2][0] == right_face[1][1]:
                    # D' R' D R
                    self.cube.rotate('down', True)
                    self.cube.rotate('right', True)
                    self.cube.rotate('down', False)
                    self.cube.rotate('right', False)
                else:
                    # D
            # check for corner piece with white tile in bottom layer and left side right face
            elif right_face[2][0] == w:
                # check for corner piece in correct position (other face colors match)
                if front_face[2][2] == front_face[1][1] and down_face[0][2] == right_face[1][1]:
                    # D L D' L'     
                else
                    # D
            # check for corner piece with white tile in bottom layer and right side down face
            elif down_face[0][2] == w:
                # move so facing front
                # F D' F' D2
                # check for corner piece in correct position (other face colors match)
                if front_face[1][1] == front_face[2][2] and right_face[2][0] == right_face[1][1]:
                    pass


    def check_white_corners(self):
        '''
        Checks if step 3 is complete assuming orientation, white top, yellow bottom
        '''
        white_face = self.cube.color_dict[w]
        white_row_one = white_face[0][0] == w and white_face[0][1] == w and white_face[0][2] == w
        white_row_two = white_face[1][0] == w and white_face[1][1] == w and white_face[1][2] == w
        white_row_three = white_face[2][0] == w and white_face[2][1] == w and white_face[3][2] == w

        white_solved = white_row_one and white_row_two and white_row_three

        faces = [o, g, b, r]
        solved = []

        for face in faces:
            current_face = self.cube.color_dict[face]

            current_solved = current_face[0][0] and current_face[0][1] and current_face[0][2] and current_face[1][1]
            solved.append(current_solved)

        return (sum(solved) == len(solved)) and white_solved






