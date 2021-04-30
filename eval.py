# Evaluation functions file

import numpy as np
import brd
import util


# ==> Also needs the position history to check if any position happened 3 times and declare draw by repetition

# Pieces swhould be worth more towards the endgame, where they make a more significant difference

def std_eval(efen, move_count):
	"""
	Takes an efen code and returns an evaluation for that position based on the features and the weights
	"""
	# Reads efen
	exp_pos, clr_to_move, castl_avl, en_pas_targ, half_mov_clk, mov_clk = util.read_fen(efen)

	# Check draw by 50 move rule


	# Material count
	white_material=[0,0,0,0,0] #pawn, knight, bishop, rook, queen
	black_material=[0,0,0,0,0]
	for piece in exp_pos:
		# White pieces
		if piece=='P':
			white_material[0]+=1
		elif piece=='N':
			white_material[1]+=1
		elif piece=='B':
			white_material[2]+=1
		elif piece=='R':
			white_material[3]+=1
		elif piece=='Q':
			white_material[4]+=1
		# Black pieces
		elif piece=='p':
			black_material[0]+=1
		elif piece=='n':
			black_material[1]+=1
		elif piece=='b':
			black_material[2]+=1
		elif piece=='r':
			black_material[3]+=1
		elif piece=='q':
			black_material[4]+=1

	# Mobility (move count function input)

	# Controlled squares (Space)


	# Development (don't move same piece twice in the opening?)

	# Positional adders (doubled pawns, blocked pawns, isolated pawns, knights on edge)

	# Tempo bonus?


	pass
	