# rubix-cube

This project implements the standard solving procedure for a 3x3 rubix cube as specified [here](https://www.rubiks.com/media/guides/RBL_solve_guide_CUBE_US_5.375x8.375in_AW_27Feb2020_VISUAL.pdf).
It can currently solve 10,000 cubes in just over 30 seconds. It takes less than **5ms** to solve a single cube. It takes roughly 300 +/- 50 moves on average to solve.

## More to come:
- JS web app with GUI cube editor
- photo integration (CV pipeline to accept images as input)
- implement AI solving methods to reduce number of moves 
  - thistlethwaite algorithm (upper bound 52 quarter turn moves, takes roughly 1-2min)
  - korf's algorithm (optimal, upper bound 26 moves, takes 0-2 days)
