import random
from itertools import product, combinations
from copy import copy

from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
session = WolframLanguageSession()



arrays = []

comb_behavior = {}

def pareto_dominates(new_val, old_val):
	failed = False
	reallyGained = False
	for player in range(players):
		if new_val[player] < old_val[player]:
			failed = True
		elif new_val[player] > old_val[player]:
			reallyGained = True

	return reallyGained and not failed


players = 3

all_pairs = []

for comb in combinations([i for i in range(players)], 2):
	pair_list = [i for i in comb]
	pair_list_r = copy(pair_list)
	pair_list_r.reverse()
	all_pairs.append(pair_list)
	all_pairs.append(pair_list_r)

items = 6
all_combs = [item for item in product([i for i in range(players)], repeat=items)]

random.shuffle(all_combs)

efx_combs = []
valuations = {0: [-1, -0.6875, -0.22916666666666666, -0.16666666666666666, -0.4166666666666667, -0.6041666666666666], 1: [-1, -3.375, -2, -2.625, -0.5, -3.25], 2: [-1, -3, -1, -3.5, -3.625, -3.875]}


all_zeros = [0 for j in range(items)]


for comb in all_combs:
	all_poss_j = []
	isAlreadyJealous = False
	for pair in all_pairs:
		side1_items = []
		side2_items = []
		for i in range(len(comb)):
			if comb[i] == pair[0]:
				side1_items.append(i)
			elif comb[i] == pair[1]:
				side2_items.append(i)
		val_side2 = 0
		for side2_item in side2_items:
			val_side2 += valuations[pair[0]][side2_item]
		for j in range(len(side1_items)):
			val_side1 = 0
			for side1_item in (side1_items[:j] + side1_items[j+1:]):
				val_side1 += valuations[pair[0]][side1_item]

			if val_side2 > val_side1:
				isAlreadyJealous = True



	if isAlreadyJealous == False:
		efx_combs.append(comb)

efx_valuations = []
for comb in efx_combs:
	new_val = []
	for player in range(players):
		player_value = 0
		for elem_ind in range(len(comb)):
			if comb[elem_ind] == player:
				player_value += valuations[player][elem_ind]

		new_val.append(player_value)
	efx_valuations.append([new_val, comb])

#print(efx_valuations)
#print(efx_combs)

old_efx_valuations = copy(efx_valuations)

print("All EFX Valuations: {}".format(old_efx_valuations))
for comb in all_combs:
	new_val = []
	for player in range(players):
		player_value = 0
		for elem_ind in range(len(comb)):
			if comb[elem_ind] == player:
				player_value += valuations[player][elem_ind]

		new_val.append(player_value)

	new_efx_valuations = []
	for e_val, e_comb in efx_valuations:
		if not pareto_dominates(new_val, e_val):
			new_efx_valuations.append([e_val, e_comb])
		#else:
		#	print("EFX comb {} with values {} superseded by {} due to combination {}".format(e_comb, e_val, new_val, comb))
	efx_valuations = new_efx_valuations
	if efx_valuations == []:
		print("REALLY??")
		import pdb
		pdb.set_trace()
print("EFX+PO Valuations: {}".format(efx_valuations))
max_ev = 0
ev_instance = []
for ev in old_efx_valuations:
	if sum(ev[0]) > max_ev:
		max_ev = sum(ev[0])
		ev_instance = ev

print("MAX {}, {}".format(max_ev, ev_instance))

import pdb
pdb.set_trace()
