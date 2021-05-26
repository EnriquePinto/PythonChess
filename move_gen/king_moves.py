# King move generation

import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
# Add parent directory to path
sys.path.insert(0, parentdir) 

# To calculate king moves per square, run commented code below
# from pcs import king
# def calc_king_move_table():
# 	moves_by_sqr=[]
# 	for i in range(64):
# 		square_efen=[]
# 		move_set_king=king(color=0, sqr=i)
# 		# Set up empty board with bishop in square i
# 		for j in range(64):
# 			if j!= i:
# 				square_efen.append('u')
# 			else:
# 				square_efen.append('K')
# 		square_efen=''.join(square_efen)
# 		square_efen=square_efen+' w - - 0 1'
# 		# Get knight controlled squares
# 		_,ctrl_sqrs=move_set_king.avl_movs(square_efen, return_ctrl_sqr=True)

# 		# Append to list
# 		moves_by_sqr.append(ctrl_sqrs)
# 	return moves_by_sqr
# king_moves=calc_king_move_table()


king_moves=[[1, 8, 9], [0, 2, 8, 9, 10], [1, 3, 9, 10, 11], [2, 4, 10, 11, 12], [3, 5, 11, 12, 13],
[4, 6, 12, 13, 14], [5, 7, 13, 14, 15], [6, 14, 15], [0, 1, 9, 16, 17], [0, 1, 2, 8, 10, 16, 17, 18],
[1, 2, 3, 9, 11, 17, 18, 19], [2, 3, 4, 10, 12, 18, 19, 20], [3, 4, 5, 11, 13, 19, 20, 21],
[4, 5, 6, 12, 14, 20, 21, 22], [5, 6, 7, 13, 15, 21, 22, 23], [6, 7, 14, 22, 23], [8, 9, 17, 24, 25],
[8, 9, 10, 16, 18, 24, 25, 26], [9, 10, 11, 17, 19, 25, 26, 27], [10, 11, 12, 18, 20, 26, 27, 28],
[11, 12, 13, 19, 21, 27, 28, 29], [12, 13, 14, 20, 22, 28, 29, 30], [13, 14, 15, 21, 23, 29, 30, 31],
[14, 15, 22, 30, 31], [16, 17, 25, 32, 33], [16, 17, 18, 24, 26, 32, 33, 34], [17, 18, 19, 25, 27, 33, 34, 35],
[18, 19, 20, 26, 28, 34, 35, 36], [19, 20, 21, 27, 29, 35, 36, 37], [20, 21, 22, 28, 30, 36, 37, 38],
[21, 22, 23, 29, 31, 37, 38, 39], [22, 23, 30, 38, 39], [24, 25, 33, 40, 41], [24, 25, 26, 32, 34, 40, 41, 42],
[25, 26, 27, 33, 35, 41, 42, 43], [26, 27, 28, 34, 36, 42, 43, 44], [27, 28, 29, 35, 37, 43, 44, 45],
[28, 29, 30, 36, 38, 44, 45, 46], [29, 30, 31, 37, 39, 45, 46, 47], [30, 31, 38, 46, 47], [32, 33, 41, 48, 49],
[32, 33, 34, 40, 42, 48, 49, 50], [33, 34, 35, 41, 43, 49, 50, 51], [34, 35, 36, 42, 44, 50, 51, 52],
[35, 36, 37, 43, 45, 51, 52, 53], [36, 37, 38, 44, 46, 52, 53, 54], [37, 38, 39, 45, 47, 53, 54, 55],
[38, 39, 46, 54, 55], [40, 41, 49, 56, 57], [40, 41, 42, 48, 50, 56, 57, 58], [41, 42, 43, 49, 51, 57, 58, 59],
[42, 43, 44, 50, 52, 58, 59, 60], [43, 44, 45, 51, 53, 59, 60, 61], [44, 45, 46, 52, 54, 60, 61, 62],
[45, 46, 47, 53, 55, 61, 62, 63], [46, 47, 54, 62, 63], [48, 49, 57], [48, 49, 50, 56, 58], [49, 50, 51, 57, 59],
[50, 51, 52, 58, 60], [51, 52, 53, 59, 61], [52, 53, 54, 60, 62], [53, 54, 55, 61, 63], [54, 55, 62]]

def gen_no_castl_king_moves(sqr, fr_bb):
	moves=[]
	str_blocker_bb='{:064b}'.format(fr_bb)
	for move in king_moves[sqr]:
		if str_blocker_bb[move]!='1':
			moves.append(move)
	return moves

def gen_kq_castl_king_moves(sqr, fr_bb, en_bb): 
	# Since king can castle, therefore no need to check color, only square!
	moves=[]

	str_castle_blocker_bb='{:064b}'.format(fr_bb|en_bb)
	#castle_blocker_bb=fr_bb|en_bb
	# Kingside
	# If white king, and no no castle blockers...
	if sqr==60 and str_castle_blocker_bb[61:63]=='00':
		moves.append(64) #64 = castle kingside
	# Else, black king and no blockers...
	elif sqr==4 and str_castle_blocker_bb[5:7]=='00':
		moves.append(64)

	# Queenside
	# If white king, and no no castle blockers...
	if sqr==60 and str_castle_blocker_bb[57:60]=='000':
		moves.append(65) #65 = castle queenside
	# Else, black king and no blockers...
	elif sqr==4 and str_castle_blocker_bb[1:4]=='000':
		moves.append(65)
	
	# Moves
	str_blocker_bb='{:064b}'.format(fr_bb)
	# White squares
	if sqr==4:
		for move in [3,5,11,12,13]:
			if str_blocker_bb[move]!='1':
				moves.append(move)
	# Black squares
	elif sqr==60:
		for move in [59,61,51,52,53]:
			if str_blocker_bb[move]!='1':
				moves.append(move)

	return moves

def gen_k_castl_king_moves(sqr, fr_bb, en_bb): 
	# Since king can castle, therefore no need to check color, only square!
	moves=[]
	str_castle_blocker_bb='{:064b}'.format(fr_bb|en_bb)
	# Kingside
	# If white king, and no no castle blockers...
	if sqr==60 and str_castle_blocker_bb[61:63]=='00':
		moves.append(64) #64 = castle kingside
	# Else, black king and no blockers...
	elif sqr==4 and str_castle_blocker_bb[5:7]=='00':
		moves.append(64)
	
	# Moves
	# White squares
	str_blocker_bb='{:064b}'.format(fr_bb)
	if sqr==4:
		for move in [3,5,11,12,13]:
			if str_blocker_bb[move]!='1':
				moves.append(move)
	# Black squares
	elif sqr==60:
		for move in [59,61,51,52,53]:
			if str_blocker_bb[move]!='1':
				moves.append(move)

	return moves

def gen_q_castl_king_moves(sqr, fr_bb, en_bb): 
	# Since king can castle, therefore no need to check color, only square!
	moves=[]
	str_castle_blocker_bb='{:064b}'.format(fr_bb|en_bb)
	# Queenside
	# If white king, and no no castle blockers...
	if sqr==60 and str_castle_blocker_bb[57:60]=='000':
		moves.append(65) #65 = castle queenside
	# Else, black king and no blockers...
	elif sqr==4 and str_castle_blocker_bb[1:4]=='000':
		moves.append(65)
	
	# Moves
	str_blocker_bb='{:064b}'.format(fr_bb)
	# White squares
	if sqr==4:
		for move in [3,5,11,12,13]:
			if str_blocker_bb[move]!='1':
				moves.append(move)
	# Black squares
	elif sqr==60:
		for move in [59,61,51,52,53]:
			if str_blocker_bb[move]!='1':
				moves.append(move)

	return moves
	