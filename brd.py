# Board class file

import util
import pcs
import numpy as np

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

	def avl_movs(self,check_legality=True, extra_output=False, output_ctrl_sqrs=False):
		# Returns moves in the format (piece_object,move)
		# "move" is a tuple: (target square, type of move)

		move_list=[]
		controlled_list=[]

		# Generate white moves if white is to move
		if self.clr_to_move=='w':
			for piece in self.white_pieces:
				piece_moves, piece_controlled_sqrs = piece.avl_movs(self.efen, return_ctrl_sqr=True)
				# Actual moves
				for move in piece_moves:
					move_list.append((piece,move))
				# Squares that are controlled (excluding captures and moves)
				for square in piece_controlled_sqrs:
					controlled_list.append(square)

		# Else, generate black moves
		else:
			for piece in self.black_pieces:
				piece_moves, piece_controlled_sqrs = piece.avl_movs(self.efen, return_ctrl_sqr=True)
				# Actual moves
				for move in piece_moves:
					move_list.append((piece,move))
				# Squares that are controlled (excluding captures and moves)
				for square in piece_controlled_sqrs:
					controlled_list.append(square)

		# Use the argument (check_legality=False) in avl_movs to avoid infinite loops during this step!
		if check_legality:
			ilegal_list=[]
			legal_list=[]
			# Check for ilegal moves and remove them
			# Creates new board to check for ilegal moves
			test_brd = board()
			# Goes through each move and checks if any of them allow a position without a king
			for move in move_list:
				# Get position after move
				test_brd.set(self.efen)
				new_efen=test_brd.make_move(move)
				oponent_answers=test_brd.avl_movs(check_legality=False)
				# Goes through each oponent answer and checks for a position without either king
				# Set ilegal flag as false, if move is deemed ilegal then set flag
				ilegal_flag=False
				for answer in oponent_answers:
					ans_pos,_,_,_,_,_ = util.read_fen(test_brd.preview_move(answer))
					# If any king is missing remove the move from list
					if ('k' not in ans_pos) or ('K' not in ans_pos):
						ilegal_list.append(move)
						ilegal_flag=True
						break
				# If no king capture was found, append to legal list
				if not ilegal_flag:
					legal_list.append(move)
			# Return extra information if requested
			if extra_output:
				if output_ctrl_sqrs:
					return legal_list, controlled_list, ilegal_list, len(legal_list)
				else:
					return legal_list, ilegal_list, len(legal_list)
			else:
				if output_ctrl_sqrs:
					legal_list, controlled_list
				else:
					return legal_list

		# If check_legality==False, then generate pseudo legal moves
		if output_ctrl_sqrs:
			return move_list,  controlled_list
		else:
			return move_list

	def print_avl_moves(self, n_col=5):
		cnt = 0
		for move in self.avl_movs():
			print('  '+"{:02d}".format(cnt)+'.',util.translate_move(move),end='')
			if cnt%n_col==4:
				print()
			cnt+=1
		print('')

	def preview_move(self, move):
		"""
		Just return the move output without changing object attributes
		"""
		return move[0].move_piece(move[1],self.efen)

	def make_move(self, move):
		"""
		Make the move and update object attributes
		"""
		new_efen=move[0].move_piece(move[1],self.efen)
		self.set(new_efen)
		return new_efen

	def board_control(self):
		# Current player
		control_vec1=np.zeros(64)
		_,controlled_sqrs1 = self.avl_movs(output_ctrl_sqrs=True)
		for sqr in controlled_sqrs1:
			control_vec1[sqr]+=1
		# Save the current EFEN and switch who's to move
		saved_efen=self.efen
		exp_pos, clr_to_move, castl_avl, en_pas_targ, half_mov_clk, mov_clk = util.read_fen(self.efen)
		if clr_to_move=='w':
			clr_to_move='b'
		else:
			clr_to_move='w'
		new_efen=exp_pos+' '+clr_to_move+' '+castl_avl+' '+en_pas_targ+' '+half_mov_clk+' '+mov_clk
		self.set(new_efen)
		# Next player
		control_vec2=np.zeros(64)
		_,controlled_sqrs2 = self.avl_movs(output_ctrl_sqrs=True)
		for sqr in controlled_sqrs2:
			control_vec2[sqr]+=1

		# Reset self.efen
		self.set(saved_efen)

		# Identify which one is the black control and which is the white control
		if clr_to_move=='w':
			# Return white and black controlled squares
			return control_vec2, control_vec1
		else:
			# Return white and black controlled squares
			return control_vec1, control_vec2

	def print_control(self, ctrl_clr='a'):
		"""
		Prints board control for current board attribute
		"""
		w_ctrl, b_ctrl=self.board_control()

		if ctrl_clr=='w':
			control_vec=w_ctrl
		elif ctrl_clr=='b':
			control_vec=b_ctrl
		else:	
			control_vec=w_ctrl-b_ctrl

		print('')
		# Prints board
		for i in range(64):
			# New line conditional
			if control_vec[i]>=0:\
				print('|','\u0305',' ',int(control_vec[i]), end='', sep='')
			else:
				print('|','\u0305',int(control_vec[i]), end='', sep='')
			
			if (i)%8==7:
				print('|')

		print(' \u0305   \u0305   \u0305   \u0305   \u0305   \u0305   \u0305   \u0305    ')
		print('')


	def manual_move(self, move):
		"""
		Makes the move with: (origin, target, type)
		"""
		pass
# A board object is to be used in every piece object instance to identify legal moves and checks!
# 	-The actual board object where moves will be made is to be called 'main_board'
# 	-The local instance of a board object in a piece object is to be called 'local_board'

# Each piece move output is a tuple: (target square, type of move, is check?)
# Move types: 0 = normal; 1 = capture; 2 = double pawn move; 3 = en passant; 
#			  4/5/6/7 = promotion to queen/rook/knight/bishop; 14/15/16/17 = capture and promotion to queen/rook/knight/bishop
#			  8/9 = castle short/long
