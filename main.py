# Main file for private Python based chess engine test
# Enrique T. R. Pinto 2021
# To do: 1.Board and piece objects 
#		 2.Board printing function 
# 		 3.Move generation (piece movements, legal moves, pawn moves, castling, en passant, promotion, check, checkmate, stalemate, repetition, 50 move rule, dead positions)
#		 4.Position Evaluation
#		 5.Alpha-Beta pruning (Best First, Depth First, Breadth first, etc.)
#		 6.Move order improvement
#		 7.Quiescence Search
#		 8.Iterative Deepening Depth First


# Imports

import util
import pcs
# Pieces positions are a number between 0 and 63 counting from square a8, left to right, downwards, finishing on square h1
# Pieces colors are represented by a bynary digit: 0=white, 1=black

# Each piece move output is a tuple: (target square, type of move, is check?)
# Move types: 0 = normal; 1 = capture; 2 = double pawn move; 3 = en passant; 
#			  4/5/6/7 = promotion to queen/rook/knight/bishop; 14/15/16/17 = capture and promotion to queen/rook/knight/bishop
#			  8/9 = castle short/long
# What piece is moving and from whence it is moving is not included in the piece class move output since it can be identified by the '.sqr' and '.name' attributes


# Identifying checks, captures, attacks:
#	Checks: All checks have the "is check?" field equals "True"
# 	Captures: All capture moves have the first digit of move type equals 1
#	Attacks: TO DO!

FEN = 'r3k2r/8/2B2B2/8/8/2b2b2/8/R3K2R b KQkq - 0 1'
fen_pos,_,_,_,_,_ = util.read_fen(FEN)

util.print_fen(FEN)

# pawn1 = pcs.pawn('p1',1,util.coord2sqr('g2'))
# pawn1_moves = pawn1.avl_movs(FEN)

rook1 = pcs.rook('r1',1,util.coord2sqr('a8'))
rook1_moves = rook1.avl_movs(FEN)

bishop1 = pcs.bishop('b1',1,util.coord2sqr('f3'))
bishop1_moves = bishop1.avl_movs(FEN)

print(bishop1_moves)

new_move = bishop1.move_piece(bishop1_moves[-3], util.fen2efen(FEN))

util.print_fen(util.efen2fen(new_move))

