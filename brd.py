# Board class file
import util, sys
from move_gen import gen_piece_moves
import time

# Suggestion, differentiate self.state from the position history, easier to keep move history (and essential changes, such as castling rights, en passants, half move)
# Actually calculate inverse move in the unmake_move function, instead of just popping last frame from stack


# Pieces by number: WHITE: 00unmoved pawn, 01moved pawn, 02knight, 03bishop, 04rook, 05queen, 06KQking, 07Kking, 08Qking, 09king
#					BLACK: 10unmoved pawn, 11moved pawn, 12knight, 13bishop, 14rook, 15queen, 16KQking, 17Kking, 18Qking, 19king
#					'': None

# Use en passant square by square number number. If no en passant: None

initial_state=[([14,12,13,15,16,13,12,14,	#
				 10,10,10,10,10,10,10,10,	#
				 '','','','','','','','',	#
				 '','','','','','','','',	#
				 '','','','','','','','',	# Board squares list
				 '','','','','','','','',	#
				 0, 0, 0, 0, 0, 0, 0, 0,	#
				 4, 2, 3, 5, 6, 3, 2, 4],	#
				 0,		# Color to move
				 None,	# En passant square
				 0)]	# Half move count

piece_dict={0:'P', 1:'P', 2:'N', 3:'B', 4:'R', 5:'Q', 6:'K', 7:'K', 8:'K', 9:'K',
			10:'p', 11:'p', 12:'n', 13:'b', 14:'r', 15:'q', 16:'k', 17:'k', 18:'k', 19:'k' }

def calc_bitboard_from_squares(squares):
	# Bitboards
	w_bb=0
	b_bb=0
	# Filling bitboard and piece list
	for i in range(64):
		# If square not empty
		if squares[i]!='':
			# If white piece... 
			if squares[i]<10:
				# Add to bitboard
				w_bb+=2**(63-i)

			# Else, black piece...
			else:
				# Add to bitboard
				b_bb+=2**(63-i)

	return w_bb,b_bb

def get_frame_piece_list(frame):
	# Declaring occupancy bitboards and piece list (dictionary)
	w_pieces={0:[],	#00unmoved pawn
			  1:[],	#01moved pawn
			  2:[],	#02knight
			  3:[],	#03bishop
			  4:[],	#04rook
			  5:[],	#05queen
			  6:[],	#06KQking
			  7:[],	#07Kking
			  8:[],	#08Qking
			  9:[]}	#09king

	b_pieces={10:[], #00unmoved pawn
			  11:[], #01moved pawn
			  12:[], #02knight
			  13:[], #03bishop
			  14:[], #04rook
			  15:[], #05queen
			  16:[], #06KQking
			  17:[], #07Kking
			  18:[], #08Qking
			  19:[]} #09king
	# Bitboards
	w_bb=0
	b_bb=0

	# Filling bitboard and piece list
	for i in range(64):
		# If square not empty
		if frame[0][i]!='':
			# If white piece... 
			if frame[0][i]<10:
				# Add to bitboard
				w_bb+=2**(63-i)
				# Increment piece count
				w_pieces[frame[0][i]].append(i)

			# Else, black piece...
			else:
				# Add to bitboard
				b_bb+=2**(63-i)
				# Increment piece count
				b_pieces[frame[0][i]].append(i)

	return w_pieces, b_pieces, w_bb, b_bb

def get_frame_from_fen(fen):
	efen=util.fen2efen(fen)
	pieces_pos, clr_to_move, castl_avl, en_pas_targ, half_mov_clk, mov_clk=util.read_fen(efen)
	# Get squares
	squares=[]
	for i in range(len(pieces_pos)):		
		# Empty
		if pieces_pos[i]=='u':
			squares.append('')
		# Pawn
		elif pieces_pos[i]=='p':
			if 8<=i<=15:
				squares.append(10)
			else:
				squares.append(11)
		elif pieces_pos[i]=='P':
			if 48<=i<=55:
				squares.append(0)
			else:
				squares.append(1)
		# Knight
		elif pieces_pos[i]=='n':
			squares.append(12)
		elif pieces_pos[i]=='N':
			squares.append(2)
		# Bishop
		elif pieces_pos[i]=='b':
			squares.append(13)
		elif pieces_pos[i]=='B':
			squares.append(3)
		# Rook
		elif pieces_pos[i]=='r':
			squares.append(14)
		elif pieces_pos[i]=='R':
			squares.append(4)
		# Queen
		elif pieces_pos[i]=='q':
			squares.append(15)
		elif pieces_pos[i]=='Q':
			squares.append(5)
		# King
		elif pieces_pos[i]=='k':
			# QKKing
			if 'k' in castl_avl and 'q' in castl_avl:
				squares.append(16)
			# KKing
			elif 'k' in castl_avl:
				squares.append(17)
			# QKing
			elif 'q' in castl_avl:
				squares.append(18)
			# King
			else:
				squares.append(19)
		elif pieces_pos[i]=='K':
			# QKKing
			if 'K' in castl_avl and 'Q' in castl_avl:
				squares.append(6)
			# KKing
			elif 'K' in castl_avl:
				squares.append(7)
			# QKing
			elif 'Q' in castl_avl:
				squares.append(8)
			# King
			else:
				squares.append(9)
	
	# Get color to move
	if clr_to_move=='w':
		frame_clr_to_move=0
	else:
		frame_clr_to_move=1

	# Get en passant square
	if en_pas_targ!='-':
		frame_en_pas_sqr=util.sqr2coord(en_pas_targ)
	else:
		frame_en_pas_sqr=None

	# Assemble frame
	return (squares, frame_clr_to_move, frame_en_pas_sqr, int(half_mov_clk))

def deep_append(tg_dict,index,elem):
	placeholder_list=list(tg_dict[index])
	placeholder_list.append(elem)
	tg_dict[index]=placeholder_list

def deep_remove(tg_dict,index,elem):
	placeholder_list=list(tg_dict[index])
	placeholder_list.remove(elem)
	tg_dict[index]=placeholder_list

# Don't recalculate piece list at every move and bitboard, ineficient!!
# Update!
# get_frame_piece_list is the bottleneck call

class board:

	def set(self, state):
		"""
		State is a list of "frames" encoded as:
			1. List of size 64 of all squares and their occupancy (castling is encoded in the king piece )
			2. Color to move
			3. En passant square
			4. Half-move count (to facilitate 50 move rule detection)
		Move count is unnecessary since it can be achieved from the list size count.

		Also store vector of [self.w_pieces,self.b_pieces,self.w_bb,self.b_bb] history
		"""
		# Store state input
		self.state=state
		# Get frame piece list
		w_pieces,b_pieces,w_bb,b_bb = get_frame_piece_list(state[-1])

		self.sup_data=[(w_pieces,b_pieces,w_bb,b_bb)]

	def update_state(self,frame,sup_data):
		# Append frame
		self.state.append(frame)
		# Get frame piece list
		self.sup_data_hist.append(sup_data)

	def get_pseudo_moves(self):
		# Check what pieces can move and assign friend and enemy bitboards
		if self.state[-1][1]==0:
			pieces=self.sup_data[-1][0]
			fr_bb=self.sup_data[-1][2]
			en_bb=self.sup_data[-1][3]
		else:
			pieces=self.sup_data[-1][1]
			fr_bb=self.sup_data[-1][3]
			en_bb=self.sup_data[-1][2]
		# Generate moves
		move_list=[]
		for (piece, sqrs) in pieces.items():
			for sqr in sqrs:
				move_list.extend(gen_piece_moves(piece, sqr, fr_bb, en_bb, self.state[-1][2]))

		return move_list


	# Change king type when rook is captured!
	# Do promotions!
	def make_move(self, move):
		# Take origin and target pieces
		piece=self.state[-1][0][move[0]]

		if move[1]<64:
			target_sqr=self.state[-1][0][move[1]]
		else:
			target_sqr=move[1] # For special moves

		# Copy original squares frame to modify
		new_squares=list(self.state[-1][0])
		
		# Always increment color to move
		new_clr_to_move=(self.state[-1][1]+1)%2


		# SUGGESTION!! Only hard copy the lists that are changed!!! This must speed up the function!
		# Make sup_data list local copy
		# w_pieces=dict((i,list(self.sup_data[-1][0][i])) for i in range(10))
		# b_pieces=dict((i,list(self.sup_data[-1][1][i])) for i in range(10,20))
		w_pieces=dict(self.sup_data[-1][0])
		b_pieces=dict(self.sup_data[-1][1])
		w_bb=self.sup_data[-1][2]
		b_bb=self.sup_data[-1][3]

		# Go through piece by piece
		# Unmoved pawn
		if piece%10==0:
			# See if capture and change piece counts
			# Removing captured piece
			if target_sqr!='':
				try:
					deep_remove(w_pieces,target_sqr,move[1])
					w_bb-=2**(63-move[1])
				except:
					deep_remove(b_pieces,target_sqr,move[1])
					b_bb-=2**(63-move[1])

			# Change pawn type in piece count after move
			try:
				deep_remove(w_pieces,piece,move[0])
				deep_append(w_pieces,piece+1,move[1])
				w_bb-=2**(63-move[0])
				w_bb+=2**(63-move[1])
			except:
				deep_remove(b_pieces,piece,move[0])
				deep_append(b_pieces,piece+1,move[1])
				b_bb-=2**(63-move[0])
				b_bb+=2**(63-move[1])
			# Move piece and change pawn type
			new_squares[move[1]]=piece+1
			new_squares[move[0]]=''
			# If double move, add en passant square
			if 40<=move[1]<=47:
				new_en_passant=move[1]+8
			elif 16<=move[1]<=23:
				new_en_passant=move[1]-8
			else:
				new_en_passant=None
			# Pawn moves reset half move clock
			new_half_move=0
			

		# Moved pawn, DO PROMOTION EXCEPTIONS!!! target_sqr>63 and piece count
		elif piece%10==1:
			# Removing captured piece
			if target_sqr!='':
				try:
					deep_remove(w_pieces,target_sqr,move[1])
					w_bb-=2**(63-move[1])
				except:
					deep_remove(b_pieces,target_sqr,move[1])
					b_bb-=2**(63-move[1])
			# Do promotions!!! Change piece count...
			# Change piece position
			try:
				deep_remove(w_pieces,piece,move[0])
				deep_append(w_pieces,piece,move[1])
				w_bb-=2**(63-move[0])
				w_bb+=2**(63-move[1])
			except:
				deep_remove(b_pieces,piece,move[0])
				deep_append(b_pieces,piece,move[1])
				b_bb-=2**(63-move[0])
				b_bb+=2**(63-move[1])
			# Move piece
			new_squares[move[1]]=piece
			new_squares[move[0]]=''

			# No en passant square
			new_en_passant=None
			# Pawn moves reset half move clock
			new_half_move=0

		# Rook
		elif piece%10==4:
			# Legend: 06KQking, 07Kking, 08Qking, 09king
			# If white piece
			if piece<10:
				# Removing captured black piece, if move was capture
				if target_sqr!='':
					deep_remove(b_pieces,target_sqr,move[1])
					b_bb-=2**(63-move[1])
					new_half_move=0
				else:
					new_half_move=self.state[-1][3]+1

				# If king can castle
				if w_pieces[9]==[]:
					# Kingside rook move removes kingside castle
					if move[0]==63:
						# KQ
						if self.state[-1][0][60]==6:
							new_squares[60]=8
							# Update piece types
							deep_remove(w_pieces,6,60) # Remove current king
							deep_append(w_pieces,8,60) # Change to no kingside castle king
						# K
						elif self.state[-1][0][60]==7:
							new_squares[60]=9
							# Update piece types
							deep_remove(w_pieces,7,60) # Remove current king
							deep_append(w_pieces,9,60) # Change to no kingside castle king
					# Queenside rook move removes queenside castle
					if move[0]==56:
						# KQ or K
						if self.state[-1][0][60]==6:
							new_squares[60]=7
							# Update piece types
							deep_remove(w_pieces,6,60) # Remove current king
							deep_append(w_pieces,7,60) # Change to no queenside castle king
						# Q
						elif self.state[-1][0][60]==8:
							new_squares[60]=9
							# Update piece types
							deep_remove(w_pieces,8,60) # Remove current king
							deep_append(w_pieces,9,60) # Change to no queenside castle king
				# If king can't castle, don't change piece types
				# Move piece
				deep_remove(w_pieces,piece,move[0]) 
				deep_append(w_pieces,piece,move[1])
				w_bb-=2**(63-move[0])
				w_bb+=2**(63-move[1])
				new_squares[move[1]]=piece
				new_squares[move[0]]=''

			# Else, black piece
			# Legend: 16KQking, 17Kking, 18Qking, 19king
			else:
				# Removing captured white piece
				if target_sqr!='':
					deep_remove(w_pieces,target_sqr,move[1])
					new_half_move=0
				else:
					new_half_move=self.state[-1][3]+1

				# If king can castle
				if b_pieces[19]==[]:
					# Kingside rook move removes kingside castle
					if move[0]==7:
						# KQ or Q
						if self.state[-1][0][4]==16:
							new_squares[4]=18
							# Update piece types
							deep_remove(b_pieces,16,4) # Remove current king
							deep_append(b_pieces,17,4) # Change to no kingside castle king
						# K
						elif self.state[-1][0][4]==17:
							new_squares[4]=19
							# Update piece types
							deep_remove(b_pieces,17,4) # Remove current king
							deep_append(b_pieces,19,4) # Change to no kingside castle king
					# Queenside rook move removes queenside castle
					elif move[0]==0:
						# KQ or K
						if self.state[-1][0][4]==16:
							new_squares[4]=17
							# Update piece types
							deep_remove(b_pieces,16,4) # Remove current king
							deep_append(b_pieces,18,4) # Change to no queenside castle king
						# Q
						elif self.state[-1][0][4]==18:
							new_squares[4]=19
							# Update piece types
							deep_remove(b_pieces,18,4) # Remove current king
							deep_append(b_pieces,19,4) # Change to no queenside castle king
				# If king can't castle, proceed normally
				# Move piece
				deep_remove(b_pieces,piece,move[0]) 
				deep_append(b_pieces,piece,move[1])
				b_bb-=2**(63-move[0])
				b_bb+=2**(63-move[1])
				new_squares[move[1]]=piece
				new_squares[move[0]]=''
					
			# No en passant square
			new_en_passant=None

		# KQKing
		elif piece%10==6:
			# Removing captured piece if normal move and capture
			if target_sqr!='' and target_sqr<20: # If target square is a piece type
				try:
					deep_remove(w_pieces,target_sqr,move[1])
					w_bb-=2**(63-move[1])
				except:
					deep_remove(b_pieces,target_sqr,move[1])
					b_bb-=2**(63-move[1])
				new_half_move=0
			# Increment half move in the new frame if no capture or not special move
			else:
				new_half_move=self.state[-1][3]+1

			# If kingside castle
			if move[1]==64:
				# White king
				if piece<10:
					new_squares[60:64]=['',4,9,'']
					# Update piece types
					# King
					deep_remove(w_pieces,6,60)
					deep_append(w_pieces,9,62)
					w_bb-=2**(63-60)
					w_bb+=2**(63-62)
					# Rook
					deep_remove(w_pieces,4,63)
					deep_append(w_pieces,4,61)
					w_bb-=2**(63-63)
					w_bb+=2**(63-61)
				# Black king
				else:
					new_squares[4:8]=['',14,19,'']
					# Update piece types
					# King
					deep_remove(b_pieces,16,4)
					deep_append(b_pieces,19,6)
					b_bb-=2**(63-4)
					b_bb+=2**(63-6)
					# Rook
					deep_remove(b_pieces,14,7)
					deep_append(b_pieces,14,5)
					b_bb-=2**(63-7)
					b_bb+=2**(63-5)
			# If queenside castle
			elif move[1]==65:
				# White king
				if piece<10:
					new_squares[56:60]=['','',9,4,'']
					# Update piece types
					# King
					deep_remove(w_pieces,6,60)
					deep_append(w_pieces,9,58)
					w_bb-=2**(63-60)
					w_bb+=2**(63-58)
					# Rook
					deep_remove(w_pieces,4,56)
					deep_append(w_pieces,4,59)
					w_bb-=2**(63-56)
					w_bb+=2**(63-59)
				# Black king
				else:
					new_squares[0:4]=['','',19,14,'']
					# Update piece types
					# King
					deep_remove(b_pieces,16,4)
					deep_append(b_pieces,19,2)
					b_bb-=2**(63-4)
					b_bb+=2**(63-2)
					# Rook
					deep_remove(b_pieces,14,0)
					deep_append(b_pieces,14,3)
					b_bb-=2**(63-0)
					b_bb+=2**(63-3)

			# Else, normal move
			else:
				# Move piece
				new_squares[move[1]]= piece-piece%10+9 # Transform into no castle king
				new_squares[move[0]]=''
				try:
					deep_remove(w_pieces,6,move[0]) 
					deep_append(w_pieces,9,move[1])
					w_bb-=2**(63-move[0])
					w_bb+=2**(63-move[1])
				except:
					deep_remove(b_pieces,16,move[0]) 
					deep_append(b_pieces,19,move[1])
					b_bb-=2**(63-move[0])
					b_bb+=2**(63-move[1])

			# No en passant square
			new_en_passant=None
		
		# KKing
		elif piece%10==7:
			# Removing captured piece if normal move
			if target_sqr!='' and target_sqr<20: # If target square is a piece type
				try:
					deep_remove(w_pieces,target_sqr,move[1])
					w_bb-=2**(63-move[1])
				except:
					deep_remove(b_pieces,target_sqr,move[1])
					b_bb-=2**(63-move[1])
				new_half_move=0
			# Increment half move in the new frame if no capture or not special move
			else:
				new_half_move=self.state[-1][3]+1

			# If kingside castle
			if move[1]==64:
				# White king
				if piece<10:
					new_squares[60:64]=['',4,9,'']
					# Update piece types
					# King
					deep_remove(w_pieces,7,60)
					deep_append(w_pieces,9,62)
					w_bb-=2**(63-60)
					w_bb+=2**(63-62)
					# Rook
					deep_remove(w_pieces,4,63)
					deep_append(w_pieces,4,61)
					w_bb-=2**(63-63)
					w_bb+=2**(63-61)

				# Black king
				else:
					new_squares[4:8]=['',14,19,'']
					# Update piece types
					# King
					deep_remove(b_pieces,17,4)
					deep_append(b_pieces,19,6)
					b_bb-=2**(63-4)
					b_bb+=2**(63-6)
					# Rook
					deep_remove(b_pieces,14,7)
					deep_append(b_pieces,14,5)
					b_bb-=2**(63-7)
					b_bb+=2**(63-5)

			# Else, normal move
			else:
				# Move piece
				new_squares[move[1]]= piece-piece%10+9 # Transform into no castle king
				new_squares[move[0]]=''
				try:
					deep_remove(w_pieces,7,move[0]) 
					deep_append(w_pieces,9,move[1])
					w_bb-=2**(63-move[0])
					w_bb+=2**(63-move[1])
				except:
					deep_remove(b_pieces,17,move[0]) 
					deep_append(b_pieces,19,move[1])
					b_bb-=2**(63-move[0])
					b_bb+=2**(63-move[1])

			# No en passant square
			new_en_passant=None

		# QKing
		elif piece%10==8:
			# Removing captured piece if normal move
			if target_sqr!='' and target_sqr<20: # If target square is a piece type
				try:
					deep_remove(w_pieces,target_sqr,move[1])
					w_bb-=2**(63-move[1])
				except:
					deep_remove(b_pieces,target_sqr,move[1])
					b_bb-=2**(63-move[1])

				new_half_move=0
			# Increment half move in the new frame if no capture or not special move
			else:
				new_half_move=self.state[-1][3]+1

			# If queenside castle
			if move[1]==65:
				# White king
				if piece<10:
					new_squares[56:60]=['','',9,4,'']
					# Update piece types
					# King
					deep_remove(w_pieces,8,60)
					deep_append(w_pieces,9,58)
					w_bb-=2**(63-60)
					w_bb+=2**(63-58)
					# Rook
					deep_remove(w_pieces,4,56)
					deep_append(w_pieces,4,59)
					w_bb-=2**(63-56)
					w_bb+=2**(63-59)
				# Black king
				else:
					new_squares[0:4]=['','',19,14,'']
					# Update piece types
					# King
					deep_remove(b_pieces,18,4)
					deep_append(b_pieces,19,2)
					b_bb-=2**(63-4)
					b_bb+=2**(63-2)
					# Rook
					deep_remove(b_pieces,14,0)
					deep_append(b_pieces,14,3)
					b_bb-=2**(63-0)
					b_bb+=2**(63-3)


			# Else, normal move
			else:
				# Move piece
				new_squares[move[1]]= piece-piece%10+9 # Transform into no castle king
				new_squares[move[0]]=''
				try:
					deep_remove(w_pieces,8,move[0]) 
					deep_append(w_pieces,9,move[1])
					w_bb-=2**(63-move[0])
					w_bb+=2**(63-move[1])
				except:
					deep_remove(b_pieces,18,move[0]) 
					deep_append(b_pieces,19,move[1])
					b_bb-=2**(63-move[0])
					b_bb+=2**(63-move[1])

			# No en passant square
			new_en_passant=None


		# Other normal pieces
		else:
			# Removing captured piece if normal move
			if target_sqr!='': # If target square is a piece type
				try:
					deep_remove(w_pieces,target_sqr,move[1])
					w_bb-=2**(63-move[1])
				except:
					deep_remove(b_pieces,target_sqr,move[1])
					b_bb-=2**(63-move[1])
				new_half_move=0
			# Increment half move in the new frame if no capture
			else:
				new_half_move=self.state[-1][3]+1

			# Move piece
			new_squares[move[1]]=piece
			new_squares[move[0]]=''
			try:
				deep_remove(w_pieces,piece,move[0])
				deep_append(w_pieces,piece,move[1])
				w_bb-=2**(63-move[0])
				w_bb+=2**(63-move[1])
			except:
				deep_remove(b_pieces,piece,move[0])
				deep_append(b_pieces,piece,move[1])
				b_bb-=2**(63-move[0])
				b_bb+=2**(63-move[1])

			# No en passant square
			new_en_passant=None

		# After makemove, check if both rooks exist and adapt king type accordingly
		new_frame=(new_squares, new_clr_to_move, new_en_passant, new_half_move)
		#w_bb,b_bb=calc_bitboard_from_squares(new_squares)
		new_sup_data=(w_pieces,b_pieces,w_bb,b_bb)

		self.state.append(new_frame)
		self.sup_data.append(new_sup_data)

	def unmake_move(self):
		self.state=self.state[0:-1]
		self.sup_data=self.sup_data[0:-1]

	def get_moves(self):
		moves=self.get_pseudo_moves()
		legal_moves=[]
		# Make the move
		#[print('init item',i,self.sup_data[i]) for i in range(len(self.sup_data))]
		#print('')
		for move in moves:
			# Exception for castling, to avoid castling through check
			if move[1] in [64,65]:
				if self.is_castling_legal(move):
					legal_moves.append(move)
			# Other kinds of moves
			else:
				#print('testing move:',move,'---------------------------------------------------------------------------')
				self.make_move(move)
				#[print('made item',i,self.sup_data[i]) for i in range(len(self.sup_data))]
				#print('')
				# Get answers
				answers=self.get_pseudo_moves()
				# See if any answer returns a position without a king, raise ilegal flag if it does
				ilegal=False
				for answer in answers:
					#print('answer',answer)
					self.make_move(answer)
					#[print('supitem',i,self.sup_data[i]) for i in range(len(self.sup_data))]
					# Look for no kings
					has_w_king=False
					for i in [6,7,8,9]:
						if self.sup_data[-1][0][i]!=[]:
							has_w_king=True
					has_b_king=False
					for i in [16,17,18,19]:
						if self.sup_data[-1][1][i]!=[]:
							has_b_king=True
					# Unmake the move to prepare for next answer
					self.unmake_move()
					#print('')
					#[print('unmade supitem',i,self.sup_data[i]) for i in range(len(self.sup_data))]
					#print('')
					if (not has_w_king) or (not has_b_king):
						ilegal=True
						break
				# If move is legal, append to legal list
				if ilegal==False:
					legal_moves.append(move)
				self.unmake_move()
		return legal_moves

	def is_castling_legal(self,move):
		# Kingside castling
		if move[1]==64:
			# If white king
			if self.state[-1][1]==0:
				# Move king to squares 61 and 62 and leave king in 60 to see if in check
				for castl_move in [(60,60),(60,61),(60,62)]:
					self.make_move(castl_move)
					# Get answers
					answers=self.get_pseudo_moves()
					# See if any answer returns a position without a king, raise ilegal flag if it does
					ilegal=False
					for answer in answers:
						self.make_move(answer)
						# Look for no kings
						has_w_king=False
						for i in [6,7,8,9]:
							if self.w_pieces[i]!=[]:
								has_w_king=True
						# Unmake the move to prepare for next answer
						self.unmake_move()
						if not has_w_king:
							ilegal=True
							break
					self.unmake_move()
					# If found a position of castling path that results in king capture, castling is ilegal!
					if ilegal==True:
						break
				# If move is legal, return true
				if ilegal==False:
					return True
				# Else return false
				else:
					return False
			# If black king
			else:
				# Move king to squares 61 and 62
				for castl_mov in [(4,4),(4,5),(4,6)]:
					self.make_move(move)
					# Get answers
					answers=self.get_pseudo_moves()
					# See if any answer returns a position without a king, raise ilegal flag if it does
					ilegal=False
					for answer in answers:
						self.make_move(answer)
						# Look for no kings
						has_b_king=False
						for i in [16,17,18,19]:
							if self.b_pieces[i]!=[]:
								has_b_king=True
						# Unmake the move to prepare for next answer
						self.unmake_move()
						if not has_b_king:
							ilegal=True
							break
					self.unmake_move()
					# If found a position of castling path that results in king capture, castling is ilegal!
					if ilegal==True:
						break
				# If move is legal, return true
				if ilegal==False:
					return True
				# Else return false
				else:
					return False
		# Queenside castle
		elif move[1]==65:
			# If white king
			if self.state[-1][1]==0:
				# Move king to squares 61 and 62
				for castl_mov in [(60,60),(60,59),(60,58)]:
					self.make_move(move)
					# Get answers
					answers=self.get_pseudo_moves()
					# See if any answer returns a position without a king, raise ilegal flag if it does
					ilegal=False
					for answer in answers:
						self.make_move(answer)
						# Look for no kings
						has_w_king=False
						for i in [6,7,8,9]:
							if self.w_pieces[i]!=[]:
								has_w_king=True
						# Unmake the move to prepare for next answer
						self.unmake_move()
						if not has_w_king:
							ilegal=True
							break
					self.unmake_move()
					# If found a position of castling path that results in king capture, castling is ilegal!
					if ilegal==True:
						break
				# If move is legal, return true
				if ilegal==False:
					return True
				# Else return false
				else:
					return False		
			# If black king
			else:
				# Move king to squares 61 and 62
				for castl_mov in [(4,4),(4,3),(4,2)]:
					self.make_move(move)
					# Get answers
					answers=self.get_pseudo_moves()
					# See if any answer returns a position without a king, raise ilegal flag if it does
					ilegal=False
					for answer in answers:
						self.make_move(answer)
						# Look for no kings
						has_b_king=False
						for i in [16,17,18,19]:
							if self.b_pieces[i]!=[]:
								has_b_king=True
						# Unmake the move to prepare for next answer
						self.unmake_move()
						if not has_b_king:
							ilegal=True
							break
					self.unmake_move()
					# If found a position of castling path that results in king capture, castling is ilegal!
					if ilegal==True:
						break
				# If move is legal, return true
				if ilegal==False:
					return True
				# Else return false
				else:
					return False

	def get_fen(self):
		efen=[]
		w_pieces=self.sup_data[-1][0]
		b_pieces=self.sup_data[-1][1]
		w_bb=self.sup_data[-1][2]
		b_bb=self.sup_data[-1][3]
		# Get pieces
		pos=self.state[-1][0]
		for i in range(len(pos)):
			# empty
			if pos[i]=='':
				efen.append('u')
			# white pawn
			elif pos[i] in [0,1]:
				efen.append('P')
			# black pawn
			elif pos[i] in [10,11]:
				efen.append('p')
			# white knight
			elif pos[i]==2:
				efen.append('N')
			# black knight
			elif pos[i]==12:
				efen.append('n')
			# white bishop
			elif pos[i]==3:
				efen.append('B')
			# black bishop
			elif pos[i]==13:
				efen.append('b')
			# white rook
			elif pos[i]==4:
				efen.append('R')
			# black rook
			elif pos[i]==14:
				efen.append('r')
			# white queen
			elif pos[i]==5:
				efen.append('Q')
			# black queen
			elif pos[i]==15:
				efen.append('q')
			# white king
			elif pos[i] in [6,7,8,9]:
				efen.append('K')
			# black rook
			elif pos[i]in [16,17,18,19]:
				efen.append('k')		
		efen.append(' ')

		# Color to move
		if self.state[-1][1]==0:
			clr_to_move='w'
		else:
			clr_to_move='b'
		efen.append(clr_to_move+' ')

		# Get castling rights from king type
		# White castling rights
		if w_pieces[6]!=[]:
			w_cstl='KQ'
		elif w_pieces[7]!=[]:
			w_cstl='K'
		elif w_pieces[8]!=[]:
			w_cstl='Q'
		else:
			w_cstl=''
		# Black castling rights
		if b_pieces[16]!=[]:
			b_cstl='kq'
		elif b_pieces[17]!=[]:
			b_cstl='k'
		elif b_pieces[18]!=[]:
			b_cstl='q'
		else:
			b_cstl=''
		# If no one can castle, use '-'
		if w_cstl=='' and b_cstl=='':
			cstl='-'
		# Else just concatenate
		else:
			cstl=w_cstl+b_cstl
		efen.append(cstl+' ')

		# En passant square
		if self.state[-1][2]==None:
			en_passant='-'
		else:
			en_passant=util.sqr2coord(self.state[-1][2])
		efen.append(en_passant+' ')

		# Half move
		half_move_cnt = str(self.state[-1][3])
		efen.append(half_move_cnt+' ')

		# Total move counter
		# Just take the length of the state vector divided by two
		move_cnt=str(int(len(self.state)/2))
		efen.append(move_cnt)

		return util.efen2fen(''.join(efen))

	def print_moves(self,n_col):
		moves=self.get_moves()
		print('Moves----')
		for i in range(len(moves)):
			origin_pc=self.state[-1][0][moves[i][0]]
			origin_sqr=moves[i][0]
			tg_sqr=moves[i][1]
			# Normal move
			if tg_sqr<64:
				move_str = '('+util.sqr2coord(origin_sqr)+') '+piece_dict[origin_pc]+util.sqr2coord(tg_sqr)
			# Kingside castling
			elif tg_sqr==64:
				move_str='('+util.sqr2coord(origin_sqr)+') '+piece_dict[origin_pc]+'KS'
			# Queen castling
			elif tg_sqr==65:
				move_str='('+util.sqr2coord(origin_sqr)+') '+piece_dict[origin_pc]+'QS'

			print('  '+"{:02d}".format(i)+'.',move_str+' ',end='')
			if i%n_col==n_col-1:
				print()
		print('')

	def print_pseudo_moves(self,n_col):
		moves=self.get_pseudo_moves()
		print('Pseudo moves----')
		for i in range(len(moves)):
			origin_pc=self.state[-1][0][moves[i][0]]
			origin_sqr=moves[i][0]
			tg_sqr=moves[i][1]
			# Normal move
			if tg_sqr<64:
				move_str = '('+util.sqr2coord(origin_sqr)+') '+piece_dict[origin_pc]+util.sqr2coord(tg_sqr)
			# Kingside castling
			elif tg_sqr==64:
				move_str='('+util.sqr2coord(origin_sqr)+') '+piece_dict[origin_pc]+'KS'
			# Queen castling
			elif tg_sqr==65:
				move_str='('+util.sqr2coord(origin_sqr)+') '+piece_dict[origin_pc]+'QS'

			print('  '+"{:02d}".format(i)+'.',move_str+' ',end='')
			if i%n_col==n_col-1:
				print()
		print('')

	def print_board(self):
		fen=self.get_fen()
		util.print_fen(fen)

	def perft(self,depth,first_call=True,start_time=time.time()):
		"""
		PERFormance Test, move path enumeration function. Used for move generation debugging.
		"""
		assert depth>0, "Depth must be bigger than 0"
		nodes=0
		moves=self.get_moves()
		if depth==1:
			return len(moves)

		for move in moves:
			self.make_move(move)
			count=self.perft(depth-1,first_call=False)
			nodes+=count
			if first_call==True:
				print(move, count, 'at',time.time() - start_time)
			self.unmake_move()
		return nodes

	# Criar lazy perft, que verifica a legalidade dos movimentos conforme eles aparecem, se ilegal, retorna flag de ilegal que anula o último movimento
	def lazy_perft(self, depth, first_call=True, start_time=time.time()):
		"""
		PERFormance Test, move path enumeration function. Used for move generation debugging.
		Lazy perft checks for legal moves on the go. If any answer gives an ilegal position, cancel last move.
		"""
		assert depth>0, "Depth must be bigger than 0"
		nodes=0
		if depth==1:
			# Only get legal moves for depth==1
			moves=self.get_moves()
			return (len(moves), True)

		# Otherwise just generate pseudolegal moves
		moves=self.get_pseudo_moves()
		for move in moves:
			# If castling, only do it if known to be legal
			if move[1] in [64,65]:
				if self.is_castling_legal(move):
					
					self.make_move(move)
					count=self.lazy_perft(depth-1,first_call=False)
					nodes+=count
					if first_call==True:
						print(move, count, 'at',time.time() - start_time)
					self.unmake_move()
			else:
				# Make move
				self.make_move(move)

				# Check legality: Look for no kings
				has_w_king=False
				for i in [6,7,8,9]:
					if self.sup_data[-1][0][i]!=[]:
						has_w_king=True
				has_b_king=False
				for i in [16,17,18,19]:
					if self.sup_data[-1][1][i]!=[]:
						has_b_king=True

				# If ilegal, return legal=False and count==0
				if (not has_w_king) or (not has_b_king):
					ilegal=True
					return (0,False)
				# If legal, proceed with perft
				#print('return',self.lazy_perft(depth-1,first_call=False))
				count, legal=self.lazy_perft(depth-1,first_call=False)
				if legal:
					nodes+=count
				# If perft returned ilegal, stop count and return 0 nodes for this move (it is ilegal, after all!)
				else:
					return (0, True)

				if first_call==True:
					print(move, count, 'at',time.time() - start_time)
				self.unmake_move()

		return (nodes, legal)

	def appraise_moves(self,move_list):
		pass

def main_func():

	fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
	frame=get_frame_from_fen(fen)

	test_board=board()
	test_board.set([frame])

	moves=test_board.get_moves()

	#test_board.print_board()
	test_board.print_moves(8)

	start_time = time.time()

	node_count,_=test_board.lazy_perft(5)
	#node_count=test_board.perft(4)
	print(node_count,'total nodes')

	# test_board.make_move(moves[3])

	# util.print_fen(test_board.get_fen())

	# print(test_board.get_pseudo_moves())

	print("Took", time.time() - start_time, "to run")
	print(node_count/(time.time() - start_time),'nps with bulk counting')

import cProfile

if __name__=='__main__':
	#cProfile.run('main_func()')
	main_func()
	# fen='rnbqk2r/3p4/2p5/8/8/2P5/3P4/RNBQK2R w KQkq - 0 1'
	# frame=get_frame_from_fen(fen)
	# test_board=board()
	# test_board.set([frame])
	# test_board.get_moves()




	# moves=test_board.get_pseudo_moves()
	# test_board.print_board()
	# test_board.print_pseudo_moves(13)
	# print(test_board.sup_data)
	# move=moves[2]
	# test_board.make_move(move)
	# print('made move',move)

	# test_board.print_board()
	# test_board.print_pseudo_moves(13)
	# [print(u) for u in test_board.sup_data]
	# test_board.unmake_move()
	# print('unmade move')

	# [print(u) for u in test_board.sup_data]
