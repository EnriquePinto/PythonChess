# Pawn move generations

def gen_pawn_moves(sqr,clr,fr_bb,en_bb,en_pas_sqr=None):
	blockers_bb=fr_bb|en_bb
	#str_blocker_bb='{:064b}'.format(blockers_bb)
	#captures_bb='{:064b}'.format(en_bb)
	moves=[]
	# Separate by color
	if clr==0:
		# Normal move not blocked
		#if str_blocker_bb[sqr-8]!='1':
		if 1&(blockers_bb>>(63-(sqr-8)))!=1:
			moves.append(sqr-8)
		# Captures (with edge exceptions)
		# Edge exceptions
		if sqr%8==0:
			#if captures_bb[sqr-7]=='1' or sqr-7==en_pas_sqr:
			if 1&(en_bb>>(63-(sqr-7)))==1 or sqr-7==en_pas_sqr:
				moves.append(sqr-7)

		elif sqr%8==7:
			#if captures_bb[sqr-9]=='1' or sqr-9==en_pas_sqr:
			if 1&(en_bb>>(63-(sqr-9)))==1 or sqr-9==en_pas_sqr:
				moves.append(sqr-9)
		# "Middle" pawns
		else:
			#if captures_bb[sqr-7]=='1' or sqr-7==en_pas_sqr:
			if 1&(en_bb>>(63-(sqr-7)))==1 or sqr-7==en_pas_sqr:
				moves.append(sqr-7)
			#if captures_bb[sqr-9]=='1' or sqr-9==en_pas_sqr:
			if 1&(en_bb>>(63-(sqr-9)))==1 or sqr-9==en_pas_sqr:
				moves.append(sqr-9)
	else:
		# Single move blocked
		#if str_blocker_bb[sqr+8]!='1':
		if 1&(blockers_bb>>(63-(sqr+8)))!=1:
			moves.append(sqr+8)
		# Captures (with edge exceptions)
		# Edge exceptions
		if sqr%8==0:
			#if captures_bb[sqr+9]=='1' or sqr+9==en_pas_sqr:
			if 1&(en_bb>>(63-(sqr+9)))==1 or sqr+9==en_pas_sqr:
				moves.append(sqr+9)			
		elif sqr%8==7:
			#if captures_bb[sqr+7]=='1' or sqr+7==en_pas_sqr:
			if 1&(en_bb>>(63-(sqr+7)))==1 or sqr+7==en_pas_sqr:
				moves.append(sqr+7)
		# "Middle" pawns
		else:
			#if captures_bb[sqr+7]=='1' or sqr+7==en_pas_sqr:
			if 1&(en_bb>>(63-(sqr+7)))==1 or sqr+7==en_pas_sqr:
				moves.append(sqr+7)
			#if captures_bb[sqr+9]=='1' or sqr+9==en_pas_sqr:
			if 1&(en_bb>>(63-(sqr+9)))==1 or sqr+9==en_pas_sqr:
				moves.append(sqr+9)
	return moves

def gen_pawn_first_moves(sqr,clr,fr_bb,en_bb):
	# Double move only if not blocked
	blockers_bb=fr_bb|en_bb
	#str_blocker_bb='{:064b}'.format(blockers_bb)
	#captures_bb='{:064b}'.format(en_bb)
	moves=[]
	# Separate by color
	if clr==0:
		# Single move blocked
		#if str_blocker_bb[sqr-8]=='1':
		if 1&(blockers_bb>>(63-(sqr-8)))==1:
			pass
		else:
			# Both moves free
			#if str_blocker_bb[sqr-16]=='0':
			if 1&(blockers_bb>>(63-(sqr-16)))==0:
				moves.append(sqr-16)
				moves.append(sqr-8)
			# Only single move free
			else:
				moves.append(sqr-8)
		# Captures (with edge exceptions)
		# Edge exceptions
		if sqr==48:
			#if captures_bb[sqr-7]=='1':
			if 1&(en_bb>>(63-(sqr-7)))==1:
				moves.append(sqr-7)			
		elif sqr==55:
			#if captures_bb[sqr-9]=='1':
			if 1&(en_bb>>(63-(sqr-9)))==1:
				moves.append(sqr-9)
		# "Middle" pawns
		else:
			#if captures_bb[sqr-7]=='1':
			if 1&(en_bb>>(63-(sqr-7)))==1:
				moves.append(sqr-7)
			#if captures_bb[sqr-9]=='1':
			if 1&(en_bb>>(63-(sqr-9)))==1:
				moves.append(sqr-9)
	else:
		# Single move blocked
		#if str_blocker_bb[sqr+8]=='1':
		if 1&(blockers_bb>>(63-(sqr+8)))==1:
			pass
		else:
			# Both moves free
			#if str_blocker_bb[sqr+16]=='0':
			if 1&(blockers_bb>>(63-(sqr+16)))==0:
				moves.append(sqr+16)
				moves.append(sqr+8)
			# Only single move free
			else:
				moves.append(sqr+8)
		# Captures (with edge exceptions)
		# Edge exceptions
		if sqr==8:
			#if captures_bb[sqr+9]=='1':
			if 1&(en_bb>>(63-(sqr+9)))==1:
				moves.append(sqr+9)			
		elif sqr==15:
			#if captures_bb[sqr+7]=='1':
			if 1&(en_bb>>(63-(sqr+7)))==1:
				moves.append(sqr+7)
		# "Middle" pawns
		else:
			#if captures_bb[sqr+7]=='1':
			if 1&(en_bb>>(63-(sqr+7)))==1:
				moves.append(sqr+7)
			#if captures_bb[sqr+9]=='1':
			if 1&(en_bb>>(63-(sqr+9)))==1:
				moves.append(sqr+9)
	return moves



# Promotions are to be handled by the board object: If a pawn move reaches board edge then add all promotion moves to the list
