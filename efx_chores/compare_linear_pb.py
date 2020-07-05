import random
from itertools import product, combinations
from copy import copy

from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
session = WolframLanguageSession()

import pylgl

import time

from pypblib import pblib
from pysat.solvers import Glucose3, Lingeling


arrays = []

items = 7

comb_behavior = {}

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

	try:
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
	except Exception as e:
		print("EXCEPTION IN GENERATE VALUATION")
		import pdb
		pdb.set_trace()

	return valuation

def pb_solve2(comb, base):

	cnf = ""
	total = 0
	all_clauses = []

	con_ind = 0

	for con in base + [comb]:
		con_ind += 1
		rhs = -1
		all_eq = []
		all_str = ""
		for elem_ind in range(len(con)):
			elem = con[elem_ind]
			if elem != 0:
				for bit in range(1,8):
					all_eq.append(pblib.WeightedLit(int("{}{}".format(elem_ind, bit)), 2**(bit-1) * elem))
					if elem > 0:
						all_str += "+ {} x{}".format(2**(bit-1) * elem, int("{}{}".format(elem_ind, bit)))
					else:
						all_str += "{} x{}".format(2**(bit-1) *elem, int("{}{}".format(elem_ind, bit)))

		all_str += " <= -1;"


		constr = pblib.PBConstraint(all_eq, pblib.LEQ, rhs)
		aux_var = pblib.AuxVarManager(10000 * con_ind)
		config = pblib.PBConfig()
		formula = pblib.VectorClauseDatabase(config)
		pb2cnf = pblib.Pb2cnf(config)
		pb2cnf.encode(constr, formula, aux_var)
		clauses = formula.get_clauses()
		all_clauses += clauses

	all_vars = set([])
	all_clauses_str = []
	for c in all_clauses:
		if not c:
			return 
		clause_str = []
		for var in c:
			all_vars.add("x{}".format(var))
			clause_str.append("x{}".format(var))

		clause = "(" + " || ".join(clause_str) + ")"
		all_clauses_str.append(clause)

	cnf = " && ".join(all_clauses_str)

	cnf_string = "SatisfiableQ[{}, ".format(cnf) + "{" + " {} ".format(",".join(all_vars)) + "}]"


	res = session.evaluate(wlexpr(cnf_string))
	print(res)

def pb_solve(comb, base):

	s = time.time()

	cnf = ""
	total = 0
	all_clauses = []

	con_ind = 0

	for con in base + [comb]:
		con_ind += 1
		rhs = -1
		all_eq = []
		for elem_ind in range(len(con)):
			elem = con[elem_ind]
			if elem != 0:
				for bit in range(1,8):
					all_eq.append(pblib.WeightedLit(int("{}{}".format(elem_ind, bit)), 2**(bit-1) * elem))

		constr = pblib.PBConstraint(all_eq, pblib.LEQ, rhs)
		aux_var = pblib.AuxVarManager(10000 * con_ind)
		config = pblib.PBConfig()
		formula = pblib.VectorClauseDatabase(config)
		pb2cnf = pblib.Pb2cnf(config)
		pb2cnf.encode(constr, formula, aux_var)
		clauses = formula.get_clauses()
		all_clauses += clauses

	e = time.time()
	print("OPB to CNF time {}".format(e - s))

	"""g = Glucose3()
	for c in all_clauses:
		g.add_clause(c)

	sol = g.solve()
	print(sol)"""

	s = time.time()

	l = Lingeling()
	for c in all_clauses:
		l.add_clause(c)

	sol = l.solve()
	print(sol)

	e = time.time()

	#print(pylgl.solve(all_clauses))

	print("CNF time {}".format(e - s))


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



true_combs_base = [[0, -1, 0, 0, 0, 0, 0], [0, 0, -1, 0, 0, 0, 0], [0, 0, 0, -1, 0, 0, 0], [0, 0, 0, 0, -1, 0, 0], [0, 0, 0, 0, 0, -1, 0], [0, 0, 0, 0, 0, 0, -1], [0, 0, -1, 1, -1, -1, -1], [-1, -1, 1, 0, 0, -1, -1], [1, -1, -1, 0, -1, 0, -1], [0, 0, -1, -1, -1, 1, -1], [0, -1, -1, -1, 0, -1, 1], [0, -1, 1, -1, -1, 0, -1], [-1, 0, 1, -1, -1, -1, 0], [-1, -1, -1, 1, 0, 0, -1], [-1, -1, -1, -1, 1, 0, 0], [0, 1, -1, 0, -1, -1, -1], [0, -1, -1, 0, -1, -1, 1], [1, -1, -1, 0, -1, -1, 0], [-1, 0, 0, -1, 1, -1, -1], [0, 0, -1, -1, 1, -1, -1], [-1, -1, -1, 0, 1, 0, -1], [0, -1, -1, 1, -1, -1, 0], (1, 0, 0, -1, -1, 0, 0), (0, 0, 0, 0, 0, -1, 1), (1, 0, 0, -1, 0, 1, 0), (1, 1, -1, 0, 0, 0, 0), (0, -1, 0, 1, 0, 0, -1), (1, 0, 1, 0, 0, -1, 0), (0, 1, 1, 0, 0, -1, 0), (0, 1, 0, 0, 1, -1, 0), (0, 1, 1, 0, 1, 0, -1), (0, 0, 0, -1, 1, 1, 0)]

manip = []

for tc in true_combs_base:
	tc = list(tc)
	manip.append(tc + [0,0,0])
	manip.append(tc + [0,0,-1])
	manip.append(tc + [0,-1,0])
	manip.append(tc + [0,-1,-1])
	manip.append(tc + [-1,0,0])
	manip.append(tc + [-1,0,-1])
	manip.append(tc + [-1,-1,0])
	manip.append(tc + [-1,-1,-1])

s_pb = time.time()
#pb_solve([1, 0, 0, 0, 0, 0, 0], true_combs_base)
pb_solve([-1, 0, 0, 0, 0, 0, 0, 0,0,0], manip)
pb_solve([1, 0, 0, 0, 0, 0, 0,0,0,0], manip)

e_pb = time.time()

print("HELLO {}".format(e_pb - s_pb))

start = time.time()

print(is_comb_in_base([1, 0, 0, 0, 0, 0, 0, 0,0,0], manip))
print(is_comb_in_base([-1, 0, 0, 0, 0, 0, 0,0,0,0], manip))

end = time.time()

print(end - start)

s_pb = time.time()
#pb_solve([1, 0, 0, 0, 0, 0, 0], true_combs_base)
pb_solve([-1, 0, 0, 0, 0, 0, 0, 0,0,0], manip)
pb_solve([1, 0, 0, 0, 0, 0, 0, 0,0,0], manip)

e_pb = time.time()

print("HELLO {}".format(e_pb - s_pb))

start = time.time()

print(is_comb_in_base([1, 0, 0, 0, 0, 0, 0,0,0,0], manip))
print(is_comb_in_base([-1, 0, 0, 0, 0, 0, 0,0,0,0], manip))

end = time.time()

print(end - start)

