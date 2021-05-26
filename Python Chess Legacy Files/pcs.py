# File containing all piece and board classes definitions
# All piece classes contain the following methods:
# 	__init__: starts up the piece name, color, and square
#   move_piece: from an eFEN and a legal move returns eFEN for a position in which such move was made
#	avl_movs: from a eFEN code returns all legal moves for that piece (first verifying the FEN code agrees with the local piece position)




import util

class pawn:

	def __init__(self, color: bin, sqr: int):
		assert 0<=sqr<=63 and isinstance(sqr,int), "PC_POS_ERR: Piece position must be an integer between 0 and 63."
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
			if move[1] in [0,1,2,3]:
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
			if move[1] in [0,1,2,3]:
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

	def avl_movs(self, efen, return_ctrl_sqr=False):
		exp_pos, clr_to_move, castl_avl, en_pas_targ, half_mov_clk, mov_clk = util.read_fen(efen)

		# Asserts that local piece parameters agree with with input position
		if self.color==0:
			assert exp_pos[self.sqr]=='P', "PC_POS_MISMATCH_ERR: Position does not agree with local piece type and location parameters."
		else:
			assert exp_pos[self.sqr]=='p', "PC_POS_MISMATCH_ERR: Position does not agree with local piece type and location parameters."
		# If pawn is white, move upwards in the board (decreases number)
		# If pawn is black, move downwards in the board (increases number)		
		avl_mov_list = []
		controlled_squares = [] # list of all controlled squares
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
					if exp_pos[self.sqr-7] not in ['u','K','Q','R','B','N','P']:
						for i in [14,15,16,17]:
							avl_mov_list.append((self.sqr-7, i, ))
					controlled_squares.append(self.sqr-7)


				# Kingside exception	
				elif (self.sqr+1)%8==0:
					if exp_pos[self.sqr-9] not in ['u','K','Q','R','B','N','P']:
						for i in [14,15,16,17]:
							avl_mov_list.append((self.sqr-9, i, ))
					controlled_squares.append(self.sqr-9)

				# Ordinary captures
				else:
					if exp_pos[self.sqr-7] not in ['u','K','Q','R','B','N','P']:
						for i in [14,15,16,17]:
							avl_mov_list.append((self.sqr-7, i, ))
					controlled_squares.append(self.sqr-7)

					if exp_pos[self.sqr-9] not in ['u','K','Q','R','B','N','P']:
						for i in [14,15,16,17]:
							avl_mov_list.append((self.sqr-9, i))
					controlled_squares.append(self.sqr-9)

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
					if exp_pos[self.sqr-7] not in ['u','K','Q','R','B','N','P']:
						avl_mov_list.append((self.sqr-7, 1, ))
					controlled_squares.append(self.sqr-7)

				# Kingside exception	
				elif (self.sqr+1)%8==0:
					if exp_pos[self.sqr-9] not in ['u','K','Q','R','B','N','P']:
						avl_mov_list.append((self.sqr-9, 1, ))
					controlled_squares.append(self.sqr-9)

				# Ordinary captures
				else:
					if exp_pos[self.sqr-7] not in ['u','K','Q','R','B','N','P']:
						avl_mov_list.append((self.sqr-7, 1, ))
					controlled_squares.append(self.sqr-7)

					if exp_pos[self.sqr-9] not in ['u','K','Q','R','B','N','P']:
						avl_mov_list.append((self.sqr-9, 1, ))
					controlled_squares.append(self.sqr-9)

				# DOUBLE MOVES
				# Checks if pawn is in any of the initial squares
				if 48<=self.sqr<=55:
					# Checks if pawn double move is blocked, adds move if it isn't
					if exp_pos[self.sqr-16]=='u' and exp_pos[self.sqr-8]=='u':
						avl_mov_list.append((self.sqr-16, 2, ))

				# EN PASSANT
				if en_pas_targ!='-':
					en_pas_targ_sqr = util.coord2sqr(en_pas_targ)
					# Only allow en passant captures of black en passant squares
					if 16<=en_pas_targ_sqr<=23:
						# Exception for edges of board
						# Queenside exception
						if self.sqr%8==0:
							if self.sqr-7==en_pas_targ_sqr:
								avl_mov_list.append((self.sqr-7, 3, ))

						# Kingside exception	
						elif (self.sqr+1)%8==0:
							if self.sqr-9==en_pas_targ_sqr:
								avl_mov_list.append((self.sqr-9, 3, ))

						# Ordinary captures
						else:
							if self.sqr-7==en_pas_targ_sqr:
								avl_mov_list.append((self.sqr-7, 3, ))
							if self.sqr-9==en_pas_targ_sqr:
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
					if exp_pos[self.sqr+9] not in ['u','k','q','r','b','n','p']:
						for i in [14,15,16,17]:
							avl_mov_list.append((self.sqr+9, i, ))
					controlled_squares.append(self.sqr+9)

				# Kingside exception	
				elif (self.sqr+1)%8==0:
					if exp_pos[self.sqr+7] not in ['u','k','q','r','b','n','p']:
						for i in [14,15,16,17]:
							avl_mov_list.append((self.sqr+7, i, ))
					controlled_squares.append(self.sqr+7)

				# Ordinary captures
				else:
					if exp_pos[self.sqr+7] not in ['u','k','q','r','b','n','p']:
						for i in [14,15,16,17]:
							avl_mov_list.append((self.sqr+7, i, ))
					controlled_squares.append(self.sqr+7)

					if exp_pos[self.sqr+9] not in ['u','k','q','r','b','n','p']:
						for i in [14,15,16,17]:
							avl_mov_list.append((self.sqr+9, i, ))
					controlled_squares.append(self.sqr+9)

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
					if exp_pos[self.sqr+9] not in ['u','k','q','r','b','n','p']:
						avl_mov_list.append((self.sqr+9, 1, ))
					controlled_squares.append(self.sqr+9)

				# Kingside exception	
				elif (self.sqr+1)%8==0:
					if exp_pos[self.sqr+7] not in ['u','k','q','r','b','n','p']:
						avl_mov_list.append((self.sqr+7, 1, ))
					controlled_squares.append(self.sqr+9)

				# Ordinary captures
				else:
					if exp_pos[self.sqr+7] not in ['u','k','q','r','b','n','p']:
						avl_mov_list.append((self.sqr+7, 1, ))
					controlled_squares.append(self.sqr+7)

					if exp_pos[self.sqr+9] not in ['u','k','q','r','b','n','p']:
						avl_mov_list.append((self.sqr+9, 1, ))
					controlled_squares.append(self.sqr+9)

				# DOUBLE MOVES
				# Checks if pawn is in any of the initial squares
				if 8<=self.sqr<=15:
					# Checks if pawn double move is blocked, adds move if it isn't
					if exp_pos[self.sqr+16]=='u' and exp_pos[self.sqr+8]=='u':
						avl_mov_list.append((self.sqr+16, 2, ))

				# EN PASSANT
				if en_pas_targ!='-':
					en_pas_targ_sqr = util.coord2sqr(en_pas_targ)
					# Only allow en passant captures of white en passant squares
					if 40<=en_pas_targ_sqr<=47:
						# Exception for edges of board
						# Queenside exception
						if self.sqr%8==0:
							if self.sqr+9==en_pas_targ_sqr:
								avl_mov_list.append((self.sqr+9, 3, ))

						# Kingside exception	
						elif (self.sqr+1)%8==0:
							if self.sqr+7==en_pas_targ_sqr:
								avl_mov_list.append((self.sqr+7, 3, ))

						# Ordinary captures
						else:
							if self.sqr+7==en_pas_targ_sqr:
								avl_mov_list.append((self.sqr+7, 3, ))
							if self.sqr+9==en_pas_targ_sqr:
								avl_mov_list.append((self.sqr+9, 3, ))
		if return_ctrl_sqr:
			return avl_mov_list, controlled_squares
		else:
			return avl_mov_list

class rook:

	def __init__(self, color, sqr):
		assert 0<=sqr<=63 and isinstance(sqr,int), "PC_POS_ERR: Piece position must be an integer between 0 and 63."
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
			new_exp_pos[move[0]]='R'
		# If it is black, fill with black piece
		else:
			new_exp_pos[move[0]]='r'

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
			# Check by color
			if self.color==0:
				# White rooks remove castling rights by moving the first time and by capturing oponent rook
				# Rights are the same in case no conditional is triggered
				new_castl_avl = castl_avl
				# Moving rook the first time (any rook move removes castling rights if there are any)
				# Kingside rook first move 
				if 'K' in castl_avl and self.sqr==63:
					new_castl_avl = new_castl_avl.replace('K','')
				# Queenside rook first move
				elif 'Q' in castl_avl and self.sqr==56:
					new_castl_avl = new_castl_avl.replace('Q','')

				# Capturing oponent rook
				# If black can castle kingside and white captured kingside rook, remove black kingside castling rights
				if 'k' in castl_avl and move[0]==7 and move[1]==1:
					new_castl_avl = new_castl_avl.replace('k','')
				# If black can castle queenside and white captured queenside rook, remove black queenside castling rights
				elif 'q' in castl_avl and move[0]==0 and move[1]==1:
					new_castl_avl = new_castl_avl.replace('q','')

			else:
				# Black rooks remove castling rights by moving the first time and by capturing oponent rook
				# Rights are the same in case no conditional is triggered
				new_castl_avl = castl_avl
				# Moving rook the first time (any rook move removes castling rights if there are any)
				# Kingside rook first move 
				if 'k' in castl_avl and self.sqr==7:
					new_castl_avl = new_castl_avl.replace('k','')
				# Queenside rook first move
				elif 'q' in castl_avl and self.sqr==0:
					new_castl_avl = new_castl_avl.replace('q','')

				# Capturing oponent rook
				# If white can castle kingside and black captured kingside rook, remove white kingside castling rights
				if 'K' in castl_avl and move[0]==63 and move[1]==1:
					new_castl_avl = new_castl_avl.replace('K','')
				# If white can castle queenside and black captured queenside rook, remove white queenside castling rights
				elif 'Q' in castl_avl and move[0]==56 and move[1]==1:
					new_castl_avl = new_castl_avl.replace('Q','')

		# Any rook move removes en passant target
		new_en_pas_targ='-'

		# Increments half move clock if no pawn advance or capture has been made
		# Checks if capture happened
		if move[1]==1:
			new_half_mov_clk=str(0)
		# No capture or pawn move increments half move counter
		else:
			new_half_mov_clk=str(int(half_mov_clk)+1)

		# Increments move clock after a black move
		if clr_to_move=='b':
			new_mov_clk=str(int(mov_clk)+1)
		# If white move, keep move clock as is
		else:
			new_mov_clk=mov_clk

		new_exp_fen = new_exp_pos+' '+new_clr_to_move+' '+new_castl_avl+' '+new_en_pas_targ+' '+new_half_mov_clk+' '+new_mov_clk

		return new_exp_fen

	def avl_movs(self, efen, return_ctrl_sqr=False):
		exp_pos, clr_to_move, castl_avl, en_pas_targ, half_mov_clk, mov_clk = util.read_fen(efen)

		# Asserts that local piece parameters agree with with input position
		if self.color==0:
			assert exp_pos[self.sqr]=='R', "PC_POS_MISMATCH_ERR: Position does not agree with local piece type and location parameters."
		else:
			assert exp_pos[self.sqr]=='r', "PC_POS_MISMATCH_ERR: Position does not agree with local piece type and location parameters."

		avl_mov_list = []
		controlled_squares = []

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
					controlled_squares.append(target_sqr)
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						avl_mov_list.append((target_sqr,1,))
						break

			# DOWNWARDS MOVES
			for i in range(1,8):
				# Stop if outside white edge board range
				target_sqr = self.sqr+8*i
				if target_sqr>63:
					break
				else:
					controlled_squares.append(target_sqr)
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						avl_mov_list.append((target_sqr,1,))
						break

			# KINGSIDEWARDS MOVES
			for i in range(1,8):
				# Stop if outside kingside edge board range
				target_sqr = self.sqr+i
				if (target_sqr)%8==0:
					break
				else:
					controlled_squares.append(target_sqr)
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						avl_mov_list.append((target_sqr,1,))
						break

			# QUEENSIDEWARDS MOVES
			for i in range(1,8):
				# Stop if outside kingside edge board range
				target_sqr = self.sqr-i
				if (target_sqr)%8==7:
					break
				else:
					controlled_squares.append(target_sqr)
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						avl_mov_list.append((target_sqr,1,))
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
					controlled_squares.append(target_sqr)
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						avl_mov_list.append((target_sqr,1,))
						break

			# DOWNWARDS MOVES
			for i in range(1,8):
				# Stop if outside white edge board range
				target_sqr = self.sqr+8*i
				if target_sqr>63:
					break
				else:
					controlled_squares.append(target_sqr)
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						avl_mov_list.append((target_sqr,1,))
						break

			# KINGSIDEWARDS MOVES
			for i in range(1,8):
				# Stop if outside kingside edge board range
				target_sqr = self.sqr+i
				if (target_sqr)%8==0:
					break
				else:
					controlled_squares.append(target_sqr)
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						avl_mov_list.append((target_sqr,1,))
						break

			# QUEENSIDEWARDS MOVES
			for i in range(1,8):
				# Stop if outside kingside edge board range
				target_sqr = self.sqr-i
				if (target_sqr)%8==7:
					break
				else:
					controlled_squares.append(target_sqr)
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						avl_mov_list.append((target_sqr,1,))
						break

		if return_ctrl_sqr:
			return avl_mov_list, controlled_squares
		else:
			return avl_mov_list

class bishop:

	def __init__(self, color, sqr):
		assert 0<=sqr<=63 and isinstance(sqr,int), "PC_POS_ERR: Piece position must be an integer between 0 and 63."
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
			new_exp_pos[move[0]]='B'
		# If it is black, fill with black piece
		else:
			new_exp_pos[move[0]]='b'

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
			# Check by color
			if self.color==0:
				# White bishops remove castling rights by capturing oponent rook
				# Rights are the same in case no conditional is triggered
				new_castl_avl = castl_avl
				# Capturing oponent rook
				# If black can castle kingside and white captured kingside rook, remove black kingside castling rights
				if 'k' in castl_avl and move[0]==7 and move[1]==1:
					new_castl_avl = new_castl_avl.replace('k','')
				# If black can castle queenside and white captured queenside rook, remove black queenside castling rights
				elif 'q' in castl_avl and move[0]==0 and move[1]==1:
					new_castl_avl = new_castl_avl.replace('q','')

			else:
				# Black bishops remove castling rights by capturing oponent rook
				# Rights are the same in case no conditional is triggered
				new_castl_avl = castl_avl
				# Capturing oponent rook
				# If white can castle kingside and black captured kingside rook, remove white kingside castling rights
				if 'K' in castl_avl and move[0]==63 and move[1]==1:
					new_castl_avl = new_castl_avl.replace('K','')
				# If white can castle queenside and black captured queenside rook, remove white queenside castling rights
				elif 'Q' in castl_avl and move[0]==56 and move[1]==1:
					new_castl_avl = new_castl_avl.replace('Q','')

		# Any bishop move removes en passant target
		new_en_pas_targ='-'

		# Increments half move clock if no pawn advance or capture has been made
		# Checks if capture happened
		if move[1]==1:
			new_half_mov_clk=str(0)
		# No capture or pawn move increments half move counter
		else:
			new_half_mov_clk=str(int(half_mov_clk)+1)

		# Increments move clock after a black move
		if clr_to_move=='b':
			new_mov_clk=str(int(mov_clk)+1)
		# If white move, keep move clock as is
		else:
			new_mov_clk=mov_clk

		new_exp_fen = new_exp_pos+' '+new_clr_to_move+' '+new_castl_avl+' '+new_en_pas_targ+' '+new_half_mov_clk+' '+new_mov_clk

		return new_exp_fen

	def avl_movs(self, efen, return_ctrl_sqr=False):
		exp_pos, clr_to_move, castl_avl, en_pas_targ, half_mov_clk, mov_clk = util.read_fen(efen)
		
		# Asserts that local piece parameters agree with with input position
		if self.color==0:
			assert exp_pos[self.sqr]=='B', "PC_POS_MISMATCH_ERR: Position does not agree with local piece type and location parameters."
		else:
			assert exp_pos[self.sqr]=='b', "PC_POS_MISMATCH_ERR: Position does not agree with local piece type and location parameters."
		
		avl_mov_list = []
		controlled_squares = []

		# Generate white moves if white
		if self.color==0:
			# BLACK-KINGSIDE DIAGONAL MOVES
			for i in range(1,8):
				target_sqr = self.sqr-7*i
				# Stop if reached top or side edge
				if target_sqr<0 or target_sqr%8==0:
					break
				else:
					controlled_squares.append(target_sqr)
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						avl_mov_list.append((target_sqr,1,))
						break

			# BLACK-QUEENSIDE DIAGONAL MOVES
			for i in range(1,8):
				target_sqr = self.sqr-9*i
				# Stop if reached top or side edge
				if target_sqr<0 or target_sqr%8==7:
					break
				else:
					controlled_squares.append(target_sqr)
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						avl_mov_list.append((target_sqr,1,))
						break

			# WHITE-KINGSIDE DIAGONAL MOVES
			for i in range(1,8):
				target_sqr = self.sqr+9*i
				# Stop if reached top or side edge
				if target_sqr>63 or target_sqr%8==0:
					break
				else:
					controlled_squares.append(target_sqr)
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						avl_mov_list.append((target_sqr,1,))
						break

			# WHITE-QUEENSIDE DIAGONAL MOVES
			for i in range(1,8):
				target_sqr = self.sqr+7*i
				# Stop if reached top or side edge
				if target_sqr>63 or target_sqr%8==7:
					break
				else:
					controlled_squares.append(target_sqr)
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						avl_mov_list.append((target_sqr,1,))
						break

		# Generate black moves if black			
		else:
			# BLACK-KINGSIDE DIAGONAL MOVES
			for i in range(1,8):
				target_sqr = self.sqr-7*i
				# Stop if reached top or side edge
				if target_sqr<0 or target_sqr%8==0:
					break
				else:
					controlled_squares.append(target_sqr)
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						avl_mov_list.append((target_sqr,1,))
						break

			# BLACK-QUEENSIDE DIAGONAL MOVES
			for i in range(1,8):
				target_sqr = self.sqr-9*i
				# Stop if reached top or side edge
				if target_sqr<0 or target_sqr%8==7:
					break
				else:
					controlled_squares.append(target_sqr)
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						avl_mov_list.append((target_sqr,1,))
						break

			# WHITE-KINGSIDE DIAGONAL MOVES
			for i in range(1,8):
				target_sqr = self.sqr+9*i
				# Stop if reached top or side edge
				if target_sqr>63 or target_sqr%8==0:
					break
				else:
					controlled_squares.append(target_sqr)
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						avl_mov_list.append((target_sqr,1,))
						break

			# WHITE-QUEENSIDE DIAGONAL MOVES
			for i in range(1,8):
				target_sqr = self.sqr+7*i
				# Stop if reached top or side edge
				if target_sqr>63 or target_sqr%8==7:
					break
				else:
					controlled_squares.append(target_sqr)
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						avl_mov_list.append((target_sqr,1,))
						break

		if return_ctrl_sqr:
			return avl_mov_list, controlled_squares
		else:
			return avl_mov_list

class knight:

	# KNIGHT MOVE LIST

	# Knight move position legend:
	#
	#  2   3  	| 1 => -10 ; 2 => -17 ; 3 => -15 ; 4 => -6 
	# 1     4	| 5 => +10 ; 6 => +17 ; 7 => +15 ; 8 => +6
	#    N 		|
	# 8     5	|
	#  7   6 	|
	#
	# A3 B5 C5 C5 C5 C5 B6 A4
	# B4 C4 D3 D3 D3 D3 C6 B7
	# C3 D2 E_ E_ E_ E_ D4 C7
	# C3 D2 E_ E_ E_ E_ D4 C7
	# C3 D2 E_ E_ E_ E_ D4 C7
	# C3 D2 E_ E_ E_ E_ D4 C7
	# B3 C2 D1 D1 D1 D1 C8 B8
	# A2 B2 C1 C1 C1 C1 B1 A1
	# 
	# Move count legend:
	# A/B/C/D/E = 2/3/4/6/8 moves
	#
	# A1: 1,2                   | A2: 3,4                   | A3: 5,6                   | A4: 7,8
	# B1: 1,2,3   | B2: 2,3,4   | B3: 3,4,5   | B4: 4,5,6   | B5: 5,6,7   | B6: 6,7,8   | B7: 7,8,1   | B8: 8,1,2
	# C1: 1,2,3,4 | C2: 2,3,4,5 | C3: 3,4,5,6 | C4: 4,5,6,7 | C5: 5,6,7,8 | C6: 6,7,8,1 | C7: 7,8,1,2 | C8: 8,1,2,3
	# D1: 8,1,2,3,4,5           | D2: 2,3,4,5,6,7           | D3: 4,5,6,7,8,1           | D4: 3,6,7,8,1,2
	# E: 1,2,3,4,5,6,7,8
	#
	# 25 types of squares in total

	# Defines a list of pseudo-legal knight moves by square
	knight_mov_list = []
	for i in range(64):
		# A1
		if i==63:
			moves=[-10,-17]
		# A2
		elif i==56:
			moves=[-15,-6]
		# A3
		elif i==0:
			moves=[10,17]
		# A4
		elif i==7:
			moves=[15,6]
		# B1
		elif i==62:
			moves=[-10,-17,-15]
		# B2
		elif i==57:
			moves=[-17,-15,-6]
		# B3
		elif i==48:
			moves=[-15,-6,10]
		# B4
		elif i==8:
			moves=[-6,10,17]
		# B5
		elif i==1:
			moves=[10,17,15]
		# B6
		elif i==6:
			moves=[17,15,6]
		# B7
		elif i==15:
			moves=[15,6,-10]
		# B8
		elif i==55:
			moves=[6,-10,-17]
		# C1
		elif i in [58,59,60,61,62]:
			moves=[-10,-17,-15,-6]
		# C2
		elif i==49:
			moves=[-17,-15,-6,10]
		# C3
		elif i in [16,24,32,40]:
			moves=[-15,-6,10,17]
		# C4
		elif i==9:
			moves=[-6,10,17,15]
		# C5
		elif i in [2,3,4,5]:
			moves=[10,17,15,6]
		# C6
		elif i==14:
			moves=[-10,6,15,17]
		# C7 
		elif i in [23,31,39,47]:
			moves=[15,6,-10,-17]
		# C8
		elif i==54:
			moves=[6,-10,-17,-15]
		# D1
		elif i in [50,51,52,53]:
			moves=[10,6,-10,-17,-15,-6]
		# D2
		elif i in [17,25,33,41]:
			moves=[10,17,15,-17,-15,-6]
		# D3
		elif i in [10,11,12,13]:
			moves=[10,17,15,6,-10,-6]
		# D4
		elif i in [22,30,38,46]:
			moves=[17,15,6,-10,-17,-15]
		# E
		else:
			moves=[10,17,15,6,-10,-17,-15,-6]
		
		knight_mov_list.append(moves)

	def __init__(self, color, sqr):
		assert 0<=sqr<=63 and isinstance(sqr,int), "PC_POS_ERR: Piece position must be an integer between 0 and 63."
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
			new_exp_pos[move[0]]='N'
		# If it is black, fill with black piece
		else:
			new_exp_pos[move[0]]='n'

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
			# Check by color
			if self.color==0:
				# White knights remove castling rights by capturing oponent rook
				# Rights are the same in case no conditional is triggered
				new_castl_avl = castl_avl
				# Capturing oponent rook
				# If black can castle kingside and white captured kingside rook, remove black kingside castling rights
				if 'k' in castl_avl and move[0]==7 and move[1]==1:
					new_castl_avl = new_castl_avl.replace('k','')
				# If black can castle queenside and white captured queenside rook, remove black queenside castling rights
				elif 'q' in castl_avl and move[0]==0 and move[1]==1:
					new_castl_avl = new_castl_avl.replace('q','')

			else:
				# Black knights remove castling rights by capturing oponent rook
				# Rights are the same in case no conditional is triggered
				new_castl_avl = castl_avl
				# Capturing oponent rook
				# If white can castle kingside and black captured kingside rook, remove white kingside castling rights
				if 'K' in castl_avl and move[0]==63 and move[1]==1:
					new_castl_avl = new_castl_avl.replace('K','')
				# If white can castle queenside and black captured queenside rook, remove white queenside castling rights
				elif 'Q' in castl_avl and move[0]==56 and move[1]==1:
					new_castl_avl = new_castl_avl.replace('Q','')

		# Any knight move removes en passant target
		new_en_pas_targ='-'

		# Increments half move clock if no pawn advance or capture has been made
		# Checks if capture happened
		if move[1]==1:
			new_half_mov_clk=str(0)
		# No capture or pawn move increments half move counter
		else:
			new_half_mov_clk=str(int(half_mov_clk)+1)

		# Increments move clock after a black move
		if clr_to_move=='b':
			new_mov_clk=str(int(mov_clk)+1)
		# If white move, keep move clock as is
		else:
			new_mov_clk=mov_clk

		new_exp_fen = new_exp_pos+' '+new_clr_to_move+' '+new_castl_avl+' '+new_en_pas_targ+' '+new_half_mov_clk+' '+new_mov_clk

		return new_exp_fen

	def avl_movs(self, efen, return_ctrl_sqr=False):
		exp_pos, clr_to_move, castl_avl, en_pas_targ, half_mov_clk, mov_clk = util.read_fen(efen)
		
		# Asserts that local piece parameters agree with with input position
		if self.color==0:
			assert exp_pos[self.sqr]=='N', "PC_POS_MISMATCH_ERR: Position does not agree with local piece type and location parameters."
		else:
			assert exp_pos[self.sqr]=='n', "PC_POS_MISMATCH_ERR: Position does not agree with local piece type and location parameters."
		
		avl_mov_list = []
		controlled_squares = []

		# Generate white moves if white
		if self.color==0:
			for move in knight.knight_mov_list[self.sqr]:
				target_sqr = self.sqr+move
				controlled_squares.append(target_sqr)
				# Generate normal move if square is free
				if exp_pos[target_sqr]=='u':
					avl_mov_list.append((target_sqr,0,))
				# Don't include move if occupied by friendly piece
				elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
					pass
				# Generate capture if finds enemy piece
				elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
					avl_mov_list.append((target_sqr,1,))
					

		# Generate black moves if black			
		else:
			for move in knight.knight_mov_list[self.sqr]:
				target_sqr = self.sqr+move
				controlled_squares.append(target_sqr)
				# Generate normal move if square is free
				if exp_pos[target_sqr]=='u':
					avl_mov_list.append((target_sqr,0,))
				# Don't include move if occupied by friendly piece
				elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
					pass
				# Generate capture if finds enemy piece
				elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
					avl_mov_list.append((target_sqr,1,))

		if return_ctrl_sqr:
			return avl_mov_list, controlled_squares
		else:
			return avl_mov_list

class queen:

	def __init__(self, color, sqr):
		assert 0<=sqr<=63 and isinstance(sqr,int), "PC_POS_ERR: Piece position must be an integer between 0 and 63."
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
			new_exp_pos[move[0]]='Q'
		# If it is black, fill with black piece
		else:
			new_exp_pos[move[0]]='q'

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
			# Check by color
			if self.color==0:
				# White queens remove castling rights by capturing oponent rook
				# Rights are the same in case no conditional is triggered
				new_castl_avl = castl_avl
				# Capturing oponent rook
				# If black can castle kingside and white captured kingside rook, remove black kingside castling rights
				if 'k' in castl_avl and move[0]==7 and move[1]==1:
					new_castl_avl = new_castl_avl.replace('k','')
				# If black can castle queenside and white captured queenside rook, remove black queenside castling rights
				elif 'q' in castl_avl and move[0]==0 and move[1]==1:
					new_castl_avl = new_castl_avl.replace('q','')

			else:
				# Black bishops remove castling rights by capturing oponent rook
				# Rights are the same in case no conditional is triggered
				new_castl_avl = castl_avl
				# Capturing oponent rook
				# If white can castle kingside and black captured kingside rook, remove white kingside castling rights
				if 'K' in castl_avl and move[0]==63 and move[1]==1:
					new_castl_avl = new_castl_avl.replace('K','')
				# If white can castle queenside and black captured queenside rook, remove white queenside castling rights
				elif 'Q' in castl_avl and move[0]==56 and move[1]==1:
					new_castl_avl = new_castl_avl.replace('Q','')

		# Any queen move removes en passant target
		new_en_pas_targ='-'

		# Increments half move clock if no pawn advance or capture has been made
		# Checks if capture happened
		if move[1]==1:
			new_half_mov_clk=str(0)
		# No capture or pawn move increments half move counter
		else:
			new_half_mov_clk=str(int(half_mov_clk)+1)

		# Increments move clock after a black move
		if clr_to_move=='b':
			new_mov_clk=str(int(mov_clk)+1)
		# If white move, keep move clock as is
		else:
			new_mov_clk=mov_clk

		new_exp_fen = new_exp_pos+' '+new_clr_to_move+' '+new_castl_avl+' '+new_en_pas_targ+' '+new_half_mov_clk+' '+new_mov_clk

		return new_exp_fen

	def avl_movs(self, efen, return_ctrl_sqr=False):
		exp_pos, clr_to_move, castl_avl, en_pas_targ, half_mov_clk, mov_clk = util.read_fen(efen)
		
		# Asserts that local piece parameters agree with with input position
		if self.color==0:
			assert exp_pos[self.sqr]=='Q', "PC_POS_MISMATCH_ERR: Position does not agree with local piece type and location parameters."
		else:
			assert exp_pos[self.sqr]=='q', "PC_POS_MISMATCH_ERR: Position does not agree with local piece type and location parameters."
		
		avl_mov_list = []
		controlled_squares = []

		# Generate white moves if white
		if self.color==0:
			# UPWARDS MOVES
			# Maximum number of squares to move is always 1 to 7 (8 squares is outside the board and 0 squares is not a move)
			for i in range(1,8):
				# Stop if outside black edge board range
				target_sqr = self.sqr-8*i
				if target_sqr<0:
					break
				else:
					controlled_squares.append(target_sqr)
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						avl_mov_list.append((target_sqr,1,))
						break

			# DOWNWARDS MOVES
			for i in range(1,8):
				# Stop if outside white edge board range
				target_sqr = self.sqr+8*i
				if target_sqr>63:
					break
				else:
					controlled_squares.append(target_sqr)
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						avl_mov_list.append((target_sqr,1,))
						break

			# KINGSIDEWARDS MOVES
			for i in range(1,8):
				# Stop if outside kingside edge board range
				target_sqr = self.sqr+i
				if (target_sqr)%8==0:
					break	
				else:
					controlled_squares.append(target_sqr)
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						avl_mov_list.append((target_sqr,1,))
						break

			# QUEENSIDEWARDS MOVES
			for i in range(1,8):
				# Stop if outside kingside edge board range
				target_sqr = self.sqr-i
				if (target_sqr)%8==7:
					break
				else:
					controlled_squares.append(target_sqr)
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						avl_mov_list.append((target_sqr,1,))
						break

			# BLACK-KINGSIDE DIAGONAL MOVES
			for i in range(1,8):
				target_sqr = self.sqr-7*i
				# Stop if reached top or side edge
				if target_sqr<0 or target_sqr%8==0:
					break
				else:
					controlled_squares.append(target_sqr)
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						avl_mov_list.append((target_sqr,1,))
						break

			# BLACK-QUEENSIDE DIAGONAL MOVES
			for i in range(1,8):
				target_sqr = self.sqr-9*i
				# Stop if reached top or side edge
				if target_sqr<0 or target_sqr%8==7:
					break
				else:
					controlled_squares.append(target_sqr)
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						avl_mov_list.append((target_sqr,1,))
						break

			# WHITE-KINGSIDE DIAGONAL MOVES
			for i in range(1,8):
				target_sqr = self.sqr+9*i
				# Stop if reached top or side edge
				if target_sqr>63 or target_sqr%8==0:
					break
				else:
					controlled_squares.append(target_sqr)
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						avl_mov_list.append((target_sqr,1,))
						break

			# WHITE-QUEENSIDE DIAGONAL MOVES
			for i in range(1,8):
				target_sqr = self.sqr+7*i
				# Stop if reached top or side edge
				if target_sqr>63 or target_sqr%8==7:
					break
				else:
					controlled_squares.append(target_sqr)
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						avl_mov_list.append((target_sqr,1,))
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
					controlled_squares.append(target_sqr)
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						avl_mov_list.append((target_sqr,1,))
						break

			# DOWNWARDS MOVES
			for i in range(1,8):
				# Stop if outside white edge board range
				target_sqr = self.sqr+8*i
				if target_sqr>63:
					break
				else:
					controlled_squares.append(target_sqr)
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						avl_mov_list.append((target_sqr,1,))
						break

			# KINGSIDEWARDS MOVES
			for i in range(1,8):
				# Stop if outside kingside edge board range
				target_sqr = self.sqr+i
				if (target_sqr)%8==0:
					break
				else:
					controlled_squares.append(target_sqr)
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						avl_mov_list.append((target_sqr,1,))
						break

			# QUEENSIDEWARDS MOVES
			for i in range(1,8):
				# Stop if outside kingside edge board range
				target_sqr = self.sqr-i
				if (target_sqr)%8==7:
					break
				else:
					controlled_squares.append(target_sqr)
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						avl_mov_list.append((target_sqr,1,))
						break

			# BLACK-KINGSIDE DIAGONAL MOVES
			for i in range(1,8):
				target_sqr = self.sqr-7*i
				# Stop if reached top or side edge
				if target_sqr<0 or target_sqr%8==0:
					break
				else:
					controlled_squares.append(target_sqr)
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						avl_mov_list.append((target_sqr,1,))
						break

			# BLACK-QUEENSIDE DIAGONAL MOVES
			for i in range(1,8):
				target_sqr = self.sqr-9*i
				# Stop if reached top or side edge
				if target_sqr<0 or target_sqr%8==7:
					break
				else:
					controlled_squares.append(target_sqr)
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						avl_mov_list.append((target_sqr,1,))
						break

			# WHITE-KINGSIDE DIAGONAL MOVES
			for i in range(1,8):
				target_sqr = self.sqr+9*i
				# Stop if reached top or side edge
				if target_sqr>63 or target_sqr%8==0:
					break
				else:
					controlled_squares.append(target_sqr)
					# Check if normal move (target square is empty)
					if exp_pos[target_sqr]=='u':
						avl_mov_list.append((target_sqr,0,))
					# Stop if blocked by friendly piece
					elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
						break
					# Generate capture if finds enemy piece and stop
					elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
						avl_mov_list.append((target_sqr,1,))
						break

			# WHITE-QUEENSIDE DIAGONAL MOVES
			for i in range(1,8):
				target_sqr = self.sqr+7*i
				# Stop if reached top or side edge
				if target_sqr>63 or target_sqr%8==7:
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
						avl_mov_list.append((target_sqr,1,))
						break

		if return_ctrl_sqr:
			return avl_mov_list, controlled_squares
		else:
			return avl_mov_list

class king:

	def __init__(self, color, sqr):
		assert 0<=sqr<=63 and isinstance(sqr,int), "PC_POS_ERR: Piece position must be an integer between 0 and 63."
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

		#Copy position
		new_exp_pos=[char for char in exp_pos]

		# Fill new piece position
		# If piece is white, fill with white piece
		if self.color==0:
			# Normal move or capture
			if move[1] in [0,1]:
				new_exp_pos[move[0]]='K'
			# Short castle
			elif move[1]==8:
				new_exp_pos[61:64]=['R','K','u']
			# Long casle
			elif move[1]==9:
				new_exp_pos[56:60]=['u','u','K','R']
		# If it is black, fill with black piece
		else:
			# Normal move or capture
			if move[1] in [0,1]:
				new_exp_pos[move[0]]='k'
			# Short castle
			elif move[1]==8:
				new_exp_pos[5:8]=['r','k','u']
			# Long casle
			elif move[1]==9:
				new_exp_pos[0:4]=['u','u','k','r']

		# Empty previous piece position
		new_exp_pos[self.sqr]='u'

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
			# Check by color
			if self.color==0:
				new_castl_avl=castl_avl

				# Moving or castling
				# Remove own castling rights when castling
				if move[1] in [8,9]:
					new_castl_avl = new_castl_avl.replace('K','')
					new_castl_avl = new_castl_avl.replace('Q','')
				# Remove own castling rights if moving
				elif move[1] in [0,1]:
					new_castl_avl = new_castl_avl.replace('K','')
					new_castl_avl = new_castl_avl.replace('Q','')

				# Capturing enemy rook
				# If black can castle kingside and white captured kingside rook, remove black kingside castling rights
				if 'k' in castl_avl and move[0]==7 and move[1]==1:
					new_castl_avl = new_castl_avl.replace('k','')
				# If black can castle queenside and white captured queenside rook, remove black queenside castling rights
				elif 'q' in castl_avl and move[0]==0 and move[1]==1:
					new_castl_avl = new_castl_avl.replace('q','')

			else:
				new_castl_avl=castl_avl

				# Moving or castling
				# Remove own castling rights when castling
				if move[1] in [8,9]:
					new_castl_avl = new_castl_avl.replace('k','')
					new_castl_avl = new_castl_avl.replace('q','')
				# Remove own castling rights if moving
				elif move[1] in [0,1]:
					new_castl_avl = new_castl_avl.replace('k','')
					new_castl_avl = new_castl_avl.replace('q','')

				# Capturing enemy rook
				# If white can castle kingside and black captured kingside rook, remove white kingside castling rights
				if 'K' in castl_avl and move[0]==63 and move[1]==1:
					new_castl_avl = new_castl_avl.replace('K','')
				# If white can castle queenside and black captured queenside rook, remove white queenside castling rights
				elif 'Q' in castl_avl and move[0]==56 and move[1]==1:
					new_castl_avl = new_castl_avl.replace('Q','')

		# Any king move removes en passant target
		new_en_pas_targ='-'

		# Increments half move clock if no pawn advance or capture has been made
		# Checks if capture happened
		if move[1]==1:
			new_half_mov_clk=str(0)
		# No capture or pawn move increments half move counter
		else:
			new_half_mov_clk=str(int(half_mov_clk)+1)

		# Increments move clock after a black move
		if clr_to_move=='b':
			new_mov_clk=str(int(mov_clk)+1)
		# If white move, keep move clock as is
		else:
			new_mov_clk=mov_clk

		new_exp_fen = new_exp_pos+' '+new_clr_to_move+' '+new_castl_avl+' '+new_en_pas_targ+' '+new_half_mov_clk+' '+new_mov_clk

		return new_exp_fen

	def avl_movs(self, efen, return_ctrl_sqr=False):
		exp_pos, clr_to_move, castl_avl, en_pas_targ, half_mov_clk, mov_clk = util.read_fen(efen)
		
		# Asserts that local piece parameters agree with with input position
		if self.color==0:
			assert exp_pos[self.sqr]=='K', "PC_POS_MISMATCH_ERR: Position does not agree with local piece type and location parameters."
		else:
			assert exp_pos[self.sqr]=='k', "PC_POS_MISMATCH_ERR: Position does not agree with local piece type and location parameters."
		
		avl_mov_list = []
		controlled_squares = []

		# Generate white moves if white
		if self.color==0:
			# Normal moves and captures
			for (move,condition) in [(-9,lambda target: target<0 or target%8==7),
									 (-8,lambda target: target<0),
									 (-7,lambda target: target<0 or target%8==0),
									 (-1,lambda target: target%8==7),
									 (1, lambda target: target%8==0),
									 (7, lambda target: target>63 or target%8==7),
									 (8, lambda target: target>63),
									 (9, lambda target: target>63 or target%8==0)]:
				target_sqr = self.sqr + move
				# Check if out of bounds
				if condition(target_sqr):
					pass
				# Check if normal move (target square is empty)
				elif exp_pos[target_sqr]=='u':
					avl_mov_list.append((target_sqr,0,))
					controlled_squares.append(target_sqr)
				# Stop if blocked by friendly piece
				elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
					controlled_squares.append(target_sqr)
					pass
				# Generate capture if finds enemy piece and stop
				elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
					avl_mov_list.append((target_sqr,1,))
					controlled_squares.append(target_sqr)

			# Castling short
			if 'K' in castl_avl and exp_pos[61]=='u' and exp_pos[62]=='u':
				avl_mov_list.append((62,8,))

			# Castling long
			if 'Q' in castl_avl and exp_pos[57]=='u' and exp_pos[58]=='u' and exp_pos[59]=='u':
				avl_mov_list.append((58,9,))

		# Generate black moves if black			
		else:
			# Normal moves
			for (move,condition) in [(-9,lambda target: target<0 or target%8==7),
									 (-8,lambda target: target<0),
									 (-7,lambda target: target<0 or target%8==0),
									 (-1,lambda target: target%8==7),
									 (1, lambda target: target%8==0),
									 (7, lambda target: target>63 or target%8==7),
									 (8, lambda target: target>63),
									 (9, lambda target: target>63 or target%8==0)]:
				target_sqr = self.sqr + move
				# Check if out of bounds
				if condition(target_sqr):
					pass
				# Check if normal move (target square is empty)
				elif exp_pos[target_sqr]=='u':
					avl_mov_list.append((target_sqr,0,))
					controlled_squares.append(target_sqr)
				# Stop if blocked by friendly piece
				elif exp_pos[target_sqr] in ['p','n','b','r','q','k']:
					controlled_squares.append(target_sqr)
					pass
				# Generate capture if finds enemy piece and stop
				elif exp_pos[target_sqr] in ['P','N','B','R','Q','K']:
					avl_mov_list.append((target_sqr,1,))
					controlled_squares.append(target_sqr)

			# Castling short
			if 'k' in castl_avl and exp_pos[5]=='u' and exp_pos[6]=='u':
				avl_mov_list.append((6,8,))

			# Castling long
			if 'q' in castl_avl and exp_pos[1]=='u' and exp_pos[2]=='u' and exp_pos[3]=='u':
				avl_mov_list.append((2,9,))

		if return_ctrl_sqr:
			return avl_mov_list, controlled_squares
		else:
			return avl_mov_list

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
