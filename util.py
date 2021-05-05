# File containing all frequently used functions for manipulating board and square position data
# Enrique T. R. Pinto 2021

import pcs,brd

# UNICODE CHESS PIECES:
# wK = U+2654 / wQ = U+2655 / wR = U+2656 / wB = U+2657 / wN = U+2658 / wp = U+2659
# bK = U+265A / bQ = U+265B / bR = U+265C / bB = U+265D / bN = U+265E / bp = U+265F

k, q, r, b, n, p = '\u2654', '\u2655', '\u2656', '\u2657', '\u2658', '\u2659'
K, Q, R, B, N, P = '\u265A', '\u265B', '\u265C', '\u265D', '\u265E', '\u265F'

unicode_pieces = dict([('K',K), ('Q',Q), ('R',R), ('B',B), ('N',N), ('P',P),
					   ('k',k), ('q',q), ('r',r), ('b',b), ('n',n), ('p',p)])

def read_fen(pos = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):	
	"""
	Extracts the information from a FEN or eFEN code and returns:
		- Pieces positions
		- Color to move
		- Castling rights
		- En passant target square
		- Half move counter
		- Full move counter

	If input was FEN code, returns standard piece position; if it was an eFEN, returns expanded piece position
	"""
	pieces_pos, clr_to_move, castl_avl, en_pas_targ, half_mov_clk, mov_clk = pos.split(" ",6)
	return pieces_pos, clr_to_move, castl_avl, en_pas_targ, half_mov_clk, mov_clk

def expand_piece_pos(pos):
	"""
	Expands the piece position section of a fen code converting numbers into 'u', representing empty squares
	"""
	expanded_pos = ''
	for character in pos:
		if character == '/':
				pass
		else:
			# Empty square conditional
			if character.isnumeric():
				for i in range(int(character)):
					expanded_pos+='u'
			else:
				expanded_pos+=character
	return expanded_pos

def contract_piece_pos(exp_pos):
	"""
	Contracts expanded piece position converting empty squares into numbers and adding line breaks('/')
	"""
	comp_pos = ''
	empty_cnt = 0
	for i in range(64):
		if exp_pos[i]=='u':
			empty_cnt+=1
		else:
			if empty_cnt!=0:
				comp_pos+=str(empty_cnt)
				empty_cnt=0
			comp_pos+=exp_pos[i]	
		if i%8==7 and i!=63:
			if empty_cnt!=0:
				comp_pos+=str(empty_cnt)
			comp_pos+='/'
			empty_cnt=0
		if i==63 and empty_cnt!=0:
			comp_pos+=str(empty_cnt)
	return comp_pos

def fen2efen(fen):
	"""
	Returns an eFEN code from a FEN code, expanding the piece position section
	"""
	pieces_pos, clr_to_move, castl_avl, en_pas_targ, half_mov_clk, mov_clk = read_fen(fen)
	exp_piece_pos = expand_piece_pos(pieces_pos)
	return exp_piece_pos+' '+clr_to_move+' '+castl_avl+' '+en_pas_targ+' '+half_mov_clk+' '+mov_clk

def efen2fen(efen):
	"""
	Returns a FEN code from an eFEN code, contracting the piece position section
	"""
	exp_pieces_pos, clr_to_move, castl_avl, en_pas_targ, half_mov_clk, mov_clk = read_fen(efen)
	piece_pos = contract_piece_pos(exp_pieces_pos)
	return piece_pos+' '+clr_to_move+' '+castl_avl+' '+en_pas_targ+' '+half_mov_clk+' '+mov_clk


def coord2sqr(coord):
	"""
	Converts standard chess coordinates to square number (0 to 63)
	"""
	let2nbr = dict([('a',0),('b',1),('c',2),('d',3),
			   ('e',4),('f',5),('g',6),('h',7)])
	return (8-int(coord[1]))*8 + let2nbr[coord[0]]

def sqr2coord(sqr):
	"""
	Converts square number (0 to 63) to standard chess coordinates
	"""
	nbr2let = ['a','b','c','d','e','f','g','h']
	return nbr2let[sqr%8]+str((8-int(sqr/8)))

def print_fen(fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', symbol_print=False):
		"""
		Prints board in unicode from a FEN string
		"""
		pieces_pos, clr_to_move, castl_avl, en_pas_targ, half_mov_clk, mov_clk = read_fen(fen)

		print('')
		# Prints board
		for character in pieces_pos:
			# New line conditional
			if character == '/':
				print('|')
			else:
				# Empty square conditional
				if character.isnumeric():
					for i in range(int(character)):
						print('|\u0305 ',end='')
				else:
					if symbol_print:
						print('|','\u0305',unicode_pieces[character], end='', sep='')
					else:
						print('|','\u0305',character, end='', sep='')
		print('|\n \u0305  \u0305  \u0305  \u0305  \u0305  \u0305  \u0305  \u0305   ')
		print('{} moves, cstl={}, e.p.={}, mov{}, half mov{}'.format(clr_to_move, castl_avl, en_pas_targ, mov_clk, half_mov_clk))
		print('')

def translate_move(move):
	# Checks color
	if move[0].color==0:
		# Pawn
		if isinstance(move[0],pcs.pawn):
			output='P '+sqr2coord(move[0].sqr)+'->'+sqr2coord(move[1][0])
			output=output+'('+str(move[1][1])+')'
		# Rook
		elif isinstance(move[0],pcs.rook):
			output='R '+sqr2coord(move[0].sqr)+'->'+sqr2coord(move[1][0])
			output=output+'('+str(move[1][1])+')'
		# Bishop
		elif isinstance(move[0],pcs.bishop):
			output='B '+sqr2coord(move[0].sqr)+'->'+sqr2coord(move[1][0])
			output=output+'('+str(move[1][1])+')'
		# Knight
		elif isinstance(move[0],pcs.knight):
			output='N '+sqr2coord(move[0].sqr)+'->'+sqr2coord(move[1][0])
			output=output+'('+str(move[1][1])+')'
		# Queen
		elif isinstance(move[0],pcs.queen):
			output='Q '+sqr2coord(move[0].sqr)+'->'+sqr2coord(move[1][0])
			output=output+'('+str(move[1][1])+')'
		# King
		elif isinstance(move[0],pcs.king):
			output='K '+sqr2coord(move[0].sqr)+'->'+sqr2coord(move[1][0])
			output=output+'('+str(move[1][1])+')'

	else:
		# Pawn
		if isinstance(move[0],pcs.pawn):
			output='p '+sqr2coord(move[0].sqr)+'->'+sqr2coord(move[1][0])
			output=output+'('+str(move[1][1])+')'
		# Rook
		elif isinstance(move[0],pcs.rook):
			output='r '+sqr2coord(move[0].sqr)+'->'+sqr2coord(move[1][0])
			output=output+'('+str(move[1][1])+')'
		# Bishop
		elif isinstance(move[0],pcs.bishop):
			output='b '+sqr2coord(move[0].sqr)+'->'+sqr2coord(move[1][0])
			output=output+'('+str(move[1][1])+')'
		# Knight
		elif isinstance(move[0],pcs.knight):
			output='n '+sqr2coord(move[0].sqr)+'->'+sqr2coord(move[1][0])
			output=output+'('+str(move[1][1])+')'
		# Queen
		elif isinstance(move[0],pcs.queen):
			output='q '+sqr2coord(move[0].sqr)+'->'+sqr2coord(move[1][0])
			output=output+'('+str(move[1][1])+')'
		# King
		elif isinstance(move[0],pcs.king):
			output='k '+sqr2coord(move[0].sqr)+'->'+sqr2coord(move[1][0])
			output=output+'('+str(move[1][1])+')'

	return output

def white_or_black(sqr):
	"""
	Returns whether a square number is white(0) or black(1) using some clever modulo operations
	"""
	return (sqr%8+int(sqr/8))%2

def perft(depth, init_efen=fen2efen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')):
	"""
	PERFormance Test, move path enumeration function. Used for move generation debugging.
	"""
	assert depth>0, "Depth must be bigger than 0"
	nodes=0

	board_perft = brd.board()
	board_perft.set(init_efen)
	moves=board_perft.avl_movs()
	if depth==1:
		return len(moves)

	
	for move in moves:
		move_efen=board_perft.make_move(move)
		nodes+=perft(depth-1,init_efen=move_efen)
		board_perft.unmake_move()

	return nodes





# TO DO: PGN TO EFEN list converter
