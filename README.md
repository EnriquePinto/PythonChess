# PythonChess

My private python chess engine project.

To do:  
1. Board and piece objects (Done!)
2. Move generation (piece movements, legal moves, castling, check, checkmate, stalemate, repetition, 50 move rule, dead positions) (Done! Missing castling through check!)
3. Position Evaluation
4. Alpha-Beta pruning (Best First, Depth First, Breadth first, etc.)
5. Move order improvement
6. Quiescence Search
7. Iterative Deepening Depth First
8. Monte Carlo Random Tree Search (computationally viable at least for some evaluations?)
9. Transposition tables
10. Improve move generation (magic bitboards, etc.)

---

Pieces positions are a number between 0 and 63 counting from square a8, left to right, downwards, finishing on square h1
Pieces colors are represented by a bynary digit: 0=white, 1=black

Moves are understood on 2 "scopes": piece level and board level. 

* Piece level moves are a tuple of the form (target square, type of move); 
* Board level moves are also tuples, but of the form (piece object instance, piece level move). 
 
A board level move may even be further nested in a tuple which states if the move is a check or not in the following form: (board level move, is check?).

## Move types: 

0 = normal;

1 = capture; 

2 = double pawn move; 

3 = en passant; 

8/9 = castle short/long

4/5/6/7 = promotion to queen/rook/knight/bishop;

14/15/16/17 = capture and promotion to queen/rook/knight/bishop
			     
What piece is moving and from whence it is moving is not included in the piece class move output since it can be identified by the '.sqr' and '.clr' attributes

## Move priority and type identification

Identifying checks, captures, attacks:
* Checks: All checks have the "is check?" field equals "True"
* Captures: All capture moves have the first digit of move type equals 1

---

Remarks:
* Generating moves through precalculated stored bitboards and using magic bitboards and masking is considered to be the vastly superior option for move generation speed benchmarks. These generated moves need to be verified for legality (or not, see above bulletpoint) and its properties (check, capture, attack, pin, etc.) considered for move ordering reasons. Future updates may include calculation of magic bitboards and an overhaul of move generation.
