# rubix-cube

This project implements the standard solving procedure for a 3x3 rubix cube as specified [here](https://www.rubiks.com/media/guides/RBL_solve_guide_CUBE_US_5.375x8.375in_AW_27Feb2020_VISUAL.pdf).
It can currently solve 10,000 cubes in just over 30 seconds. It takes less than **5ms** to solve a single cube. It takes roughly 275 +/- 50 moves  to solve a single cube.

### More to come:
- JS web app with GUI cube editor
- photo integration (CV pipeline to accept 6 2D images as input)
- implement AI solving methods to reduce number of moves (inspiration: [here](https://github.com/benbotto/rubiks-cube-cracker))
  - [thistlethwaite algorithm](https://www.jaapsch.net/puzzles/thistle.htm) (upper bound 52  moves, takes roughly 1-2min)
    - ~6x less moves 
    - \>12,000x slower (4 orders of magnitude)
  - [korf's algorithm](https://www.cs.princeton.edu/courses/archive/fall06/cos402/papers/korfrubik.pdf) (optimal, upper bound [God's Number](https://www.cube20.org/qtm/), takes 1-2 days)
    - optimal move sequence
    - \>17,000,000x slower (7 orders of magnitude)
