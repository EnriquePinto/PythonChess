# Evaluation functions file
# Make a function checking if it is either stalemate or mate


import numpy as np
import brd, util, pcs

def is_over(efen_hist, last_move_was_check):
	"""
	Game end verifying function, given an array of EFENs (the history of the game), returns if position is a draw (2), mate(1), or normal position(0).
	The EFEN hist list is used for repetition checking only.
	Only checks the last position for the 50 move rule and threefold repetition.
	"""
	exp_pos_v=[]
	clr_to_move_v=[] 
	castl_avl_v=[]
	en_pas_targ_v=[]
	half_mov_clk_v=[]
	mov_clk_v=[]

	# Makes a list out of every entry of each EFEN
	for efen in efen_hist:
		exp_pos, clr_to_move, castl_avl, en_pas_targ, half_mov_clk, mov_clk = util.read_fen(efen)
		# Appends to the lists
		exp_pos_v.append(exp_pos)
		clr_to_move_v.append(clr_to_move) 
		castl_avl_v.append(castl_avl)
		en_pas_targ_v.append(en_pas_targ)
		half_mov_clk_v.append(half_mov_clk)
		mov_clk_v.append(mov_clk)

	# Checks draw types in sequence, from the least computationally expensive to the most expensive
	# DRAW BY 50 MOVE RULE - Check draw by 50 move rule ----------
	if int(half_mov_clk_v[-1])>=50:
		return 2

	# INSUFICIENT MATERIAL - Check the following piece combinations
	# 	1.king versus king
	#	2.king and bishop versus king
	#	3.king and knight versus king
	#	4.king and bishop versus king and bishop with the bishops on the same color.

	#piece_count=[pawn, rook, w sqr bishop, b sqr bishop, knight, queen, king]
	test_brd = brd.board()
	test_brd.set(efen_hist[-1])
	# king vs king
	if test_brd.w_piece_count==[0,0,0,0,0,0,1] and test_brd.b_piece_count==[0,0,0,0,0,0,1]:
		return 2
	# Knight and king vs king (both ways)
	elif ((test_brd.w_piece_count==[0,0,0,0,1,0,1] and test_brd.b_piece_count==[0,0,0,0,0,0,1]) or 
		 (test_brd.w_piece_count==[0,0,0,0,0,0,1] and test_brd.b_piece_count==[0,0,0,0,1,0,1])):
		return 2
	# King and bishop vs king
	elif ((test_brd.w_piece_count==[0,0,1,0,0,0,1] and test_brd.b_piece_count==[0,0,0,0,0,0,1]) or 
		 (test_brd.w_piece_count==[0,0,0,1,0,0,1] and test_brd.b_piece_count==[0,0,0,0,0,0,1]) or
		 (test_brd.w_piece_count==[0,0,0,0,0,0,1] and test_brd.b_piece_count==[0,0,1,0,0,0,1]) or 
		 (test_brd.w_piece_count==[0,0,0,0,0,0,1] and test_brd.b_piece_count==[0,0,0,1,0,0,1])):
		return 2
	# Symmetrical king and bishop
	elif ((test_brd.w_piece_count==[0,0,1,0,0,0,1] and test_brd.b_piece_count==[0,0,1,0,0,0,1]) or
		 (test_brd.w_piece_count==[0,0,0,1,0,0,1] and test_brd.b_piece_count==[0,0,0,1,0,0,1])):
		return 2
	

	# DRAW BY REPETITION - Check for threefold repetition ----------
	# First, creates a vector 'pos_vec' with relevant information for checking for threefold repetition in each position
	pos_vec=[]
	for i in range(len(efen_hist)):
		pos=exp_pos_v[i]+clr_to_move_v[i]+castl_avl_v[i]+en_pas_targ_v[i]
		pos_vec.append(pos)
	# Second, we count how many times the last position appears
	counter=0
	for pos in pos_vec:
		if pos==pos_vec[-1]:
			counter+=1
		# Return '2' if current position occured more than thrice
		if counter>=3:	
			return 2

	# DRAW BY STALEMATE - Check last position for available moves
	# mate_brd = brd.board()
	# mate_brd.set(efen_hist[-1])
	n_of_avl_movs=test_brd.avl_movs(check_legality=True, extra_output=True)[2] # Output: (legal_moves, ilegal_moves, how many legal moves)
	if n_of_avl_movs==0:
		if last_move_was_check:
			return 1
		else:
			return 2


	# If all draw types and win conditions failed, return '0' (normal position)
	return 0

def mate_stalemate_or_normal(efen):
	"""
	'Hard' checks a position for mate or stalemate, instead of relying on an input informing whether last move was check.
	Returns if position is a draw (2), mate(1), or normal position(0)
	"""
	mate_brd = brd.board()
	mate_brd.set(efen)
	n_of_avl_movs=mate_brd.avl_movs(check_legality=True, extra_output=True)[2] # Output: (legal_moves, ilegal_moves, how many legal moves)
	
	# Verifying if it is mate if there are no moves
	if n_of_avl_movs==0:
		w_ctrl, b_ctrl=mate_brd.board_control()
		# If it is white to move, see if white king is attacked
		if mate_brd.clr_to_move=='w':
			# Loop through pieces and look for the king
			for piece in mate_brd.white_pieces:
				if isinstance(piece,pcs.king):
					# Check if king square is controlled by white
					if b_ctrl[piece.sqr]>0:
						return 1
					else:
						return 2
		# If it is black to move, see if black king is attacked
		else:
			# Loop through pieces and look for the king
			for piece in mate_brd.black_pieces:
				if isinstance(piece,pcs.king):
					# Check if king square is controlled by white
					if w_ctrl[piece.sqr]>0:
						return 1
					else:
						return 2
	# If there are moves, normal position!
	else:
		return 0



# Pieces swhould be worth more towards the endgame, where they make a more significant difference
def std_eval(efen, move_count):
	"""
	Takes an efen code and returns an evaluation for that position based on the features and the weights
	"""
	# Reads efen
	exp_pos, clr_to_move, castl_avl, en_pas_targ, half_mov_clk, mov_clk = util.read_fen(efen)

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
	