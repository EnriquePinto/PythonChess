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
#		 9.Zobrist hashing for positions, transposition tables, etc.


# Imports

import util, pcs, brd, evaluation

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

#start_fen='rnbqk1nr/pppp1ppp/4p3/8/1b1P4/2N5/PPP1PPPP/R1BQKBNR w KQkq - 0 1'

normal_efen=util.fen2efen('3k4/8/4P3/2Q5/8/6B1/3N4/1K1R2R1 w - - 0 1')
mate_efen=util.fen2efen('k7/8/8/8/8/8/R7/1R5K b - - 0 1')
stalemate_efen=util.fen2efen('k7/8/1Q6/8/8/8/8/7K b - - 0 1')
mov50_efen=util.fen2efen('3k4/8/4P3/2Q5/8/6B1/3N4/1K1R2R1 w - - 50 100')


util.print_fen(util.efen2fen(normal_efen))

board1 = brd.board()
board1.set(normal_efen)

# 1st move
mov_list1=board1.avl_movs(check_legality=True)
board1.print_avl_moves()
#new_move1=board1.make_move(mov_list1[0])
# util.print_fen(util.efen2fen(new_move1))


print(evaluation.is_over([mov50_efen],True))
#print(evaluation.mate_stalemate_or_normal(stalemate_efen))

print('- - - - - -')

# # 2nd move
# mov_list2=board1.avl_movs()
# board1.print_avl_moves()
# board1.print_control()
# new_move2=board1.make_move(mov_list2[13])
# util.print_fen(util.efen2fen(new_move2))

# # 3rd move
# mov_list3=board1.avl_movs()
# board1.print_avl_moves()
# new_move3=board1.make_move(mov_list3[1])
# util.print_fen(util.efen2fen(new_move3))




