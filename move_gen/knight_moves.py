# Generation of knight moves via bitboards and lookup tables

import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
# Add parent directory to path
sys.path.insert(0, parentdir) 


# Use commented code below to calculate the knight move table
# from pcs import knight
# def calc_knight_move_table():
# 	moves_by_sqr=[]
# 	for i in range(64):
# 		square_efen=[]
# 		move_set_knight=knight(color=0, sqr=i)
# 		# Set up empty board with bishop in square i
# 		for j in range(64):
# 			if j!= i:
# 				square_efen.append('u')
# 			else:
# 				square_efen.append('N')
# 		square_efen=''.join(square_efen)
# 		square_efen=square_efen+' w - - 0 1'
# 		# Get knight controlled squares
# 		_,ctrl_sqrs=move_set_knight.avl_movs(square_efen, return_ctrl_sqr=True)
# 		# Append to list
# 		moves_by_sqr.append(ctrl_sqrs)
# 	return moves_by_sqr
# knight_moves=calc_knight_move_table()

# Pre calculated move table to avoid importing pcs
knight_moves=[[10, 17], [11, 18, 16], [12, 19, 17, 8], [13, 20, 18, 9], [14, 21, 19, 10],
 [15, 22, 20, 11], [23, 21, 12], [22, 13], [2, 18, 25], [3, 19, 26, 24], [20, 27, 25, 16, 0, 4],
 [21, 28, 26, 17, 1, 5], [22, 29, 27, 18, 2, 6], [23, 30, 28, 19, 3, 7], [4, 20, 29, 31], [30, 21, 5],
 [1, 10, 26, 33], [27, 34, 32, 0, 2, 11], [28, 35, 33, 24, 8, 1, 3, 12], [29, 36, 34, 25, 9, 2, 4, 13],
 [30, 37, 35, 26, 10, 3, 5, 14], [31, 38, 36, 27, 11, 4, 6, 15], [39, 37, 28, 12, 5, 7], [38, 29, 13, 6],
 [9, 18, 34, 41], [35, 42, 40, 8, 10, 19], [36, 43, 41, 32, 16, 9, 11, 20], [37, 44, 42, 33, 17, 10, 12, 21],
 [38, 45, 43, 34, 18, 11, 13, 22], [39, 46, 44, 35, 19, 12, 14, 23], [47, 45, 36, 20, 13, 15], [46, 37, 21, 14],
 [17, 26, 42, 49], [43, 50, 48, 16, 18, 27], [44, 51, 49, 40, 24, 17, 19, 28], [45, 52, 50, 41, 25, 18, 20, 29],
 [46, 53, 51, 42, 26, 19, 21, 30], [47, 54, 52, 43, 27, 20, 22, 31], [55, 53, 44, 28, 21, 23], [54, 45, 29, 22],
 [25, 34, 50, 57], [51, 58, 56, 24, 26, 35], [52, 59, 57, 48, 32, 25, 27, 36], [53, 60, 58, 49, 33, 26, 28, 37],
 [54, 61, 59, 50, 34, 27, 29, 38], [55, 62, 60, 51, 35, 28, 30, 39], [63, 61, 52, 36, 29, 31], [62, 53, 37, 30],
 [33, 42, 58], [32, 34, 43, 59], [60, 56, 40, 33, 35, 44], [61, 57, 41, 34, 36, 45], [62, 58, 42, 35, 37, 46],
 [63, 59, 43, 36, 38, 47], [60, 44, 37, 39], [61, 45, 38], [41, 50], [40, 42, 51], [48, 41, 43, 52],
 [49, 42, 44, 53], [50, 43, 45, 54], [51, 44, 46, 55], [52, 45, 47], [53, 46]]

def gen_knight_moves(sqr, fr_bb):
	# Go through knight moves and see if enemy occupancy is 1
	pseudo_moves=[]
	for move in knight_moves[sqr]:
		#str_blocker_bb='{:064b}'.format(fr_bb)
		#if str_blocker_bb[move]!='1':
		if 1&(fr_bb>>(63-move))!=1:
			pseudo_moves.append(move)
	return pseudo_moves

