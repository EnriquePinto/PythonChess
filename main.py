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


# UNICODE CHESS PIECES:
# wK = U+2654 / wQ = U+2655 / wR = U+2656 / wB = U+2657 / wN = U+2658 / wp = U+2659
# bK = U+265A / bQ = U+265B / bR = U+265C / bB = U+265D / bN = U+265E / bp = U+265F

k, q, r, b, n, p = '\u2654', '\u2655', '\u2656', '\u2657', '\u2658', '\u2659'
K, Q, R, B, N, P = '\u265A', '\u265B', '\u265C', '\u265D', '\u265E', '\u265F'

unicode_pieces = dict([('K',K), ('Q',Q), ('R',R), ('B',B), ('N',N), ('P',P),
					   ('k',k), ('q',q), ('r',r), ('b',b), ('n',n), ('p',p)])

def read_fen(pos = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):	
	"""
	Extracts the information from a FEN code and returns:
		- Pieces positions
		- Color to move
		- Castling rights
		- En passant target square
		- Half move counter
		- Full move counter
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

def compact_piece_pos(exp_pos):
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

def print_fen(pos = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', rd_pcs_only = False, symbol_print=False):
		"""
		Prints board in unicode from a FEN string
		"""
		# Adds the option of printing only board and pieces
		if not rd_pcs_only:
			pieces_pos, clr_to_move, castl_avl, en_pas_targ, half_mov_clk, mov_clk = read_fen(pos)
		else:
			pieces_pos = pos
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
		if not rd_pcs_only:
			print('{} moves, cstl={}, e.p.={}, mov{}'.format(clr_to_move, castl_avl, en_pas_targ, mov_clk))
		print('')


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


class board:

	def set(self, fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
		# Expand FEN and instantiate a piece in each position
		# Use piece_list with piece objects
		pass

# A board object is to be used in every piece object instance to identify legal moves and checks!
# 	-The actual board object where moves will be made is to be called 'main_board'
# 	-The local instance of a board object in a piece object is to be called 'local_board'

class pawn:

	def __init__(self, name: str, color: bin, sqr: int):
		assert 0<=sqr<=63 and isinstance(sqr,int), "PC_POS_ERR: Piece position must be an integer between 0 and 63."
		self.name = name
		self.color = color
		self.sqr = sqr

	def move_piece(self, exp_pos, move):
		# Empty previous piece position
		new_exp_pos=[char for char in exp_pos]
		new_exp_pos[self.sqr]='u'

		# Fill new piece position
		if self.color==0:
			new_exp_pos[move[0]]='P'
		else:
			new_exp_pos[move[0]]='p'

		# If En Passant, remove captured pawn
		if move[1]==3:
			if self.color==0:
				new_exp_pos[move[0]+8]='u'
			else:
				new_exp_pos[move[0]-8]='u'

		new_exp_pos = ''.join(new_exp_pos)
		return new_exp_pos

	def avl_movs(self, fen):
		pieces_pos, clr_to_move, castl_avl, en_pas_targ, half_mov_clk, mov_clk = read_fen(fen)
		exp_pos = expand_piece_pos(pieces_pos)
		# Asserts that local piece parameters agree with with input position
		if self.color==0:
			assert exp_pos[self.sqr]=='P', "PC_POS_MISMATCH_ERR: Position does not agree with local piece type and location parameters."
		else:
			assert exp_pos[self.sqr]=='p', "PC_POS_MISMATCH_ERR: Position does not agree with local piece type and location parameters."
		# If pawn is white, move upwards in the board (decreases number)
		# If pawn is black, move downwards in the board (increases number)

		# TO DO: Go through all other pieces in current position and verify if there are discovered checks
		# 	It will be more convenient to check if a square is attacked (instead of the king), i.e. see if king is in an attacked square to look for checks,
		# 	since it is a more flexible construct and allows for easier legal castling verification
		
		avl_mov_list = []

		# Generate white pawn moves if white
		if self.color==0:
			# PROMOTION CHECK
			# Checks piece position to see if any advance move (simple moves or captures) will result in promotion
			# If move is a promotion, generate promotion moves
			if 8<=self.sqr<=15:
				# SIMPLE MOVES
				# Checks if normal move is occupied by piece and adds move if square is free
				if exp_pos[self.sqr-8]=='u':
					for i in [4,5,6,7]:
						avl_mov_list.append((self.sqr-8, i, ))
				
				# CAPTURE MOVES
				# Checks if there are available captures and adds captures to available mov list
				# Exception for edges of board
				# Queenside exception
				if self.sqr%8==0:	
					if exp_pos[self.sqr-7] not in ['u','K','Q','B','N','P']:
						for i in [14,15,16,17]:
							avl_mov_list.append((self.sqr-7, i, ))

				# Kingside exception	
				elif (self.sqr+1)%8==0:
					if exp_pos[self.sqr-9] not in ['u','K','Q','B','N','P']:
						for i in [14,15,16,17]:
							avl_mov_list.append((self.sqr-9, i, ))

				# Ordinary captures
				else:
					if exp_pos[self.sqr-7] not in ['u','K','Q','B','N','P']:
						for i in [14,15,16,17]:
							avl_mov_list.append((self.sqr-7, i, ))
					if exp_pos[self.sqr-9] not in ['u','K','Q','B','N','P']:
						for i in [14,15,16,17]:
							avl_mov_list.append((self.sqr-9, i, ))

			# If move is not a promotion, generate normal moves
			else:
				# SIMPLE MOVES
				# Checks if normal move is occupied by piece and adds move if square is free
				if exp_pos[self.sqr-8]=='u':
					# If move is not a promotion, generate simple move
					avl_mov_list.append((self.sqr-8, 0, ))

				# CAPTURE MOVES
				# Checks if there are available captures and adds captures to available mov list
				# Exception for edges of board
				# Queenside exception
				if self.sqr%8==0:
					if exp_pos[self.sqr-7] not in ['u','K','Q','B','N','P']:
						avl_mov_list.append((self.sqr-7, 1, ))

				# Kingside exception	
				elif (self.sqr+1)%8==0:
					if exp_pos[self.sqr-9] not in ['u','K','Q','B','N','P']:
						avl_mov_list.append((self.sqr-9, 1, ))

				# Ordinary captures
				else:
					if exp_pos[self.sqr-7] not in ['u','K','Q','B','N','P']:
						avl_mov_list.append((self.sqr-7, 1, ))
					if exp_pos[self.sqr-9] not in ['u','K','Q','B','N','P']:
						avl_mov_list.append((self.sqr-9, 1, ))

				# DOUBLE MOVES
				# Checks if pawn is in any of the initial squares
				if 48<=self.sqr<=55:
					# Checks if pawn double move is blocked, adds move if it isn't
					if exp_pos[self.sqr-16]=='u' and exp_pos[self.sqr-8]=='u':
						avl_mov_list.append((self.sqr-16, 2, ))

				# EN PASSANT
				en_pas_tarq_sqr = coord2sqr(en_pas_targ)
				# Exception for edges of board
				# Queenside exception
				if self.sqr%8==0:
					if self.sqr-7==en_pas_tarq_sqr:
						avl_mov_list.append((self.sqr-7, 3, ))

				# Kingside exception	
				elif (self.sqr+1)%8==0:
					if self.sqr-9==en_pas_tarq_sqr:
						avl_mov_list.append((self.sqr-9, 3, ))

				# Ordinary captures
				else:
					if self.sqr-7==en_pas_tarq_sqr:
						avl_mov_list.append((self.sqr-7, 3, ))
					if self.sqr-9==en_pas_tarq_sqr:
						avl_mov_list.append((self.sqr-9, 3, ))
		
		# Generate black pawn moves if black
		else:
			# PROMOTION CHECK
			# Checks piece position to see if any advance move (simple moves or captures) will result in promotion
			# If move is a promotion, generate promotion moves
			if 48<=self.sqr<=55:
				# SIMPLE MOVES
				# Checks if normal move is occupied by piece and adds move if square is free
				if exp_pos[self.sqr+8]=='u':
					for i in [4,5,6,7]:
						avl_mov_list.append((self.sqr+8, i, ))
				
				# CAPTURE MOVES
				# Checks if there are available captures and adds captures to available mov list
				# Exception for edges of board
				# Queenside exception
				if self.sqr%8==0:	
					if exp_pos[self.sqr+9] not in ['u','k','q','b','n','p']:
						for i in [14,15,16,17]:
							avl_mov_list.append((self.sqr+9, i, ))

				# Kingside exception	
				elif (self.sqr+1)%8==0:
					if exp_pos[self.sqr+7] not in ['u','k','q','b','n','p']:
						for i in [14,15,16,17]:
							avl_mov_list.append((self.sqr+7, i, ))

				# Ordinary captures
				else:
					if exp_pos[self.sqr+7] not in ['u','k','q','b','n','p']:
						for i in [14,15,16,17]:
							avl_mov_list.append((self.sqr+7, i, ))
					if exp_pos[self.sqr+9] not in ['u','k','q','b','n','p']:
						for i in [14,15,16,17]:
							avl_mov_list.append((self.sqr+9, i, ))

			# If move is not a promotion, generate normal moves
			else:
				# SIMPLE MOVES
				# Checks if normal move is occupied by piece and adds move if square is free
				if exp_pos[self.sqr+8]=='u':
					# If move is not a promotion, generate simple move
					avl_mov_list.append((self.sqr+8, 0, ))

				# CAPTURE MOVES
				# Checks if there are available captures and adds captures to available mov list
				# Exception for edges of board
				# Queenside exception
				if self.sqr%8==0:
					if exp_pos[self.sqr+9] not in ['u','k','q','b','n','p']:
						avl_mov_list.append((self.sqr+9, 1, ))

				# Kingside exception	
				elif (self.sqr+1)%8==0:
					if exp_pos[self.sqr+7] not in ['u','k','q','b','n','p']:
						avl_mov_list.append((self.sqr+7, 1, ))

				# Ordinary captures
				else:
					if exp_pos[self.sqr+7] not in ['u','k','q','b','n','p']:
						avl_mov_list.append((self.sqr+7, 1, ))
					if exp_pos[self.sqr+9] not in ['u','k','q','b','n','p']:
						avl_mov_list.append((self.sqr+9, 1, ))

				# DOUBLE MOVES
				# Checks if pawn is in any of the initial squares
				if 8<=self.sqr<=15:
					# Checks if pawn double move is blocked, adds move if it isn't
					if exp_pos[self.sqr+16]=='u' and exp_pos[self.sqr+8]=='u':
						avl_mov_list.append((self.sqr+16, 2, ))

				# EN PASSANT
				en_pas_tarq_sqr = coord2sqr(en_pas_targ)
				# Exception for edges of board
				# Queenside exception
				if self.sqr%8==0:
					if self.sqr+9==en_pas_tarq_sqr:
						avl_mov_list.append((self.sqr+9, 3, ))

				# Kingside exception	
				elif (self.sqr+1)%8==0:
					if self.sqr+7==en_pas_tarq_sqr:
						avl_mov_list.append((self.sqr+7, 3, ))

				# Ordinary captures
				else:
					if self.sqr+7==en_pas_tarq_sqr:
						avl_mov_list.append((self.sqr+7, 3, ))
					if self.sqr+9==en_pas_tarq_sqr:
						avl_mov_list.append((self.sqr+9, 3, ))

		# Go through generated move list and see if:
		#  1. It is a discovered check;
		#  2. It is an ilegal move (would leave own king in check)



				
		return avl_mov_list
	

class rook:

	def __init__(self, name, color, sqr):
		assert 0<=sqr<=63 and isinstance(sqr,int), "PC_POS_ERR: Piece position must be an integer between 0 and 63."
		self.name = name
		self.color = color
		self.sqr = sqr

	def avl_movs(self, fen):
		pieces_pos, clr_to_move, castl_avl, en_pas_targ, half_mov_clk, mov_clk = read_fen(fen)
		exp_pos = expand_piece_pos(pieces_pos)
		# Asserts that local piece parameters agree with with input position
		if self.color==0:
			assert exp_pos[self.sqr]=='P', "PC_POS_MISMATCH_ERR: Position does not agree with local piece type and location parameters."
		else:
			assert exp_pos[self.sqr]=='p', "PC_POS_MISMATCH_ERR: Position does not agree with local piece type and location parameters."







print_fen(pos='8/1p1pp3/3R1N2/4B3/5Pp1/8/2p1p3/1R6 w - f3 0 1')

pawn1 = pawn('p1',1,coord2sqr('g4'))
pawn1_moves = pawn1.avl_movs('8/1p1pp3/3R1N2/4B3/5Pp1/8/2p1p3/1R6 w - f3 0 1')
print(pawn1_moves)

new_move = pawn1.move_piece(expand_piece_pos('8/1p1pp3/3R1N2/4B3/5Pp1/8/2p1p3/1R6'), pawn1_moves[1])
print_fen(compact_piece_pos(new_move), rd_pcs_only=True)

