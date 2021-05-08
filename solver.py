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
        self.solve_white_corners()

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
                self.cube.apply_seq(["F", "F"])
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
        def get_faces():
            return self.cube.get_face_from_orient(front) , self.cube.get_face_from_orient(up), self.cube.get_face_from_orient(right), self.cube.get_face_from_orient(left), self.cube.get_face_from_orient(down)

        def move_corner_in_between():
            #corner is in bottom layer, so we need to rotate down until it is in between
            #its two corresponding centers
            front_face, top_face, right_face, left_face, down_face = get_faces()
            front_color = None

            if front_face[2][2] == w:
                front_color = down_face[0][2]
            if right_face[2][0] == w:
                front_color = front_face[2][2]
            if down_face[0][2] == w:
                front_color = right_face[2][0]
            while front_face[1][1] != front_color:
                self.cube.apply_seq(["D", "LL"])
                front_face, top_face, right_face, left_face, down_face = get_faces()

        
        def bring_corner_up():
            front_face, top_face, right_face, left_face, down_face = get_faces()
            #corner piece must be in bottom right corner of front face, so we can bring it up
            if front_face[2][2] == w:
                self.cube.apply_seq(["D'", "R'", "D", "R"])
            if right_face[2][0] == w:
                
                self.cube.apply_seq(["LL", "D", "L", "D'", "L'", "RR"])
            if down_face[0][2] == w:
                self.cube.apply_seq(["F", "D'", "F'", "D", "D"])
                bring_corner_up()

        #rotate face up twice so that white cross is on up face
        self.cube.apply_seq(["UU", "UU"])
        
        #for each corner
        while not self.check_white_corners():
            front_face, top_face, right_face, left_face, down_face = get_faces()

            right_corner = top_face[2][2] == w and front_face[0][2] == front_face[1][1] and right_face[0][0] == right_face[1][1]

            if top_face[2][2] == w or front_face[0][2] == w or right_face[0][0] == w:
                if not right_corner:
                    #bring her down into bottom right corner
                    self.cube.apply_seq(["R'", "D'", "R", "D"])
                    move_corner_in_between()
                    bring_corner_up()
            else:
                # check bottom layer

                for _ in range(4):
                    front_face, top_face, right_face, left_face, down_face = get_faces()
                    if front_face[2][2] == w or right_face[2][0] == w or down_face[0][2] == w:
                        #found a corner
                        #get it in between the proper center pieces
                        move_corner_in_between()
                        bring_corner_up()
                    else:
                      self.cube.apply_seq(["D"])
     
            self.cube.apply_seq(["LL"])

    def check_white_corners(self):
        '''
        Checks if step 3 is complete assuming orientation, white top, yellow bottom
        '''
        # assert self.check_daisy() and self.check_white_cross()
        # assert self.cube.orient_dict[up] == w and self.cube.orient_dict[down] == y
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
        # print(sum(solved))
        return sum(solved) == len(solved) and white_solved



