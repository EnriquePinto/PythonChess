# Generating queen moves from bishop moves and rook moves
from move_gen.bishop_moves import gen_bishop_moves
from move_gen.rook_moves import gen_rook_moves

def gen_queen_moves(sqr, fr_bb, en_bb):
	b_moves=gen_bishop_moves(sqr,fr_bb,en_bb)
	r_movs=gen_rook_moves(sqr,fr_bb,en_bb)
	return b_moves+r_movs


