# PythonChess (Discontinued)

---
NOTICE: This project has been discontinued as a shot on making a de facto chess engine on Python. While Python is a worthy language in its own right for many applications regarding data analysis and machine learning, it is not an effective choice for the brute force computations required in the traditional paradigms of chess engines.
Therefore, this project is now regarded as a framework for a future chess engine written in C++
---


My private python chess engine project.

To do:  
1. Board and piece objects (Done!)
2. Move generation (promotion moves missing in make_move!)
3. Position Evaluation
4. Alpha-Beta pruning (Best First, Depth First, Breadth first, etc.)
5. Move order improvement
6. Quiescence Search
7. Iterative Deepening Depth First
8. Monte Carlo Random Tree Search (computationally viable at least for some evaluations?)
9. Transposition tables

---

Pieces positions are a number between 0 and 63 counting from square a8, left to right, downwards, finishing on square h1
Pieces colors are represented by a bynary digit: 0=white, 1=black

Pieces by number:
* WHITE: 00 unmoved pawn, 01 moved pawn, 02 knight, 03 bishop, 04 rook, 05 queen, 06 KQking, 07 Kking, 08 Qking, 09 king
* BLACK: 10 unmoved pawn, 11 moved pawn, 12 knight, 13 bishop, 14 rook, 15 queen, 16 KQking, 17 Kking, 18 Qking, 19 king
* '': Empty

Moves are a tuple (origin square, target square). Special moves are codified with a target square larger than 63.
Move legend: 
* 0-63: target square
* 64: kingside castle
* 65: queenside castle
* a + target_square; a=100/200/300/400: promotion to knight/bishop/rook/queen/rook


State is a list of "frames" encoded as:
1. List of size 64 of all squares and their occupancy (castling is encoded in the king piece ) TO DO: USE SOME HASHING: ZOBRIST, BCH, ...
2. Color to move
3. En passant square
4. Half-move count (to facilitate 50 move rule detection)
Move count is unnecessary since it can be achieved from the list size count.
Also store vector sup_data of (w_pieces, b_pieces, w_bb, b_bb) history
