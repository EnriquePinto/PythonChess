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

# Pieces should be worth more towards the endgame, where they make a more significant difference
def std_eval(efen_hist, last_move):
	"""
	Takes an efen code history, and the last move and returns an evaluation for that position based on the features and the weights
	"""

	# Check if draw, win, or normal
	# Last move check?
	last_move_was_check=last_move[1]
	over=is_over(efen_hist, last_move_was_check)
	# If draw, return 0
	if over==2:
		return 0
	# If mate or win, return large value
	elif over==1:
		return 1e6


	# Actually evaluate current position
	efen=efen_hist[-1]

	# Reads efen
	exp_pos, clr_to_move, castl_avl, en_pas_targ, half_mov_clk, mov_clk = util.read_fen(efen)

	# Material count -------
	material_weight=np.array([1, 2.5, 3, 3, 5, 9])
	white_material=np.array([0,0,0,0,0,0]) #pawn, knight, w bishop, b bishop, rook, queen
	black_material=np.array([0,0,0,0,0,0])
	for i in range(len(exp_pos)):
		# White pieces
		if exp_pos[i]=='P':
			white_material[0]+=1
		elif exp_pos[i]=='N':
			white_material[1]+=1
		elif exp_pos[i]=='B':
			if util.white_or_black(i)==0:
				white_material[2]+=1
			else:
				white_material[3]+=1
		elif exp_pos[i]=='R':
			white_material[4]+=1
		elif exp_pos[i]=='Q':
			white_material[5]+=1
		# Black pieces
		elif exp_pos[i]=='p':
			black_material[0]+=1
		elif exp_pos[i]=='n':
			black_material[1]+=1
		elif exp_pos[i]=='b':
			if util.white_or_black(i)==0:
				black_material[2]+=1
			else:
				black_material[3]+=1
		elif exp_pos[i]=='r':
			black_material[4]+=1
		elif exp_pos[i]=='q':
			black_material[5]+=1
	material_score=material_weight@(white_material-black_material)

	# Mobility (move count function input) -------
	eval_brd=brd.board()
	eval_brd.set(efen)
	move_count1=len(eval_brd.avl_movs())
	# Change current player to move to get mobility
	prev_clr_to_move=clr_to_move
	if clr_to_move=='w':
		clr_to_move='b'
	else:
		clr_to_move='w'
	eval_brd.set(exp_pos+' '+clr_to_move+' '+castl_avl+' '+en_pas_targ+' '+half_mov_clk+' '+mov_clk)
	move_count2=len(eval_brd.avl_movs())
	# If white was to move originally:
	if clr_to_move=='b':
		mob_score=move_count1-move_count2
		clr_to_move=prev_clr_to_move
	# If black was to move:
	else:
		mob_score=move_count2-move_count1
		clr_to_move=prev_clr_to_move

	# Controlled squares (Space) -------
	w_ctrl,b_ctrl=eval_brd.board_control()
	control_score=sum(w_ctrl-b_ctrl)

	# Development (don't move same piece twice in the opening?)

	# Positional adders (doubled pawns, blocked pawns, isolated pawns, knights on edge)

	# Tempo bonus
	if clr_to_move=='w':
		tempo_bonus=0.2
	else:
		tempo_bonus=-0.2

	# General scoring weight: [material, mobility, control, tempo]
	score_weight=np.array([1, 0.1, 0.1, 1])
	score = score_weight@np.array([material_score, mob_score, control_score, tempo_bonus])

	return score
	