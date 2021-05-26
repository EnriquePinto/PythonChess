# Alpha-beta pruning and other optimization methods file for the PythonChess project

import evaluation,brd
import numpy as np

# board_state is a tuple of (efen_hist, (board lvl last_move, last_move_was_check?))

def alpha_beta(board_state, depth, alpha, beta, max_player):
	# If the depth is zero, or if the node is a draw or win, then return the heuristic value of node
	if depth==0 or evaluation.is_over(board_state[0],board_state[1][1]):
		#print('child eval:',evaluation.std_eval(board_state[0], board_state[1]))
		return evaluation.std_eval(board_state[0], board_state[1])
	# If maximizing player
	if max_player:
		value=-np.inf
		# Sets up board at current node to generate child nodes
		node_board=brd.board()
		node_board.set(board_state[0][-1],reset_hist=True)
		node_board.efen_hist=board_state[0]
		moves=node_board.gen_moves() # returns ((piece obj, pc lvl move) tuple, is check?) tuple
		for move in moves:
			child_efen=node_board.preview_move(move[0])
			child_board_state=(node_board.efen_hist+[child_efen], move) # Board state = (child efen_hist, (board lvl last_move, last_move_was_check?))
			value=max(value, alpha_beta(child_board_state, depth-1, alpha, beta, False))
			alpha=max(alpha,value)
			#print('alpha',alpha,'| beta',beta,'| value',value, '| max_player')
			if alpha>= beta:
				# Branch beta cutoff
				break
		return value
	# Else, minimizing player
	else:
		value=np.inf
		# Sets up board at current node to generate child nodes
		node_board=brd.board()
		node_board.set(board_state[0][-1],reset_hist=True)
		node_board.efen_hist=board_state[0]
		moves=node_board.gen_moves() # returns ((piece obj, pc lvl move) tuple, is check?) tuple
		for move in moves:
			child_efen=node_board.preview_move(move[0])
			child_board_state=(node_board.efen_hist+[child_efen], move) # Board state = (child efen_hist, (board lvl last_move, last_move_was_check?))
			value=min(value, alpha_beta(child_board_state, depth-1, alpha, beta, True))
			beta=min(beta,value)
			#print('alpha',alpha,'| beta',beta,'| value',value,'| min player')
			if alpha>= beta:
				# Branch alpha cutoff
				break
		return value