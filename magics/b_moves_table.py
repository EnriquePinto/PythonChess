# File for pseudo legal, square based bitboard, bishop move table generation. 
# Explained sources: http://vicki-chess.blogspot.com/2013/04/magics.html ; https://rhysre.net/fast-chess-move-generation-with-magic-bitboards.html

# 1. Pick some random 64-bit number, call it magic.
# 2. Get all the variations for the piece on the square (i.e. for example bb 2,3 and 4).
# 3. Create a database of size 2^bits (starting of with the number of bits in the original attack-board, i.e. bb 1).
# 4. For each attack variation:
# 	a. Calculate the result bitboard for the variation, i.e. bb 6 for bb 2,3 and 4. 
# 	b. Create an index by multiplying variation with magic and shift it right with 64 - bits.
# 	c. If database[index] is not 0 and the result board stored there is not compatible with variation, then we have a clash and we have to try a new magic number.
# 	d. Otherwise, we store the result bitboard for variation at database[index].
# 5. If the loop ends with no clashes, then magic is a valid magic number for the piece on a1

# Magic bitboards exclude edge squares and the output bitboard treats them as unoccupied. The output move set  bits are only kept if they are 1 in the output and zero in the friendly blocker bitboard (A^~B).
# The output table moves can initially be of the size of the possible blocker arrangements. Ideally it is smaller: use trial and error to try and find more efficient magics

import random, math
import numpy as np
import pickle


from pcs import bishop

edge_mask = 0x7E7E7E7E7E7E00

# Function for helping the visualization of bitboards
def viz_bb(bb):
	string_buf='{:064b}'.format(bb)
	for i in range(64):
		if i%8==0 and i!=0:
			print()
			print(string_buf[i],end='')
		else:
			print(string_buf[i],end='',sep='')
	print('\n----')

# Function for convering binary list of length 64 to integer
def b64_2_int(list):
	acum=0x0
	for i in range(64):
		acum+=int(list[i]*2**(63-i))
	return acum

# Get hamming weight from integer
def hamming_weight(x):
	bin_str=bin(x)[2:]
	cnt=0
	for bit in bin_str:
		if bit=='1':
			cnt+=1
	return cnt

# From an int, returns a string with left side zero fill to target length
def zero_fill(x,target_len):
	bin_str=bin(x)[2:]
	missing_len=target_len-len(bin_str)
	left_fill=''
	for i in range(missing_len):
		left_fill+='0'
	return left_fill+bin_str



# Function for generating attack masks
def gen_att_masks():	
	attack_list=[]
	for i in range(64):
		square_efen=[]
		attack_set_bishop=bishop(color=0, sqr=i)
		# Set up empty board with bishop in square i
		for j in range(64):
			if j!= i:
				square_efen.append('u')
			else:
				square_efen.append('B')
		square_efen=''.join(square_efen)
		square_efen=square_efen+' w - - 0 1'
		# Get bishop controlled squares
		_,ctrl_sqrs=attack_set_bishop.avl_movs(square_efen, return_ctrl_sqr=True)
		attack_set=np.zeros(64)
		for j in range(64):
			if j in ctrl_sqrs:
				attack_set[j]=1
		# Add to list of attack set masks
		attack_list.append(attack_set)

	# Convert list of binaries into int masks
	attack_masks=[]
	for attack in attack_list:
		attack_masks.append(b64_2_int(attack))
	return attack_masks

def gen_block_sets(attack_masks):
	# For each square attack set generate relevant blocker sets
	blocker_sets=[] # Contains a list for each square, containing all possible blocker arrangements relevant for that square
	for i in range(64):
		# Get relevant blocker squares
		rel_sqrs=[]
		for j in range(64):
			if '{:064b}'.format(attack_masks[i]&edge_mask)[j]=='1':
				rel_sqrs.append(j)
		# How many blocker squares?
		n_bits=len(rel_sqrs)
		# Get all possible blocker arrangements (i.e. count in binary to n_bits)	
		blocker_group=[]
		for j in range(2**n_bits):
			blockers=['0' for ii in range(64)]
			bin_j=zero_fill(j,n_bits)
			for k in range(n_bits):
				blockers[rel_sqrs[k]]=bin_j[k]
			blocker_group.append(''.join(blockers))
		blocker_sets.append(blocker_group)
	return blocker_sets

def gen_min_move_sets(blocker_sets):
	# Returns distinct move sets of each square
	# (initially of the size of the blocker arrangements, then smaller)
	move_sets=[] # List of pseudolegal move bitboards for each square given each blocker arangement of that square
	for i in range(64):
		valid_moves_list=[] # List of distinct pseudolegal move bitboards for THIS square
		test_bishop=bishop(color=0, sqr=i)
		for blockers in blocker_sets[i]:
			# Create a efen for this blocker arrangement with enemy pawns for blockers
			blockers_efen=['p' if blockers[j]=='1' else 'u' for j in range(64)]
			blockers_efen[i]='B'
			blockers_efen=''.join(blockers_efen)+' w - - 0 1'
			# Compute pseudolegal moves and convert bitboard to int
			_,ctrl_sqrs=test_bishop.avl_movs(blockers_efen, return_ctrl_sqr=True)
			moves=[1 if j in ctrl_sqrs else 0 for j in range(64)]
			moves=b64_2_int(moves)
			# Add to list if it is not in list
			if moves not in valid_moves_list:
				valid_moves_list.append(moves)
		move_sets.append(valid_moves_list)
	return move_sets

def gen_move_sets(blocker_sets):
	# Returns distinct move sets of each square
	# (initially of the size of the blocker arrangements, then smaller)
	move_sets=[] # List of pseudolegal move bitboards for each square given each blocker arangement of that square
	for i in range(64):
		valid_moves_list=[] # List of distinct pseudolegal move bitboards for THIS square
		test_bishop=bishop(color=0, sqr=i)
		for blockers in blocker_sets[i]:
			# Create a efen for this blocker arrangement with enemy pawns for blockers
			blockers_efen=['p' if blockers[j]=='1' else 'u' for j in range(64)]
			blockers_efen[i]='B'
			blockers_efen=''.join(blockers_efen)+' w - - 0 1'
			# Compute pseudolegal moves and convert bitboard to int
			_,ctrl_sqrs=test_bishop.avl_movs(blockers_efen, return_ctrl_sqr=True)
			moves=[1 if j in ctrl_sqrs else 0 for j in range(64)]
			moves=b64_2_int(moves)
			# Add to list
			valid_moves_list.append(moves)
		move_sets.append(valid_moves_list)
	return move_sets

def get_bishop_magics(blocker_sets, min_max_bits, n_tries=1000000):
	# Generate a magic for each square
	database=[]
	for i in range(64):
		# Init database of (move_list, magic number, bits) tuples for each square
		# Prepare bishop 
		test_bishop=bishop(color=0, sqr=i) 
		# Leave for other function: Start from the more compressed table and go towards the more expansive table
		#for bits in range(min_max_bits[i][0],min_max_bits[i][1]+1):
		# For now, use max bits
		for bits in [min_max_bits[i][1]]:
			# Flag to see if we found a magic of size bits
			found_magic=False
			for j in range(int(n_tries)):
				# Fail flag starts false, is raised if clash occurs
				fail_flag=False
				# Generate a 64 bit magic number candidate with few nonzero bits
				magic_cand=random.getrandbits(64)&random.getrandbits(64)&random.getrandbits(64)
				# Start with empty move list of size 2^bits every try
				moves_list=[None] * (2**bits)
				# Go through each blocker arrangement for this square
				for k in range(len(blocker_sets[i])):
					moves=move_sets[i][k]
					# Get index from magic number and bitshift
					idx=((int(blocker_sets[i][k],2)*magic_cand)&0xFFFFFFFFFFFFFFFF	)>>(64-bits)

					# If database[index] is not None and the result board stored there is not compatible with variation, then we have a clash and we have to try a new magic number.
					if moves_list[idx]!=None and moves_list[idx]!=moves:
						# Clash!
						fail_flag=True
						break
					else:
						# Otherwise, store moves in the database
						moves_list[idx]=moves
				# If clash didn't occur, then we found a magic of size 'bits'
				if fail_flag==False:
					found_magic=True
					# Store: move sets, magic number, bits
					database.append((moves_list, magic_cand, bits))
					print('n={} with {} bits, max of {} bits'.format(i,bits,min_max_bits[i][1]))
					# Break out of 'tries' loop
					break
			if found_magic==True:
				# Stop right after we found a magic of size bits, since bits will only increase here
				break
		# If we didn't find a magic for this number, report error
		assert found_magic==True, 'ERROR: Did not find any magic for n={}'.format(i) 
	return database


if __name__=="__main__":
	# Generate attack set masks (for each square)
	attack_masks=gen_att_masks()
	# Generate relevant blocker arrangements (for each square)
	blocker_sets=gen_block_sets(attack_masks)
	# Find out what the minimal move set table looks like and their sizes
	smallest_move_sets=gen_min_move_sets(blocker_sets)
	# Precaulculate move sets for each square and blocker arrangement
	move_sets=gen_move_sets(blocker_sets)
	# Get sizes of the most compressed tables and the largest addressable table for each square
	min_max_move_set_sizes=[(len(smallest_move_sets[i]),len(blocker_sets[i])) for i in range(64)] # Tuples (min size, max size)
	# Calculate how many bits in the max and min move tables
	min_max_bits=[(math.ceil(math.log(x[0],2)), math.ceil(math.log(x[1],2))) for x in min_max_move_set_sizes]

	# Calculate the magic numbers and bitboards
	database=get_bishop_magics(blocker_sets, min_max_bits, n_tries=1000000)

	pickle.dump( database, open( "bishop_magics.p", "wb" ) )



