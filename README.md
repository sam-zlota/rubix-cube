# rubix-cube

This project implements the standard solving procedure for a 3x3 rubix cube as specified [here](https://www.rubiks.com/media/guides/RBL_solve_guide_CUBE_US_5.375x8.375in_AW_27Feb2020_VISUAL.pdf).
For a scrambled cube, it takes roughly 3.5 ms to solve (depending on computational resources) and the solution sequence is on average 245 quarter-turn moves.

Here are statistics for 10,000 cubes(100 scrambles each):

<img src="https://user-images.githubusercontent.com/57266808/118036600-c46ec180-b33a-11eb-83e4-204bed3fa321.png" width="666" height="1000"/>



### More to come:
- JS web app with GUI cube editor.
- photo integration (CV pipeline to accept 6 2D images as input).
- implement AI solving methods. Because these have been implemented [before](https://github.com/benbotto/rubiks-cube-cracker)), we look to improve their upper bounds in time.
  - [thistlethwaite algorithm](https://www.jaapsch.net/puzzles/thistle.htm) (upper bound 52  moves, takes roughly 1-2min)
    - ~6x less moves 
    - ~10,000x slower (4 orders of magnitude)
  - [korf's algorithm](https://www.cs.princeton.edu/courses/archive/fall06/cos402/papers/korfrubik.pdf) (optimal, upper bound [God's Number](https://www.cube20.org/qtm/), takes many hours to days)
    - optimal move sequence
    - ~10,000,000x slower (7 orders of magnitude)
