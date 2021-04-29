# Board class file

import util
import pcs

start_fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

class board:

	def set(self, efen, fen_in=False):
		if fen_in:
			self.fen=fen
			# Expand FEN and instantiate a piece in each position
			self.efen=util.fen2efen(fen)
		else:
			self.efen=efen
		# Interprets the EFEN code
		self.exp_pos, self.clr_to_move, self.castl_avl, self.en_pas_targ, self.half_mov_clk, self.mov_clk = util.read_fen(self.efen)
		# Piece list
		self.white_pieces=[]
		self.black_pieces=[]
		for i in range(64):
			# White
			if self.exp_pos[i]=='P':
				self.white_pieces.append(pcs.pawn(0,i))
			elif self.exp_pos[i]=='R':
				self.white_pieces.append(pcs.rook(0,i))
			elif self.exp_pos[i]=='B':
				self.white_pieces.append(pcs.bishop(0,i))
			elif self.exp_pos[i]=='N':
				self.white_pieces.append(pcs.knight(0,i))
			elif self.exp_pos[i]=='Q':
				self.white_pieces.append(pcs.queen(0,i))
			elif self.exp_pos[i]=='K':
				self.white_pieces.append(pcs.king(0,i))
			# Black
			elif self.exp_pos[i]=='p':
				self.black_pieces.append(pcs.pawn(1,i))
			elif self.exp_pos[i]=='r':
				self.black_pieces.append(pcs.rook(1,i))
			elif self.exp_pos[i]=='b':
				self.black_pieces.append(pcs.bishop(1,i))
			elif self.exp_pos[i]=='n':
				self.black_pieces.append(pcs.knight(1,i))
			elif self.exp_pos[i]=='q':
				self.black_pieces.append(pcs.queen(1,i))
			elif self.exp_pos[i]=='k':
				self.black_pieces.append(pcs.king(1,i))

	def avl_movs(self):
		# Returns moves in the format (piece_object,move)
		# "move" is a tuple: (target square, type of move)

		move_list=[]
		# Generate white moves if white is to move
		if self.clr_to_move=='w':
			for piece in self.white_pieces:
				for move in piece.avl_movs(self.efen):
					move_list.append((piece,move))

		#Else, generate black moves
		else:
			for piece in self.black_pieces:
				for move in piece.avl_movs(self.efen):
					move_list.append((piece,move))

		return move_list

	def print_avl_moves(self):
		for move in self.avl_movs():
			print(util.translate_move(move), end='; ')
		print('')

	def make_move(self, move):
		new_move=move[0].move_piece(move[1],self.efen)
		self.set(new_move)
		return new_move

# A board object is to be used in every piece object instance to identify legal moves and checks!
# 	-The actual board object where moves will be made is to be called 'main_board'
# 	-The local instance of a board object in a piece object is to be called 'local_board'

# Each piece move output is a tuple: (target square, type of move, is check?)
# Move types: 0 = normal; 1 = capture; 2 = double pawn move; 3 = en passant; 
#			  4/5/6/7 = promotion to queen/rook/knight/bishop; 14/15/16/17 = capture and promotion to queen/rook/knight/bishop
#			  8/9 = castle short/long
