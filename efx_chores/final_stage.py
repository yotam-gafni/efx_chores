import random
from itertools import product, combinations
from copy import copy

from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
session = WolframLanguageSession()

import time


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

def generate_valuation(base):
	variable_string = "{"
	variables = []
	constraint_string = ""
	constraints = []

	for item in range(items):
		variables.append("x{}".format(item))


	for elem in base:
		con_string = ""
		for item in range(items):
			if elem[item] == 1:
				con_string += "+ x{}".format(item)
			elif elem[item] == -1:
				con_string += "- x{}".format(item)
		constraints.append(con_string + " < 0")

	opt_goal = "5"

	constraint_string = "{" + ",".join(constraints) + "}"

	variable_string += ",".join(variables) + "}"

	lp_string = "Quiet[Maximize[" + opt_goal + ", " + constraint_string + "," + variable_string + "]]"

	is_feasible = session.evaluate(wlexpr(lp_string))

	valuation = []

	for item in range(items):
		if type(is_feasible[1][item][1]) == int:
			valuation.append(is_feasible[1][item][1])
		else:
			try:
				valuation.append(is_feasible[1][item][1][0] / is_feasible[1][item][1][1])
			except Exception as e:
				for i in range(1000):
					print("UNFEASIBLE CONSTRAINTS!!!!")
					return None


	return valuation


def reverse_comb(comb):
	new_comb = []
	for i in comb:
		new_comb.append(-i)

	return new_comb

def is_comb_in_base(comb, base):
	variable_string = "{"
	variables = []
	constraint_string = ""
	constraints = []
	item_constraints = ["" for j in range(len(comb))]
	for i in range(len(base)):
		variables.append("x{}".format(i))
		constraints.append("x{} >= 0".format(i))
		for j in range(len(comb)):
			if base[i][j] == 1:
				item_constraints[j] += "+ x{}".format(i)
			elif base[i][j] == -1:
				item_constraints[j] += " - x{}".format(i)


	opt_goal = item_constraints[0]
	for j in range(len(comb)):
		item_constraints[j] += " == {}".format(comb[j])

	all_constraints = item_constraints + constraints

	constraint_string = "{" + ",".join(all_constraints) + "}"

	variable_string += ",".join(variables) + "}"

	lp_string = "Quiet[Maximize[" + opt_goal + ", " + constraint_string + "," + variable_string + "]]"

	is_feasible = session.evaluate(wlexpr(lp_string))


	return type(is_feasible[0]) == int


#is_comb_in_base([0,0,1,-1,1,0],[[-1, 0, 0, 0, 0, 0], [0, -1, 0, 0, 0, 0], [0, 0, -1, 0, 0, 0], [0, 0, 0, -1, 0, 0], [0, 0, 0, 0, -1, 0], [0, 0, 0, 0, 0, -1], [1, -1, -1, 0, 0, 1], (1, -1, 1, -1, 0, 0), (-1, 1, 0, -1, 0, 1), [1, 0, -1, -1, 1, 1], [1, -1, -1, 1, 0, -1], [0, 0, -1, 0, 0, 1], [1, 1, -1, -1, -1, 1], [1, 0, -1, 0, 1, 0], [0, -1, -1, 1, 1, 0], (0, -1, -1, -1, -1, 1), (1, 1, -1, 0, 0, 0), (-1, 0, 0, -1, 1, 1), (-1, 1, -1, 1, 0, -1), (-1, 0, -1, 0, 0, 0), (-1, 1, 0, 0, 0, -1), (1, 1, 1, -1, -1, -1), (0, 0, 0, 0, -1, 1), (-1, 1, 0, -1, 0, 0), [0, 0, 1, -1, 1, 0], [0, 1, 1, -1, 0, -1], [0, -1, -1, 0, 0, -1], (-1, 1, 1, 1, 1, 0), [0, 1, 0, 0, 0, -1], [1, 0, -1, 1, 0, 0], [-1, 0, -1, 1, 1, 0], (0, 1, 1, -1, 0, 0), (0, 0, 1, -1, 0, -1), [1, -1, 1, 0, -1, 0], [1, -1, 0, 0, 1, 1], [0, 0, -1, 1, 1, 0], [0, 0, 1, 1, 1, 1], (0, -1, 0, -1, 0, 1), (-1, -1, -1, 1, 1, -1), [0, -1, -1, 1, -1, -1], [1, 0, 0, -1, -1, 0], (0, -1, 0, -1, 1, 0), [0, -1, -1, 0, -1, 1], [1, -1, 1, 1, 0, -1], [-1, 1, 0, 0, -1, 1], (1, 1, 0, -1, -1, 0), (-1, -1, -1, 0, 0, 1), [-1, 0, 0, 0, -1, -1], [-1, 1, 1, -1, 1, 1], [1, 0, -1, 0, 0, 0], [0, -1, -1, 0, -1, 0], (0, 0, 1, 0, 1, -1), (1, -1, 1, 0, 1, -1), (1, 1, 1, 1, 1, -1), [-1, 1, 1, 1, 0, -1], (-1, -1, -1, 1, 1, 0), (-1, -1, 0, 1, -1, -1), (1, 1, -1, 1, 0, -1), (-1, 0, 0, 1, 0, 1), [1, -1, -1, 1, 0, 0], [0, 1, -1, 0, 0, -1], [1, 1, 1, -1, 0, 0], (-1, -1, 1, 0, 0, 0), (1, 0, -1, 0, 1, -1), (0, -1, 1, 1, -1, -1), (0, -1, 0, -1, -1, 1), [1, 0, 1, -1, 1, 1], [-1, 1, 0, 1, 0, -1], [1, 1, 1, 0, -1, 1], (-1, 1, 0, -1, 0, -1), [-1, 0, 1, -1, 1, 0], [0, -1, 0, -1, -1, 1], (1, 0, 0, 1, 1, -1), [-1, -1, 1, -1, -1, -1], (1, 1, -1, 0, 0, -1), [0, 0, 1, 0, 0, 1], (-1, -1, 1, -1, 1, 0), [0, -1, 0, -1, 1, 0], (-1, 1, 0, 0, -1, 0), (1, -1, 1, 1, 1, -1), [0, 0, 0, -1, 0, 0], (0, 1, 0, 0, 0, -1), (-1, 1, -1, 1, -1, 1), (1, 1, 1, -1, 1, -1), [0, 0, 0, -1, -1, 0], (-1, 1, -1, -1, -1, 1), [0, -1, -1, 0, 1, 1], [1, 0, 0, 1, 0, 1], [1, 1, -1, -1, -1, 0], [1, -1, -1, 1, 1, 0], [-1, -1, -1, 1, 0, 0], (-1, 1, -1, 1, -1, -1), (0, 0, 0, 1, 1, -1), [-1, -1, 1, 0, -1, 0], [0, 0, 0, -1, 1, 0], [1, -1, 1, 0, 0, 1], (1, 0, 0, 1, 1, 1), (0, -1, 0, 0, -1, 0), [-1, 1, 1, -1, 1, 0], [-1, 0, -1, 0, 1, -1], (-1, 0, 0, -1, -1, 0), (0, 1, 0, 1, 0, 1), [-1, 1, 1, 0, 1, 0], (1, -1, 1, -1, 1, 1), [-1, 1, 1, 0, 1, 1], (1, 1, 0, -1, -1, -1), [-1, -1, 0, 1, 1, -1], (1, 1, -1, -1, 0, 1), (1, 0, 1, -1, 1, 1), (1, 0, -1, -1, -1, -1), (-1, 1, 1, 1, 0, 1), (1, 1, -1, 0, 0, 1), (-1, 0, -1, -1, 0, 1), [0, -1, 1, 1, 0, 1], (0, 1, 1, 1, -1, -1), [-1, -1, -1, -1, 1, 0], [-1, 1, 1, 1, -1, -1], [-1, -1, 1, -1, 1, 0], (1, 0, -1, 1, -1, -1), [0, -1, 0, 0, 1, 1], [0, 0, 1, 0, 1, -1], [-1, -1, -1, 1, -1, 0], [1, -1, 0, 1, -1, 0], [0, -1, -1, 1, -1, 1], [-1, -1, -1, 0, 1, 0], [1, 0, -1, -1, 0, 0], [-1, 1, -1, 0, 0, 0], (0, 0, 1, -1, 1, 1), (0, -1, -1, 0, 0, 0), [-1, 1, -1, -1, -1, 0], [0, 1, 0, 1, 0, 0], [-1, 1, 1, -1, 1, -1], (1, 1, 1, 1, -1, 1), [1, 1, -1, -1, 0, -1], [-1, -1, 0, -1, -1, 1], [-1, 0, -1, 0, -1, 0], [1, 0, 1, -1, 0, 0], [1, -1, 1, 1, 1, 1], [-1, 1, -1, 0, 0, -1], [0, -1, 1, 0, 1, -1], [-1, 0, -1, 1, -1, 0], (0, -1, 0, -1, 1, 1), [-1, 0, 0, -1, -1, 0], [-1, -1, 0, -1, 0, -1], [0, 1, 1, 0, 1, 1], [-1, 0, 1, -1, 1, -1], [-1, 0, 0, 0, 0, -1], (-1, 1, 1, -1, 1, 1), (0, -1, 0, 0, 1, 0), (-1, 0, 1, 0, -1, -1), [1, 1, 1, 1, 1, 1], [-1, 0, 0, 1, -1, 1], (0, -1, -1, -1, 0, -1), [-1, 0, 1, -1, 0, -1], [-1, 1, 1, 0, 0, 0], [1, -1, 0, 1, -1, 1], [0, 0, 1, 0, -1, 0], (1, 1, 0, 1, -1, 0), (0, 1, 0, -1, -1, 1), [1, 1, 1, 0, 1, 1], (-1, 1, 1, 1, 0, -1), (-1, -1, -1, -1, 1, 0), [0, 1, -1, -1, 1, 0], (1, 1, 0, -1, 0, -1), (0, 1, -1, 1, -1, -1), [1, 1, 1, 0, 1, 0], (-1, -1, 0, 0, 1, 1), (1, 1, -1, -1, -1, 0), [0, -1, 1, 1, -1, -1], (1, 1, 0, 1, 0, -1), [1, 0, 1, -1, 0, 1], [1, -1, -1, 0, 1, 1], [1, 1, 0, -1, 0, 0], (1, -1, 0, 0, -1, 0), (0, 0, 1, 1, -1, 0), (-1, 0, 1, 0, 0, 1), (1, -1, -1, 1, 0, -1), (1, -1, -1, 1, 1, 0), [0, -1, 1, 0, 1, 0], (0, -1, 1, 1, 0, 1), [0, 1, 0, 0, 0, 0], (-1, 1, -1, 1, -1, 0), (-1, 0, 1, -1, 0, -1), [1, 1, 0, 0, 0, 1], [1, 1, -1, 1, 1, 0], (-1, -1, 1, 0, 0, 1), (0, 1, 1, 0, 0, -1), (1, 1, 0, 0, 1, 0), (1, 0, 0, 0, 1, 0), [-1, -1, 1, -1, 1, 1], (0, 1, -1, -1, 0, 1), (-1, 0, 1, 1, 1, -1), [1, 1, -1, 1, 1, -1], [-1, 0, -1, -1, 1, 0], [0, 1, 1, -1, 0, 0], (1, 0, -1, 1, 0, -1), (1, -1, 0, 0, -1, 1), (-1, -1, 1, -1, 0, -1), (-1, 1, 1, -1, -1, -1), (0, 0, -1, -1, 0, -1), (1, 1, -1, 0, -1, -1), [0, -1, 0, 1, 0, 1], (-1, 1, 0, -1, -1, 0), (0, 1, 1, 1, 1, 1), (1, 1, 1, 0, 1, 1), (1, -1, -1, 0, 1, -1), [0, 0, 1, 0, 0, -1], (0, -1, -1, 0, 0, -1), [0, -1, -1, -1, -1, 0], [1, 1, -1, -1, 0, 1], (-1, -1, -1, -1, 0, 1), (-1, -1, 1, -1, 1, -1), [1, 0, 0, -1, 0, 1], [1, 0, 0, 1, 1, 1], [1, -1, -1, -1, 0, 0], [-1, 0, -1, 0, 0, 1], [-1, 0, 1, 1, -1, 0], [-1, 0, 1, 0, 1, -1], [0, 1, -1, 1, -1, -1], [-1, -1, 0, 0, 1, 1], [1, -1, 1, -1, -1, -1], [-1, -1, 1, 0, 1, -1], [-1, 0, -1, 0, 0, -1], [0, -1, 1, 1, 0, 0], [1, 1, 0, -1, -1, -1], (1, 0, -1, 0, 0, 0), [-1, 0, 1, 0, 1, 0], [0, 1, 1, 0, -1, -1], (1, 1, 0, 0, 0, 1), [-1, -1, -1, 0, 0, 0], (-1, -1, 0, -1, 0, 0), [0, -1, 0, -1, 0, 0], (-1, -1, 1, 0, -1, 0), [-1, 1, 0, -1, 0, 1], (1, -1, 1, 0, -1, 0), [1, 1, -1, 0, 0, 1], (1, 0, 1, 0, 1, -1), [1, 0, 0, 0, -1, 0], [-1, 0, 0, 0, 1, 1], [1, 1, 0, -1, 0, -1], (-1, 0, 0, -1, 1, 0), (-1, -1, 1, 0, 1, 1), (0, -1, 1, -1, 0, -1), (1, -1, 0, -1, 1, 1), [0, 0, -1, -1, 1, -1], (-1, -1, 0, -1, 0, -1), (-1, 1, 1, 0, -1, 0), (-1, 0, -1, 0, 1, 1), [-1, -1, -1, 0, -1, 0], (0, 1, 1, -1, 0, -1), (-1, 0, 0, 0, 0, -1), (0, -1, -1, -1, 1, 1), [-1, 0, 1, 0, -1, -1], (-1, -1, 0, -1, 1, -1), [0, 1, -1, 1, -1, 0], (-1, -1, -1, 0, 0, 0), [0, 0, 1, -1, -1, 0], [0, 0, 1, 0, 0, 0], [0, 0, -1, 0, 1, 1], [0, -1, 0, 0, -1, 1], [0, -1, -1, -1, -1, 1], [1, 0, -1, 0, -1, 1], [0, -1, -1, 1, 1, -1], [0, 1, 0, 1, 1, 1], [0, 1, 0, -1, 1, -1], [1, 0, 1, -1, -1, 1], (1, 0, -1, 1, 1, 1), [0, -1, 1, 0, -1, -1], (1, 0, -1, 1, 1, 0), (1, 0, 1, -1, 0, -1), (1, -1, 1, 0, 1, 0), [0, 0, 0, -1, 0, -1], (0, -1, 0, 0, 0, -1), (0, 1, 1, -1, -1, -1), (1, 0, 1, 0, -1, -1), (1, 0, 0, 0, 1, -1), (-1, -1, -1, 1, -1, -1), [-1, 1, -1, 1, 0, -1], (-1, -1, 0, -1, 0, 1), [0, -1, 1, -1, -1, 0], (-1, 1, 0, 0, 1, 0), (1, -1, -1, -1, -1, 1), (0, 1, -1, 0, 1, -1), [1, -1, 0, 1, -1, -1], [0, -1, -1, -1, 1, 0], [-1, 1, 0, 0, 0, 0], [0, 1, 0, 0, -1, -1], [0, 1, 0, 1, 1, 0], [0, 0, -1, 0, -1, 0], [-1, 1, 1, 0, -1, 0], [1, 0, 1, 1, -1, 1], (-1, -1, 1, 0, 1, 0), (0, -1, 1, 1, 0, -1), [-1, -1, 1, 1, 1, 1], [1, -1, -1, 0, -1, 1], [-1, -1, 0, 0, 1, 0], (1, 0, 1, 0, 1, 1), (1, 0, -1, -1, -1, 0), [0, 1, 0, 1, -1, 1]])

def is_pareto_dominable(alloc, true_combs_base, all_combs):
	players = len(true_combs_base)
	items = len(alloc)

	all_zeros = [0 for j in range(items)]


	for comb in  all_combs:
		eq_by_player = [copy(all_zeros) for i in range(players)]

		for i in range(items):
			if alloc[i] != comb[i]:
				eq_by_player[alloc[i]][i] = 1
				eq_by_player[comb[i]][i] = -1

		isPD = True
		isSPD = False
		for player in range(players):
			if sum(eq_by_player[player]) == 0 and len(set(eq_by_player[player])) == 1:
				continue
			elif is_comb_in_base(eq_by_player[player], true_combs_base[player]):
				isSPD = True
				continue
			anti_comb = reverse_comb(eq_by_player[player])
			if is_comb_in_base(anti_comb, true_combs_base[player]):
				isPD = False
				break
			else:
				isSPD = True

		if isPD and isSPD:
			return True, eq_by_player

	return False, None

def is_pareto_dominated(alloc, true_combs_base, all_combs, good_combs):
	players = len(true_combs_base)
	items = len(alloc)

	all_zeros = [0 for j in range(items)]
	all_combs_copy = copy(all_combs)

	random.shuffle(all_combs_copy)

	running_ind = 0
	how_many = 0


	bad_combs = {0: set([]), 1: set([]), 2:set([])}


	for comb in  all_combs_copy:
		running_ind += 1
		eq_by_player = [copy(all_zeros) for i in range(players)]

		for i in range(items):
			if alloc[i] != comb[i]:
				eq_by_player[alloc[i]][i] = 1
				eq_by_player[comb[i]][i] = -1

		isPD = True
		isSPD = False
		more_thorough = []
		for player in range(players):
			if sum(eq_by_player[player]) == 0 and len(set(eq_by_player[player])) == 1:
				continue
			elif 1 not in eq_by_player[player]:
				isSPD = True
				continue
			elif -1 not in eq_by_player[player]:
				isPD = False
			else:
				more_thorough.append(player)
		
		if isPD:
			for player in more_thorough:
				how_many += 1
				if tuple(eq_by_player[player]) in good_combs[player]:
					isSPD = True
					continue

				elif tuple(eq_by_player[player]) in bad_combs[player]:
					isPD = False
					break

				if is_comb_in_base(eq_by_player[player], true_combs_base[player]):
					isSPD = True
					good_combs[player].add(tuple(eq_by_player[player]))
					continue
				else:
					isPD = False
					bad_combs[player].add(tuple(eq_by_player[player]))
					break

		if isPD and isSPD:
			#print("FOUND PD IN RUN INDEX {}".format(running_ind))
			print("HOW MANY: {}".format(how_many))
			return True

	#print("NOT PD")
	print("HOW MANY: {}".format(how_many))

	return False

def filter_pareto_dominated(allocs, true_combs_base, all_combs, good_combs):
	filtered_allocs = []
	players = len(true_combs_base)
	items = len(allocs[0])

	all_zeros = [0 for j in range(items)]
	all_combs_copy = copy(all_combs)

	random.shuffle(all_combs_copy)

	running_ind = 0
	how_many = 0


	bad_combs = {0: set([]), 1: set([]), 2:set([])}

	for alloc in allocs:
		foundPD = False
		for comb in  all_combs_copy:
			running_ind += 1
			eq_by_player = [copy(all_zeros) for i in range(players)]

			for i in range(items):
				if alloc[i] != comb[i]:
					eq_by_player[alloc[i]][i] = 1
					eq_by_player[comb[i]][i] = -1

			isPD = True
			isSPD = False
			more_thorough = []
			for player in range(players):
				if sum(eq_by_player[player]) == 0 and len(set(eq_by_player[player])) == 1:
					continue
				elif 1 not in eq_by_player[player]:
					isSPD = True
					continue
				elif -1 not in eq_by_player[player]:
					isPD = False
					break
				else:
					more_thorough.append(player)
			
			if isPD: 
				for player in more_thorough:
					how_many += 1
					if tuple(eq_by_player[player]) in good_combs[player]:
						isSPD = True
						continue

					elif tuple(eq_by_player[player]) in bad_combs[player]:
						isPD = False
						break

					if is_comb_in_base(eq_by_player[player], true_combs_base[player]):
						isSPD = True
						good_combs[player].add(tuple(eq_by_player[player]))
						continue
					else:
						isPD = False
						bad_combs[player].add(tuple(eq_by_player[player]))
						break

			if isPD and isSPD:
				#print("FOUND PD IN RUN INDEX {}".format(running_ind))
				#print("HOW MANY: {}, FILTERED LENGTH: {}".format(how_many, len(filtered_allocs)))
				foundPD = True
				#print("Found PD")
				break

		#print("NOT PD")
		if not foundPD:
			filtered_allocs.append(alloc)
		#print("HOW MANY: {}, FILTERED LENGTH: {}".format(how_many, len(filtered_allocs)))

	return filtered_allocs

def filter_efx_envious(allocs, true_combs_base, all_combs, good_combs):
	filtered_allocs = []
	for alloc in allocs:
		all_poss_j = []
		for pair in all_pairs:
			side1_items = []
			side2_items = []
			equ = copy(all_zeros)
			for i in range(len(alloc)):
				if alloc[i] == pair[0]:
					side1_items.append(i)
					equ[i] = 1
				elif alloc[i] == pair[1]:
					side2_items.append(i)
					equ[i] = -1

			for j in side2_items:
				curr_equ = copy(equ)
				curr_equ[j] = 0
				if sum(curr_equ) == 0 and len(set(curr_equ)) == 1:
					continue
				all_poss_j.append(tuple([pair[0], curr_equ]))

		random.shuffle(all_poss_j)
		isAlreadyJealous = False
		for elem in all_poss_j:
			#anti_comb = reverse_comb(elem[1])
			if tuple(elem[1]) in good_combs[elem[0]] or is_comb_in_base(tuple(elem[1]), true_combs_base[elem[0]]):
				good_combs[elem[0]].add(tuple(elem[1]))
				#print("alloc {} has eq {} for player {}, and thus envious".format(alloc, elem[1], elem[0]))
				isAlreadyJealous = True
				break

		if isAlreadyJealous == False:
			#print("alloc {} has no current envy".format(alloc))
			filtered_allocs.append(alloc)

	return filtered_allocs


def split_mandatory(all_combs):
	mandatory_combs = []
	later_combs = []
	latest_combs = []

	for comb in all_combs:
		counts = [0,0,0]
		counts[0] = len([i for i in filter(lambda x: x==0, comb)])
		counts[1] = len([i for i in filter(lambda x: x==1, comb)])
		counts[2] = len([i for i in filter(lambda x: x==2, comb)])

		counts.sort()
		if counts[:2] == [1,1]:
			mandatory_combs.append(comb)
		elif 1 in counts:
			later_combs.append(comb)
		elif 0 not in counts:
			latest_combs.append(comb)

	return mandatory_combs, later_combs, latest_combs



players = 3
items = 7

all_pairs = []


def loop_lookahead(allocs, true_combs_base, good_combs, evil_combs):
	votes = {}
	critical_level = {}

	#print("ALLOCS BEFORE FILTER {}".format(len(allocs)))
	allocs = filter_pareto_dominated(allocs, true_combs_base, all_combs, good_combs)
	#print("ALLOCS AFTER PARETO FILTER {}".format(len(allocs)))
	allocs = filter_efx_envious(allocs, true_combs_base, all_combs, good_combs)
	#print("ALLOCS AFTER EFX FILTER {}".format(len(allocs)))

	all_poss_j = []
	for alloc in allocs:
		for pair in all_pairs:
			side1_items = []
			side2_items = []
			equ = copy(all_zeros)
			for i in range(len(alloc)):
				if alloc[i] == pair[0]:
					side1_items.append(i)
					equ[i] = 1
				elif alloc[i] == pair[1]:
					side2_items.append(i)
					equ[i] = -1

			for j in side2_items:
				curr_equ = copy(equ)
				curr_equ[j] = 0
				if sum(equ) == 0 and len(set(equ)) == 1:
					continue
				if tuple([pair[0], tuple(curr_equ)]) in votes:
					votes[tuple([pair[0],tuple(curr_equ)])] += 1
				else:
					votes[tuple([pair[0],tuple(curr_equ)])] = 1

					all_poss_j.append(tuple([pair[0], tuple(curr_equ)]))
		for player, eq in all_poss_j:
			if tuple([player, eq]) not in critical_level:
				critical_level[tuple([player, eq])] = len(all_poss_j)
			else:
				critical_level[tuple([player, eq])] = min(critical_level[tuple([player, eq])], len(all_poss_j))
		#random.shuffle(all_poss_j)

	f_votes = {}

	for key, val in votes.items():
		player, eq = key
		anti_eq = tuple(reverse_comb(eq))
		if anti_eq in evil_combs[player]:
			continue
		elif is_comb_in_base(anti_eq, true_combs_base[player]):
			evil_combs[player].add(anti_eq)
		else:
			f_votes[key] = val

	if len(allocs) > 0:
		return len(f_votes)  / len(allocs) 
	else:

		valuations = {0: [], 1: [], 2:[]}

		for player in range(players):
			valuations[player] = generate_valuation(true_combs_base[player])

		print(valuations)
		return 0



for comb in combinations([i for i in range(players)], 2):
	pair_list = [i for i in comb]
	pair_list_r = copy(pair_list)
	pair_list_r.reverse()
	all_pairs.append(pair_list)
	all_pairs.append(pair_list_r)


	all_combs = [item for item in product([i for i in range(players)], repeat=items)]

	# RUN 4
	true_combs_base = {0: [[-1, 0, 0, 0, 0, 0, 0], [0, -1, 0, 0, 0, 0, 0], [0, 0, -1, 0, 0, 0, 0], [0, 0, 0, -1, 0, 0, 0], [0, 0, 0, 0, -1, 0, 0], [0, 0, 0, 0, 0, -1, 0], [0, 0, 0, 0, 0, 0, -1], [0, -1, 0, -1, -1, 1, -1], [-1, 1, -1, 0, 0, -1, -1], [-1, 0, 1, -1, -1, 0, -1], [0, -1, -1, 1, -1, -1, 0], [-1, 0, 0, 1, -1, -1, -1], [-1, -1, -1, 0, 1, 0, -1], [0, -1, 1, 0, -1, -1, -1], [-1, -1, -1, 0, -1, 1, 0], [-1, 1, -1, -1, -1, 0, 0], [-1, 1, 0, -1, 0, -1, -1], [0, -1, -1, 0, -1, -1, 1], [-1, -1, 0, -1, 1, -1, 0], [1, -1, -1, -1, -1, 0, 0], [1, -1, 0, -1, 0, -1, -1], [1, -1, -1, 0, 0, -1, -1], [0, 0, -1, -1, 1, -1, -1], (0, 1, 0, -1, 0, -1, 0), (0, 1, 0, 0, 0, 1, -1), (1, 0, -1, -1, 0, 0, 0), (0, 0, 0, 0, -1, -1, 1), (-1, 0, 1, 0, 0, 0, 0), (-1, 0, 0, 0, 0, 1, 1), (-1, 0, 0, 0, 1, 0, 1), (-1, 0, 1, 0, 0, 0, 1)], 1: [[-1, 0, 0, 0, 0, 0, 0], [0, -1, 0, 0, 0, 0, 0], [0, 0, -1, 0, 0, 0, 0], [0, 0, 0, -1, 0, 0, 0], [0, 0, 0, 0, -1, 0, 0], [0, 0, 0, 0, 0, -1, 0], [0, 0, 0, 0, 0, 0, -1], [1, -1, 0, -1, 0, -1, -1], [0, -1, -1, -1, 0, 1, -1], [1, 0, -1, -1, -1, -1, 0], [-1, -1, -1, 0, 1, 0, -1], [0, 0, -1, -1, 1, -1, -1], [-1, 0, -1, -1, -1, 0, 1], [-1, -1, -1, 0, 1, -1, 0], [-1, -1, 0, 0, 1, -1, -1], [-1, -1, 1, 0, -1, -1, 0], [0, 1, 0, -1, -1, -1, -1], [-1, -1, -1, 0, -1, 1, 0], [-1, 1, -1, 0, -1, 0, -1], [-1, -1, 0, -1, 0, -1, 1], [-1, 1, -1, 0, -1, -1, 0], [-1, -1, 0, -1, -1, 1, 0], [1, -1, 0, -1, -1, 0, -1], (-1, 0, 0, 0, 0, 0, 1), (-1, 0, 1, 0, 0, 0, 0), (0, 0, 0, 0, -1, 1, 0), (0, 0, 0, -1, 1, 0, 0), (-1, 0, 0, 1, 0, 0, 1), (0, 1, 0, 0, -1, 0, -1), (0, 1, -1, 0, 0, 0, 1), (-1, 0, 0, 0, 1, 1, 0), (1, 0, 0, -1, 0, -1, 0), (-1, 1, 0, 1, 0, 0, 0), (-1, 1, 1, 0, 0, 0, 0), (0, 1, 1, -1, 1, 0, 0)], 2: [[-1, 0, 0, 0, 0, 0, 0], [0, -1, 0, 0, 0, 0, 0], [0, 0, -1, 0, 0, 0, 0], [0, 0, 0, -1, 0, 0, 0], [0, 0, 0, 0, -1, 0, 0], [0, 0, 0, 0, 0, -1, 0], [0, 0, 0, 0, 0, 0, -1], [-1, 0, 0, -1, 1, -1, -1], [-1, 0, 0, -1, -1, 1, -1], [0, -1, -1, 1, -1, 0, -1], [-1, 1, -1, 0, 0, -1, -1], [-1, 0, -1, 0, -1, -1, 1], [-1, 0, -1, -1, 1, -1, 0], [-1, -1, 0, 0, 1, -1, -1], [0, -1, 0, -1, -1, -1, 1], [1, 0, -1, 0, -1, -1, -1], [-1, 1, -1, -1, 0, 0, -1], [0, -1, -1, -1, 1, 0, -1], [1, 0, -1, -1, -1, -1, 0], [-1, -1, 1, 0, -1, -1, 0], [-1, -1, -1, 0, 0, 1, -1], [0, 1, -1, -1, -1, 0, -1], [-1, 0, -1, 1, -1, 0, -1], [-1, 1, 0, -1, 0, -1, -1], [-1, 1, -1, 0, -1, -1, 0], [1, -1, -1, 0, 0, -1, -1], [-1, -1, -1, 1, 0, -1, 0], [-1, -1, 0, -1, -1, 1, 0], [1, -1, 0, -1, -1, -1, 0], (0, 0, -1, 0, 0, -1, 1), (0, 0, 1, 0, 0, 0, -1), (0, 0, 0, 1, 1, 0, -1), (0, 1, 0, 0, 1, -1, 0), (-1, 0, -1, 0, 0, 1, 0), (0, 0, 0, -1, 1, 1, 0), (1, 0, 0, -1, 0, -1, 0), (-1, 1, 0, 0, 0, 0, 1), (-1, 0, 1, 0, 0, 0, 1), (-1, 1, 1, 0, 0, 0, 1), (-1, -1, 0, 0, 0, 1, 1)]}
	#true_combs_base[0].append([-1, 1, 0, 1, 1, 0, 0])

	#allocs = [(1, 0, 1, 0, 0, 2, 2), (1, 0, 0, 0, 1, 2, 2), (1, 2, 2, 0, 2, 0, 2), (2, 2, 0, 1, 0, 1, 2), (1, 0, 2, 0, 2, 2, 2), (1, 0, 2, 0, 1, 2, 2), (0, 2, 1, 1, 2, 2, 2), (0, 0, 1, 1, 2, 2, 2), (0, 0, 2, 1, 1, 2, 2), (1, 1, 0, 0, 2, 2, 2), (0, 0, 0, 1, 1, 2, 2), (1, 0, 1, 0, 1, 2, 2), (2, 1, 1, 0, 1, 1, 2), (2, 2, 1, 0, 1, 1, 2), (1, 1, 0, 2, 0, 2, 2), (0, 1, 2, 1, 1, 2, 2), (1, 0, 0, 0, 2, 2, 2), (2, 1, 1, 0, 1, 1, 0), (2, 1, 2, 0, 1, 1, 0), (0, 1, 0, 1, 1, 2, 2), (0, 1, 1, 1, 0, 2, 2), (2, 0, 0, 1, 0, 1, 2), (1, 2, 0, 2, 0, 0, 2), (0, 2, 1, 1, 0, 2, 2), (1, 1, 0, 0, 0, 2, 2), (1, 1, 0, 0, 1, 2, 2), (1, 2, 2, 0, 1, 2, 2), (2, 1, 0, 1, 0, 1, 2), (1, 2, 0, 1, 0, 2, 2), (1, 0, 0, 1, 0, 2, 2), (2, 1, 0, 0, 1, 1, 2), (1, 1, 0, 2, 0, 0, 2), (1, 2, 2, 0, 0, 2, 2), (1, 0, 0, 2, 0, 1, 2), (0, 2, 0, 1, 1, 2, 2), (1, 0, 1, 0, 2, 2, 2), (0, 0, 1, 1, 1, 2, 2), (1, 2, 0, 2, 0, 1, 2), (1, 2, 0, 0, 2, 2, 2), (0, 1, 2, 1, 2, 2, 2), (1, 0, 0, 2, 0, 0, 2), (1, 2, 1, 0, 2, 2, 2), (1, 2, 0, 0, 1, 2, 2), (1, 1, 2, 0, 2, 0, 2), (2, 0, 1, 1, 0, 2, 0), (0, 0, 1, 1, 0, 2, 2), (1, 1, 2, 0, 0, 2, 2), (0, 2, 2, 1, 1, 2, 2), (0, 1, 0, 2, 1, 1, 2), (1, 1, 1, 0, 0, 2, 2), (2, 0, 0, 1, 1, 2, 0), (2, 2, 1, 0, 1, 1, 0), (2, 0, 1, 0, 1, 1, 2)]
	#allocs = [(2, 1, 0, 0, 2, 2, 1), (2, 1, 0, 0, 1, 0, 2), (2, 1, 0, 2, 1, 1, 0), (2, 1, 0, 0, 2, 2, 0), (2, 1, 1, 2, 1, 0, 0), (2, 1, 0, 0, 2, 0, 2), (2, 1, 1, 0, 1, 0, 2), (2, 1, 0, 0, 2, 1, 0), (2, 1, 0, 2, 1, 2, 0), (2, 1, 0, 0, 2, 2, 2), (2, 1, 0, 2, 0, 2, 2), (2, 1, 0, 0, 1, 2, 0), (2, 1, 0, 2, 2, 1, 0), (2, 1, 1, 0, 2, 0, 1), (2, 1, 0, 2, 2, 0, 2), (2, 1, 0, 2, 2, 2, 0), (2, 1, 0, 0, 1, 1, 1), (2, 1, 1, 2, 0, 0, 2), (2, 1, 0, 2, 2, 1, 1), (2, 1, 1, 2, 0, 1, 0), (2, 1, 1, 0, 2, 1, 0), (2, 1, 0, 0, 2, 0, 1), (2, 1, 0, 1, 1, 2, 2), (2, 1, 2, 2, 1, 0, 0), (2, 1, 0, 2, 2, 2, 1), (2, 0, 0, 2, 1, 1, 1), (2, 1, 0, 0, 2, 1, 1), (2, 1, 0, 2, 1, 0, 0), (2, 1, 0, 2, 1, 0, 2), (2, 1, 0, 2, 1, 1, 1), (2, 1, 0, 0, 1, 1, 2), (2, 1, 1, 0, 2, 0, 0), (2, 1, 1, 2, 2, 0, 0), (2, 1, 1, 2, 2, 1, 0), (2, 1, 1, 0, 1, 2, 0), (2, 1, 0, 2, 0, 1, 1), (2, 1, 1, 2, 0, 2, 0), (2, 1, 0, 2, 0, 2, 1), (2, 1, 1, 0, 1, 1, 0), (2, 1, 0, 2, 2, 1, 2), (2, 1, 1, 0, 2, 2, 0), (2, 1, 0, 0, 2, 0, 0), (2, 1, 0, 2, 1, 1, 2), (2, 1, 0, 0, 1, 2, 2), (2, 1, 2, 2, 1, 1, 0), (2, 0, 0, 2, 1, 1, 2), (2, 1, 0, 2, 0, 1, 2), (2, 1, 1, 2, 1, 1, 0), (2, 1, 0, 0, 1, 2, 1), (2, 1, 2, 2, 1, 0, 1), (2, 1, 0, 2, 2, 0, 0), (2, 1, 1, 2, 1, 2, 0), (2, 1, 0, 2, 1, 2, 1), (2, 1, 1, 2, 0, 0, 0), (2, 0, 0, 2, 1, 2, 1), (2, 1, 1, 0, 2, 0, 2), (2, 1, 2, 2, 1, 2, 0), (2, 1, 1, 2, 2, 2, 0)]

	allocs = [(1, 0, 1, 0, 0, 2, 2), (1, 0, 0, 0, 1, 2, 2), (1, 2, 2, 0, 2, 0, 2), (2, 2, 0, 1, 0, 1, 2), (1, 0, 2, 0, 2, 2, 2), (1, 0, 2, 0, 1, 2, 2), (0, 2, 1, 1, 2, 2, 2), (0, 0, 1, 1, 2, 2, 2), (0, 0, 2, 1, 1, 2, 2), (1, 1, 0, 0, 2, 2, 2), (0, 0, 0, 1, 1, 2, 2), (1, 0, 1, 0, 1, 2, 2), (2, 1, 1, 0, 1, 1, 2), (2, 2, 1, 0, 1, 1, 2), (1, 1, 0, 2, 0, 2, 2), (0, 1, 2, 1, 1, 2, 2), (1, 0, 0, 0, 2, 2, 2), (2, 1, 1, 0, 1, 1, 0), (2, 1, 2, 0, 1, 1, 0), (0, 1, 0, 1, 1, 2, 2), (0, 1, 1, 1, 0, 2, 2), (2, 0, 0, 1, 0, 1, 2), (1, 2, 0, 2, 0, 0, 2), (0, 2, 1, 1, 0, 2, 2), (1, 1, 0, 0, 0, 2, 2), (1, 1, 0, 0, 1, 2, 2), (1, 2, 2, 0, 1, 2, 2), (2, 1, 0, 1, 0, 1, 2), (1, 2, 0, 1, 0, 2, 2), (1, 0, 0, 1, 0, 2, 2), (2, 1, 0, 0, 1, 1, 2), (1, 1, 0, 2, 0, 0, 2), (1, 2, 2, 0, 0, 2, 2), (1, 0, 0, 2, 0, 1, 2), (0, 2, 0, 1, 1, 2, 2), (1, 0, 1, 0, 2, 2, 2), (0, 0, 1, 1, 1, 2, 2), (1, 2, 0, 2, 0, 1, 2), (1, 2, 0, 0, 2, 2, 2), (0, 1, 2, 1, 2, 2, 2), (1, 0, 0, 2, 0, 0, 2), (1, 2, 1, 0, 2, 2, 2), (1, 2, 0, 0, 1, 2, 2), (1, 1, 2, 0, 2, 0, 2), (2, 0, 1, 1, 0, 2, 0), (0, 0, 1, 1, 0, 2, 2), (1, 1, 2, 0, 0, 2, 2), (0, 2, 2, 1, 1, 2, 2), (0, 1, 0, 2, 1, 1, 2), (1, 1, 1, 0, 0, 2, 2), (2, 0, 0, 1, 1, 2, 0), (2, 2, 1, 0, 1, 1, 0), (2, 0, 1, 0, 1, 1, 2)]

	good_combs = {0: set([]), 1: set([]), 2: set([])}
	evil_combs = {0: set([]), 1: set([]), 2: set([])}


	#allocs = [(1, 0, 0, 1, 0, 2, 1), (2, 0, 0, 2, 0, 1, 0), (0, 0, 2, 2, 0, 1, 2), (2, 0, 2, 2, 0, 1, 2), (0, 0, 2, 2, 0, 1, 0), (1, 0, 2, 2, 0, 1, 0), (0, 0, 0, 1, 0, 2, 1), (0, 0, 2, 2, 0, 1, 1), (2, 0, 2, 2, 0, 1, 1), (0, 2, 2, 2, 0, 1, 0), (1, 0, 2, 2, 0, 1, 2), (2, 0, 0, 2, 0, 1, 2), (2, 0, 2, 2, 0, 1, 0), (1, 0, 2, 2, 0, 1, 1), (0, 1, 2, 2, 0, 1, 0)]

	all_zeros = [0 for j in range(items)]

	valuations = {0: [], 1: [], 2:[]}

	for player in range(players):
		valuations[player] = generate_valuation(true_combs_base[player])

	print(valuations)
	while True:
		votes = {}
		critical_level = {}

		print("ALLOCS BEFORE FILTER {}".format(len(allocs)))
		allocs = filter_pareto_dominated(allocs, true_combs_base, all_combs, good_combs)
		print("ALLOCS AFTER PARETO FILTER {}".format(len(allocs)))
		allocs = filter_efx_envious(allocs, true_combs_base, all_combs, good_combs)
		#print("ALLOCS AFTER EFX FILTER {}".format(len(allocs)))

		all_poss_j = []
		for alloc in allocs:
			for pair in all_pairs:
				side1_items = []
				side2_items = []
				equ = copy(all_zeros)
				for i in range(len(alloc)):
					if alloc[i] == pair[0]:
						side1_items.append(i)
						equ[i] = 1
					elif alloc[i] == pair[1]:
						side2_items.append(i)
						equ[i] = -1

				for j in side2_items:
					curr_equ = copy(equ)
					curr_equ[j] = 0
					if sum(equ) == 0 and len(set(equ)) == 1:
						continue
					if tuple([pair[0], tuple(curr_equ)]) in votes:
						votes[tuple([pair[0],tuple(curr_equ)])] += 1
					else:
						votes[tuple([pair[0],tuple(curr_equ)])] = 1

						all_poss_j.append(tuple([pair[0], tuple(curr_equ)]))
			for player, eq in all_poss_j:
				if tuple([player, eq]) not in critical_level:
					critical_level[tuple([player, eq])] = len(all_poss_j)
				else:
					critical_level[tuple([player, eq])] = min(critical_level[tuple([player, eq])], len(all_poss_j))
			#random.shuffle(all_poss_j)

		f_votes = {}

		for key, val in votes.items():
			player, eq = key
			anti_eq = tuple(reverse_comb(eq))
			if anti_eq in evil_combs[player]:
				continue
			elif is_comb_in_base(anti_eq, true_combs_base[player]):
				evil_combs[player].add(anti_eq)
			else:
				f_votes[key] = val

		max_val = 0
		max_arg = []
		for f_vote in f_votes:
			tcb = copy(true_combs_base)
			gc = copy(good_combs)
			ec = copy(evil_combs)
			ac = copy(allocs)

			tcb[f_vote[0]].append(list(f_vote[1]))
			curr_val = loop_lookahead(ac, tcb, gc, ec) 
			print("For f_vote {} lookahead val is {}".format(f_vote, curr_val))
			if curr_val > max_val:
				max_val = curr_val
				max_arg = f_vote

		print("CHOSE f_vote {} with lookahead val of {}".format(max_arg, max_val))
		true_combs_base[max_arg[0]].append(list(max_arg[1]))

