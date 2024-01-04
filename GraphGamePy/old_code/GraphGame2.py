#old attempt at the solver

import numpy as np
import nashpy as nash

#Object that stores strategy info. The constructor takes a set of strategy matrices, calculates
#the game with nashpy, and stores the resulting mixed strategies and utilities for either player.
#Meant to be stored as an element in the solution_chart
class EquilibriaStrategy:

	def __init__(self, reward_matrices):
		game = nash.Game(reward_matrices[0], reward_matrices[1])
		equilibria = game.support_enumeration()
		for eq in equilibria:
			self.mixed_strategies = eq
			self.utilities = game[eq]
			print(game)
			print(self.utilities)

#Returns the total utility for a node with moves left. side effect: populates solution_chart. The function's
#purpose is to fill out the solution chart but only recurses the utilities, as only they are relevant to
#calculating the next state's utilities
def get_utility(node, moves_left):
	already_calculated = solution_chart[node][moves_left];
	neighbors = get_neighbors(node)
	attacker_utilities = []
	defender_utilities = []
	#if the solution is already in the solution chart, use that
	if already_calculated != None:
		strategy = already_calculated
	#if there is only one move left, future rewards (utility) don't matter so they are set to 0. The reward
	#matrices are just the immediate reward. base case
	elif moves_left == 1:
		attacker_utilities = [0.]*len(neighbors)
		defender_utilities = [0.]*len(neighbors)
		reward_matrices = create_reward_matrices(node, attacker_utilities, defender_utilities)
		#create an EquilibriaStrategy, thereby solving the game for the reward matrices, then record the
		#results in solution_chart
		strategy = EquilibriaStrategy(reward_matrices)
		solution_chart[node][moves_left] = strategy
	#recursive case
	#in order to get the current utility, we need to know all neighbors' utilities, so get those recursively
	else:
		for i in neighbors:
			#I think this may be where the problem is. This should be calling utility on multiple
			#neighbors, but seems to get caught calling on node 1 for a while. The output shows only
			#moves_left = 5 games being calculated by EquilibriaStrategy class; there should be a lot
			#more than that because it should be calling multiple neighbors here, but seems to not be
			utility = get_utility(i, moves_left - 1)
			#These are returned as [attacker utility, defender utility], so we have to use indeces 0 and 1
			#to get the utilities for each neighbor and for the attacker and defender, using .append to
			#form seperate lists for the attacker and defender's utilties, to be combined with immediate
			#rewards by create_reward_matrices()
			attacker_utilities.append(utility[0])
			defender_utilities.append(utility[1])
		reward_matrices = create_reward_matrices(node, attacker_utilities, defender_utilities)
		#create an EquilibriaStrategy, thereby solving the game for the reward matrices, then record the
		#results in solution_chart
		strategy = EquilibriaStrategy(reward_matrices)
		solution_chart[node][moves_left] = strategy
	#return just the utilities, to be used in the above recursion
	return strategy.utilities

#This function is responsible for forming the reward matrices to be fed to nashpy
def create_reward_matrices(current_node, attacker_utilities, defender_utilities):
	#this function starts the reward matrices by getting the immediate rewards available around the current
	#node. For the attacker, the main diagonal is negated, since it loses points when the attacker and defender
	#choose the same option. The negation of the attacker's matrix is then taken to get the defender's
	#reward matrix.
	imm_rewards = get_immediate_rewards(current_node)
	attacker_matrix = np.tile(imm_rewards,(len(imm_rewards),1))
	for i in range(0, len(attacker_matrix)):
		attacker_matrix[i][i] *= -1
	defender_matrix = attacker_matrix[:] * -1

	#print(defender_matrix)
	#print(defender_utilities)

	#Then, it adds the provided (future) utilities (calculated in get_utility()) appropriately to the columns
	#or rows of the attacker and defender's reward matrices
	for x in range(0, len(attacker_matrix)):
		for y in range(0, len(attacker_matrix)):
			attacker_matrix[x][y] += attacker_utilities[y]
	for x in range(0, len(defender_matrix)):
		for y in range(0, len(defender_matrix)):
			defender_matrix[x][y] += defender_utilities[x]

	#print(defender_matrix)

	return [attacker_matrix, defender_matrix]

#turns the neighbors from get_neighbors() into their immediate reward values
def get_immediate_rewards(node):
	neighbors = get_neighbors(node)
	rewards = []
	for i in neighbors:
		rewards.append(immediate_rewards[i])
	return rewards

#returns a list of all the neighbors around a given node
def get_neighbors(node): #could improve with dynamic?
	neighbors = []
	for i in range(0, numberOfNodes):
		if adjacency_matrix[node][i] == 1:
			neighbors.append(i)
	return neighbors

#test data
adjacency_matrix = np.array([[1,0,0,0,0,0,1,0],[0,1,1,1,1,0,0,0],[0,1,1,0,0,0,0,0],[0,1,0,1,0,0,0,0],[0,1,0,0,1,1,0,0],[0,0,0,0,1,1,1,1],[1,0,0,0,0,1,1,0],[0,0,0,0,0,1,0,1]])
#immediate_rewards = [1., 3., 5., 2., 1., 6., 2., 4.]
immediate_rewards = [134., 227., 371., 50., 41., 100., 11., 250.]
start = 1
total_moves = 5
numberOfNodes = len(immediate_rewards)
solution_chart = [[None] * (total_moves+1)] * (numberOfNodes)

#for x in range(0,numberOfNodes):
#	for y in range(1,total_moves):
#		get_utility(x, y)

get_utility(start, total_moves)
print(get_neighbors(start))
print(solution_chart[start][total_moves].mixed_strategies)
print(solution_chart[start][total_moves].utilities)