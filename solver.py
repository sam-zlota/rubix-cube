from constants import up, down, left, right, front, back, y, w, r, o, g, b

class Solver:
    def __init__(self, cube):
        self.cube = cube
    def solve(self):
        '''
        Returns solve sequence steps
        '''
        #sequence = [] # to contain solve sequence
        sequence = self.solve_daisy()

        return sequence
        
    def solve_daisy(self):
        '''
        Solves the daisy portion of the cube and outputs steps taken to solve
        '''
        steps = [] # to contain steps taken to solve

        while True:
        #print('original state')
        #print(self.cube.print_v2())
        #for i in range(20):
            #print('outer loop')

            # daisy is solved
            if self.check_daisy():
                break 

            # check for white piece already facing up
            if self.cube.color_dict[self.cube.orient_dict[up]][2][1] == w:
                #print('up rotate')
                # rotate up prime
                step = self.cube.rotate(up, True)
                steps.append(step)
                #print(self.cube.print_v2())
            else:
                # search face
                while True:
                    cube_orient = self.cube.orient_dict
                    cube_dict = self.cube.color_dict 
                    front_face = cube_dict[cube_orient[front]]
                    top_face = cube_dict[cube_orient[up]]
                    down_face = cube_dict[cube_orient[down]]

                    # check for edge already in top layer
                    if front_face[0][1] == w:
                        #print('already on top')


                        # rotate one face right
                        step = self.cube.cube_rot_right()
                        steps.append('rotate one face right')


                        # rotate right prime
                        step = self.cube.rotate(right, True)
                        steps.append(step)
                        # rotate up not prime
                        step = self.cube.rotate(up, False)
                        steps.append(step)
                        # rotate front prime
                        step = self.cube.rotate(front, True)
                        steps.append(step)
                        #print(self.cube.print_v2())
                    # middle left edge
                    elif front_face[1][0] == w:
                        #print('middle left edge')
                        # rotate front not prime
                        step = self.cube.rotate(front, False)
                        steps.append(step)
                        #print(self.cube.print_v2())
                    # middle right edge
                    elif front_face[1][2] == w:
                        #print('middle right edge')
                        # rotate front prime
                        step = self.cube.rotate(front, True)
                        steps.append(step)
                        #print(self.cube.print_v2())
                    # bottom edge
                    elif front_face[2][1] == w:
                        #print('bottom edge')
                        # rotate front twice
                        step = self.cube.rotate(front, False)
                        steps.append(step)
                        step = self.cube.rotate(front, False)
                        steps.append(step)
                        #print(self.cube.print_v2())
                    # down face
                    elif down_face[0][1] == w:
                        #print('down face')
                        # rotate front twice
                        step = self.cube.rotate(front, False)
                        steps.append(step)
                        step = self.cube.rotate(front, False)
                        steps.append(step)
                        #print(self.cube.print_v2())
                    else:
                        #print('face rotate')
                        # rotate face and break from while loop
                        self.cube.cube_rot_left()
                        #print(self.cube.print_v2())
                        break

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

class BasicSolver(Solver):
    def __init__(self, cube):
        self.cube = cube
    def solve(self):
        pass
