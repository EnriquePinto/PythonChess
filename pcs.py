# File containing all piece and board classes definitions
# All piece classes contain the following methods:
# 	__init__: starts up the piece name, color, and square
#   move_piece: from an expanded FEN and a legal move returns an expanded FEN (eFEN) for a position in which such move was made
#	avl_movs: from a FEN code returns all legal moves for that piece (first verifying the FEN code agrees with the local piece position)


# Note: make "move_piece" method receive a complete FEN and return a complete eFEN!

import util

class board:

	def set(self, fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
		# Expand FEN and instantiate a piece in each position
		# Use piece_list with piece objects
		pass

# A board object is to be used in every piece object instance to identify legal moves and checks!
# 	-The actual board object where moves will be made is to be called 'main_board'
# 	-The local instance of a board object in a piece object is to be called 'local_board'

# Each piece move output is a tuple: (target square, type of move, is check?)
# Move types: 0 = normal; 1 = capture; 2 = double pawn move; 3 = en passant; 
#			  4/5/6/7 = promotion to queen/rook/knight/bishop; 14/15/16/17 = capture and promotion to queen/rook/knight/bishop
#			  8/9 = castle short/long

class pawn:

	def __init__(self, name: str, color: bin, sqr: int):
		assert 0<=sqr<=63 and isinstance(sqr,int), "PC_POS_ERR: Piece position must be an integer between 0 and 63."
		self.name = name
		self.color = color
		self.sqr = sqr

	def move_piece(self, move, efen):
		"""
		Makes the described move from a FEN code, returns expanded FEN (eFEN) of move made
		"""

		# Interprets the input EFEN code
		exp_pos, clr_to_move, castl_avl, en_pas_targ, half_mov_clk, mov_clk = util.read_fen(efen)

		# Checks if no turn mismatch occured (white piece can only move on white turn)
		if self.color == 0:
			assert clr_to_move=='w', "MOV_CLR_ERR: Wrong color to move, this piece is not allowed to move in the current turn"
		else:
			assert clr_to_move=='b', "MOV_CLR_ERR: Wrong color to move, this piece is not allowed to move in the current turn"

		# Empty previous piece position
		new_exp_pos=[char for char in exp_pos]
		new_exp_pos[self.sqr]='u'

		# Fill new piece position
		# If piece is white, fill with white piece
		if self.color==0:
			# Checks if move is not a promotion
			# i.e. either normal, capture, en passant; capture promotions and simple promotions are of a different type (4,5,6,7,14,15,16,17)
			if move[1]==0 or move[1]==1 or move[1]==3:
				new_exp_pos[move[0]]='P'
			# If it is a promotion, which promotion?
			else:
				# Promotion to queen
				if move[1]==4 or move[1]==14:
					new_exp_pos[move[0]]='Q'
				# Promotion to rook
				elif move[1]==5 or move[1]==15:
					new_exp_pos[move[0]]='R'
				# Promotion to knight
				elif move[1]==6 or move[1]==16:
					new_exp_pos[move[0]]='N'
				# Promotion to bishop
				elif move[1]==7 or move[1]==17:
					new_exp_pos[move[0]]='B'
		# If it is black, fill with black piece
		else:
			# Checks if move is not a promotion
			if move[1]==0 or move[1]==1 or move[1]==3:
				new_exp_pos[move[0]]='p'
			# If it is a promotion, which promotion?
			else:
				# Promotion to queen
				if move[1]==4 or move[1]==14:
					new_exp_pos[move[0]]='q'
				# Promotion to rook
				elif move[1]==5 or move[1]==15:
					new_exp_pos[move[0]]='r'
				# Promotion to knight
				elif move[1]==6 or move[1]==16:
					new_exp_pos[move[0]]='n'
				# Promotion to bishop
				elif move[1]==7 or move[1]==17:
					new_exp_pos[move[0]]='b'

		# If En Passant, remove captured pawn
		if move[1]==3:
			if self.color==0:
				new_exp_pos[move[0]+8]='u'
			else:
				new_exp_pos[move[0]-8]='u'

		# Synthesizes new expanded position
		new_exp_pos = ''.join(new_exp_pos)

		# Defines new color to move
		if clr_to_move=='w':
			new_clr_to_move='b'
		else:
			new_clr_to_move='w'

		# Checks new castling availability
		# If no one can castle now, no castling can be available in the future
		if castl_avl=='-':
			new_castl_avl='-'
		else:
			# A pawn move can only remove castling rights if it captures a rook
			# Check by color case by case
			if self.color==0:
				# No white pawn move can remove white castling rights and vice versa (only temporarily prevent castling, i.e. leaving castling route in check)
				# Therefore white pawn moves can only change black's castling rights (e.g. by capturing a rook)
				# If black can castle kingside and white captured kingside rook, remove black kingside castling rights
				if 'k' in castl_avl and move[0]==7 and move[1] in [1,4,5,6,7,14,15,16,17]:
					new_castl_avl = castl_avl.replace('k','')
				# If black can castle queenside and white captured queenside rook, remove black queenside castling rights
				elif 'q' in castl_avl and move[0]==0 and move[1] in [1,4,5,6,7,14,15,16,17]:
					new_castl_avl = castl_avl.replace('q','')
				# If no capture was made, preserve castling rights
				else:
					new_castl_avl = castl_avl
			else:
				# If white can castle kingside and black captured kingside rook, remove white kingside castling rights
				if 'K' in castl_avl and move[0]==63 and move[1] in [1,4,5,6,7,14,15,16,17]:
					new_castl_avl = castl_avl.replace('K','')
				# If white can castle queenside and black captured queenside rook, remove white queenside castling rights
				elif 'Q' in castl_avl and move[0]==56 and move[1] in [1,4,5,6,7,14,15,16,17]:
					new_castl_avl = castl_avl.replace('Q','')
				# If no capture was made, preserve castling rights
				else:
					new_castl_avl = castl_avl

		# If double pawn move, add en passant target
		if move[1]==2:
			# Check color
			if self.color==0:
				new_en_pas_targ=util.sqr2coord(move[0]+8)
			else:
				new_en_pas_targ=util.sqr2coord(move[0]-8)
		# En passant only happens immediately after a double pawn move
		else:
			new_en_pas_targ='-'

		# Increments half move clock if no pawn advance or capture has been made
		# Every pawn move resets hal move clock
		new_half_mov_clk=str(0)

		# Increments move clock after a black move
		if clr_to_move=='b':
			new_mov_clk=str(int(mov_clk)+1)
		# If white move, keep move clock as is
		else:
			new_mov_clk=mov_clk

		new_exp_fen = new_exp_pos+' '+new_clr_to_move+' '+new_castl_avl+' '+new_en_pas_targ+' '+new_half_mov_clk+' '+new_mov_clk

		return new_exp_fen

	def avl_movs(self, fen):
		pieces_pos, clr_to_move, castl_avl, en_pas_targ, half_mov_clk, mov_clk = util.read_fen(fen)
		exp_pos = util.expand_piece_pos(pieces_pos)
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
				en_pas_tarq_sqr = util.coord2sqr(en_pas_targ)
				# Only allow en passant captures of black en passant squares
				if 16<=en_pas_tarq_sqr<=23:
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
				en_pas_tarq_sqr = util.coord2sqr(en_pas_targ)
				# Only allow en passant captures of white en passant squares
				if 40<=en_pas_tarq_sqr<=47:
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

	def move_piece(self, exp_pos, move):
		# Empty previous piece position
		new_exp_pos=[char for char in exp_pos]
		new_exp_pos[self.sqr]='u'

		# Fill new piece position
		# If piece is white, fill with white piece
		if self.color==0:
			new_exp_pos[move[0]]='R'
		# If it is black, fill with black piece
		else:
			new_exp_pos[move[0]]='r'

		new_exp_pos = ''.join(new_exp_pos)
		return new_exp_pos

	def avl_movs(self, fen):
		pieces_pos, clr_to_move, castl_avl, en_pas_targ, half_mov_clk, mov_clk = util.read_fen(fen)
		exp_pos = util.expand_piece_pos(pieces_pos)
		# Asserts that local piece parameters agree with with input position
		if self.color==0:
			assert exp_pos[self.sqr]=='R', "PC_POS_MISMATCH_ERR: Position does not agree with local piece type and location parameters."
		else:
			assert exp_pos[self.sqr]=='r', "PC_POS_MISMATCH_ERR: Position does not agree with local piece type and location parameters."

		avl_mov_list = []

		# Generate white moves if white (necessary distinction since one cannot capture one's own piece)
		if self.color==0:
			# UPWARDS MOVES
			# Maximum number of squares to move is always 1 to 7 (8 squares is outside the board and 0 squares is not a move)
			for i in range(1,8):
				# Stop if outside black edge board range
				target_sqr = self.sqr-8*i
				if target_sqr<0:
					break
				else:
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['p','n','b','r','Q','k']:
						avl_mov_list.append((target_sqr,1))
						break
			# DOWNWARDS MOVES
			for i in range(1,8):
				# Stop if outside white edge board range
				target_sqr = self.sqr+8*i
				if target_sqr>63:
					break
				else:
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						avl_mov_list.append((target_sqr,1))
						break
			# KINGSIDEWARDS MOVES
			for i in range(1,8):
				# Stop if outside kingside edge board range
				target_sqr = self.sqr+i
				if (target_sqr)%8==0:
					break
				else:
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						avl_mov_list.append((target_sqr,1))
						break
			# QUEENSIDEWARDS MOVES
			for i in range(1,8):
				# Stop if outside kingside edge board range
				target_sqr = self.sqr-i
				if (target_sqr)%8==7:
					break
				else:
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						avl_mov_list.append((target_sqr,1))
						break

		# Generate black moves if black
		else:
			# UPWARDS MOVES
			for i in range(1,8):
				# Stop if outside black edge board range
				target_sqr = self.sqr-8*i
				if target_sqr<0:
					break
				else:
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						avl_mov_list.append((target_sqr,1))
						break
			# DOWNWARDS MOVES
			for i in range(1,8):
				# Stop if outside white edge board range
				target_sqr = self.sqr+8*i
				if target_sqr>63:
					break
				else:
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						avl_mov_list.append((target_sqr,1))
						break
			# KINGSIDEWARDS MOVES
			for i in range(1,8):
				# Stop if outside kingside edge board range
				target_sqr = self.sqr+i
				if (target_sqr)%8==0:
					break
				else:
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						avl_mov_list.append((target_sqr,1))
						break
			# QUEENSIDEWARDS MOVES
			for i in range(1,8):
				# Stop if outside kingside edge board range
				target_sqr = self.sqr-i
				if (target_sqr)%8==7:
					break
				else:
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						avl_mov_list.append((target_sqr,1))
						break

		return avl_mov_list


class bishop:

	def __init__(self, name, color, sqr):
		assert 0<=sqr<=63 and isinstance(sqr,int), "PC_POS_ERR: Piece position must be an integer between 0 and 63."
		self.name = name
		self.color = color
		self.sqr = sqr

	def move_piece(self, exp_pos, move):
		# Empty previous piece position
		new_exp_pos=[char for char in exp_pos]
		new_exp_pos[self.sqr]='u'

		# Fill new piece position
		# If piece is white, fill with white piece
		if self.color==0:
			new_exp_pos[move[0]]='B'
		# If it is black, fill with black piece
		else:
			new_exp_pos[move[0]]='b'

		new_exp_pos = ''.join(new_exp_pos)
		return new_exp_pos


# avl_movs workflow: 
#	1. Interpret the FEN
#	2. Checks if local piece color and square agrees with FEN
#	3. Checks piece color
#	4. Generate moves for that color
#	5. Make each move on a local board object and look for checks and ilegal moves
#	6. Mark "is check?" move tuple field and remove ilegal moves
#	7. Return legal moves


# Each piece move output is a tuple: (target square, type of move, is check?)
# Move types: 0 = normal; 1 = capture; 2 = double pawn move; 3 = en passant; 
#			  4/5/6/7 = promotion to queen/rook/knight/bishop; 14/15/16/17 = capture and promotion to queen/rook/knight/bishop
#			  8/9 = castle short/long
