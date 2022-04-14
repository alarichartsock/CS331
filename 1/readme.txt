To run:
As an example: running with input file name of inputfile.txt, a goal file name of goalfile.txt, a mode of dfs, and an output file of outfile.txt

(!!IMPORTANT!!) You need to run this file with Python 3. 

    $ python3 main.py inputfile.txt goalfile.txt dfs outfile.txt

Possible choices for mode:
    bfs
    dfs
    iddfs
    astar

Example start file:
0,0,0
3,3,1

Example goal file:
3,3,1
0,0,0

Example command line output:
Goal reached, Left Bank: 0 chicken, 0 wolf, 0 boat. Right Bank: 3 chicken, 3 wolf, 1 boat

GOAL DEPTH: 11
15 nodes expanded

Example output file once file is ran:
Left Bank: 3 chicken, 3 wolf, 1 boat. Right Bank: 0 chicken, 0 wolf, 0 boat
Left Bank: 2 chicken, 2 wolf, 0 boat. Right Bank: 1 chicken, 1 wolf, 1 boat
Left Bank: 3 chicken, 2 wolf, 1 boat. Right Bank: 0 chicken, 1 wolf, 0 boat
Left Bank: 3 chicken, 0 wolf, 0 boat. Right Bank: 0 chicken, 3 wolf, 1 boat

(!!IMPORTANT!!) Please note that in every instance, the starting bank will be the left bank. Also 

Please email me at hartsoca@oregonstate.edu for any support or assistance
