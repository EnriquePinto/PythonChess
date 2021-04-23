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

FEN = '8/2p5/5p2/3pP3/8/1R2r2q/8/8 w - d6 0 1'
fen_pos,_,_,_,_,_ = util.read_fen(FEN)

util.print_fen(pos=FEN)

pawn1 = pcs.pawn('p1',1,util.coord2sqr('c7'))
pawn1_moves = pawn1.avl_movs(FEN)

rook1 = pcs.rook('r1',0,util.coord2sqr('b3'))
rook1_moves = rook1.avl_movs(FEN)

print(rook1_moves)

new_move = rook1.move_piece(util.expand_piece_pos(FEN), rook1_moves[0])
util.print_fen(util.compact_piece_pos(new_move), rd_pcs_only=True)

