# Movegen function that generates moves based on type

from .pawn_moves import gen_pawn_moves,gen_pawn_first_moves
from .knight_moves import gen_knight_moves
from .bishop_moves import gen_bishop_moves
from .rook_moves import gen_rook_moves
from .queen_moves import gen_queen_moves
from .king_moves import gen_no_castl_king_moves, gen_kq_castl_king_moves, gen_k_castl_king_moves, gen_q_castl_king_moves

# Move legend: 0-63: target square
#			   64: kingside castle
#			   65: queenside castle
#			   a + target_square; a=100/200/300/400: simple move promotion to knight/bishop/rook/queen/rook

def unmoved_pawn_cond(sqr, clr, fr_bb, en_bb, en_pas_sqr):
	return gen_pawn_first_moves(sqr,clr,fr_bb,en_bb)

def moved_pawn_cond(sqr, clr, fr_bb, en_bb, en_pas_sqr):
	pawn_moves=gen_pawn_moves(sqr,clr,fr_bb,en_bb,en_pas_sqr)
	moves=[]
	for move in pawn_moves:
		# Add promotion if move reaches edge of board
		if 0<=move<=7 or 56<=move<=63:
			moves.extend([move+100,move+200,move+300,move+400])
		# If move doesn't reach edge of the board add the generated moves
		else:
			moves=pawn_moves
	return moves

def knight_cond(sqr, clr, fr_bb, en_bb, en_pas_sqr):
	return gen_knight_moves(sqr, fr_bb)

def bishop_cond(sqr, clr, fr_bb, en_bb, en_pas_sqr):
	return gen_bishop_moves(sqr, fr_bb, en_bb)

def rook_cond(sqr, clr, fr_bb, en_bb, en_pas_sqr):
	return gen_rook_moves(sqr, fr_bb, en_bb)

def queen_cond(sqr, clr, fr_bb, en_bb, en_pas_sqr):
	return gen_queen_moves(sqr, fr_bb, en_bb)
	
def KQking_cond(sqr, clr, fr_bb, en_bb, en_pas_sqr):
	return gen_kq_castl_king_moves(sqr, fr_bb, en_bb)

def Kking_cond(sqr, clr, fr_bb, en_bb, en_pas_sqr):
	return gen_k_castl_king_moves(sqr, fr_bb, en_bb)

def Qking_cond(sqr, clr, fr_bb, en_bb, en_pas_sqr):
	return gen_q_castl_king_moves(sqr, fr_bb, en_bb)

def king_cond(sqr, clr, fr_bb, en_bb, en_pas_sqr):
	return gen_no_castl_king_moves(sqr, fr_bb)

def gen_piece_moves(piece, sqr, fr_bb, en_bb, en_pas_sqr):
	# Color legend: 0=white, 1=black
	clr=int(piece/10)
	# Pieces legend: 0unmoved pawn, 1moved pawn, 2knight, 3bishop, 4rook, 5queen, 6KQking, 7Kking, 8Qking, 9king
	piece_type=piece%10

	# Do this with a function list to avoid conditionals
	func_list=[unmoved_pawn_cond, # Unmoved pawns
			   moved_pawn_cond,
			   knight_cond,
			   bishop_cond,
			   rook_cond,
			   queen_cond,
			   KQking_cond,
			   Kking_cond,
			   Qking_cond,
			   king_cond]

	moves=func_list[piece_type](sqr, clr, fr_bb, en_bb, en_pas_sqr)

	# # Generate moves
	# # unmoved pawn
	# if piece_type==0:
	# 	moves=gen_pawn_first_moves(sqr,clr,fr_bb,en_bb)
	# # moved pawn
	# elif piece_type==1:
	# 	pawn_moves=gen_pawn_moves(sqr,clr,fr_bb,en_bb,en_pas_sqr)
	# 	moves=[]
	# 	for move in pawn_moves:
	# 		# Add promotion if move reaches edge of board
	# 		if 0<=move<=7 or 56<=move<=63:
	# 			moves.extend([move+100,move+200,move+300,move+400])
	# 		# If move doesn't reach edge of the board add the generated moves
	# 		else:
	# 			moves=pawn_moves
	# # knight
	# elif piece_type==2:
	# 	moves=gen_knight_moves(sqr, fr_bb)
	# # bishop
	# elif piece_type==3:
	# 	moves=gen_bishop_moves(sqr, fr_bb, en_bb)
	# # rook
	# elif piece_type==4:
	# 	moves=gen_rook_moves(sqr, fr_bb, en_bb)
	# # queen
	# elif piece_type==5:
	# 	moves=gen_queen_moves(sqr, fr_bb, en_bb)
	# # KQking
	# elif piece_type==6:
	# 	moves=gen_kq_castl_king_moves(sqr, fr_bb, en_bb)
	# # Kking
	# elif piece_type==7:
	# 	moves=gen_k_castl_king_moves(sqr, fr_bb, en_bb)
	# # Qking
	# elif piece_type==8:
	# 	moves=gen_q_castl_king_moves(sqr, fr_bb, en_bb)
	# # king
	# elif piece_type==9:
	# 	moves=gen_no_castl_king_moves(sqr, fr_bb)
	
	# Return generated moves
	return [(sqr,move) for move in moves]