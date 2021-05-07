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







