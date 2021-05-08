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





