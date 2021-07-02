"""
   These constants are used for indexing the cube and applying actions to the cube.
"""

# UP = "U"
UP = 23
# DOWN = "D"
DOWN = 22
# LEFT = "L"
LEFT = 3
# RIGHT = "R"
RIGHT = 21
# FRONT = "F"
FRONT = 5
# BACK = "B"
BACK = 6
# UP_PRIME = "U'"
UP_PRIME = 7
# DOWN_PRIME = "D'"
DOWN_PRIME = 20
# LEFT_PRIME = "L'"
LEFT_PRIME = 9
# RIGHT_PRIME = "R'"
RIGHT_PRIME = 10
# FRONT_PRIME = "F'"
FRONT_PRIME = 11
# BACK_PRIME = "B'"
BACK_PRIME = 12

"""
    3D rotation across X, Y, Z axis.
"""
# Z_ROT = "Z"
Z_ROT = 13
# Z_ROT_PRIME = "Z'"
Z_ROT_PRIME = 14
# Y_ROT = "Y"
Y_ROT = 15
# Y_ROT_PRIME = "Y'"
Y_ROT_PRIME = 19
# X_ROT = "X"
X_ROT = 17
# X_ROT_PRIME = "X'"
X_ROT_PRIME = 18

"""
    Colors.
"""
# YELLOW ="y"
YELLOW = 1
# WHITE = "w"
WHITE = 2
# RED =  "r"
RED = 4
# ORANGE  ="o"
ORANGE = 8
# GREEN  = "g"
GREEN = 16
# BLUE  = "b"
BLUE = 32

"""
    Positional constants. Make indexing easier.
"""
TOP_RIGHT = (0,2)
TOP_MIDDLE = (0,1)
TOP_LEFT = (0,0)

MIDDLE_RIGHT = (1,2)
CENTER = (1,1)
MIDDLE_LEFT = (1,0)

BOTTOM_RIGHT  = (2,2)
BOTTOM_MIDDLE = (2,1)
BOTTOM_LEFT = (2,0)



"""
    A dictionary that can be used to get the string representations for the given constant.
"""

TO_STRING = {
    UP: "U",
    UP_PRIME: "U'",
    DOWN: "D",
    DOWN_PRIME: "D'",
    LEFT: "L",
    LEFT_PRIME: "L'",
    RIGHT: "R",
    RIGHT_PRIME: "R'",
    FRONT: "F",
    FRONT_PRIME: "F'",
    BACK: "B",
    BACK_PRIME: "B'",
    Z_ROT: "Z",
    Z_ROT_PRIME: "Z'",
    Y_ROT: "Y",
    Y_ROT_PRIME: "Y'",
    X_ROT: "X",
    X_ROT_PRIME: "X'",
    YELLOW: "y",
    WHITE: "w",
    RED: "r",
    ORANGE: "o",
    BLUE: "b",
    GREEN: "g"
}


"""
    A dictionary that can be used to get the inverse actions that undo the specified action.
"""
INVERSE = {

    UP: UP_PRIME,
    UP_PRIME: UP,
    DOWN: DOWN_PRIME,
    DOWN_PRIME: DOWN,
    LEFT: LEFT_PRIME,
    LEFT_PRIME: LEFT,
    RIGHT: RIGHT,
    RIGHT_PRIME: RIGHT_PRIME,
    FRONT: FRONT_PRIME,
    FRONT_PRIME: FRONT,
    BACK: BACK_PRIME,
    BACK_PRIME: BACK,
    Z_ROT: Z_ROT_PRIME,
    Z_ROT_PRIME: Z_ROT,
    Y_ROT: Y_ROT_PRIME,
    Y_ROT_PRIME: Y_ROT,
    X_ROT: X_ROT_PRIME,
    X_ROT_PRIME: X_ROT,
}


"""
    A dictionary that can be used to get the opposite color.
"""
OPPOSITE = {
    YELLOW: WHITE,
    WHITE: YELLOW,
    RED: ORANGE,
    ORANGE: RED,
    BLUE: GREEN,
    GREEN: BLUE
}
