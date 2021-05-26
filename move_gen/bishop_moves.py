# Bishop move generation file from the magic bitboards

import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
# Add parent directory to path
sys.path.insert(0, parentdir) 

import pickle
import numpy as np

# To calculate attack masks run commented code below
# from pcs import bishop
# from magics.b_moves_table import *
# att_masks=gen_att_masks()


# Define edge mask
edge_mask = 0x7E7E7E7E7E7E00
# Load bishop magics
magic_tuples=pickle.load( open( parentdir+'\\magics\\bishop_magics.p', "rb" ) )


# Precalculated bishop attack masks
att_masks=[18049651735527937, 45053622886727936, 22667548931719168, 11334324221640704, 5667164249915392, 2833579985862656,
 1416240237150208, 567382630219904, 4611756524879479810, 11529391036782871041, 5764696068147249408, 2882348036221108224,
 1441174018118909952, 720587009051099136, 360293502378066048, 144117404414255168, 2323857683139004420, 1197958188344280066,
 9822351133174399489, 4911175566595588352, 2455587783297826816, 1227793891648880768, 577868148797087808, 288793334762704928,
 1161999073681608712, 581140276476643332, 326598935265674242, 9386671504487645697, 4693335752243822976, 2310639079102947392,
 1155178802063085600, 577588851267340304, 580999811184992272, 290500455356698632, 145390965166737412, 108724279602332802,
 9241705379636978241, 4620711952330133792, 2310355426409252880, 1155177711057110024, 290499906664153120, 145249955479592976,
 72625527495610504, 424704217196612, 36100411639206946, 9241421692918565393, 4620710844311799048, 2310355422147510788,
 145249953336262720, 72624976676520096, 283693466779728, 1659000848424, 141017232965652, 36099303487963146, 9241421688590368773,
 4620710844295151618, 72624976668147712, 283691315142656, 1108177604608, 6480472064, 550848566272, 141012904249856, 36099303471056128,
 9241421688590303744]

def gen_bishop_moves(sqr, fr_bb, en_bb): #square, friend occupancy bitboard, enemy occupancy bitboard
	# Total blocker set is the sum of both blocker sets and remove piece from bitboard
	blockers=fr_bb|en_bb&(0xFFFFFFFFFFFFFFFF-2**(63-sqr))
	# Calculate occupancy squares with the masks
	occupancy=att_masks[sqr]&blockers&edge_mask
	# Calculate index for magic bitboard
	magic=magic_tuples[sqr]
	idx=((occupancy*magic[1])&0xFFFFFFFFFFFFFFFF)>>(64-magic[2])
	
	# Try 1&(bb >> (63-i)); instead of bb_str[i]
	# Retrieve moves from magic bitboard table and remove own captures
	avl_moves_bb=magic[0][idx]&(~fr_bb)

	# Return list of destination squares
	move_list=[]
	for i in range(64):
		if 1&(avl_moves_bb>>(63-i))==1:
			move_list.append(i)

	return move_list
