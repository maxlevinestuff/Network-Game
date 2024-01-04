#Max Levine 6/23/20
#This code seems to work correctly, and calculates the mixed strategies at every state
#very old version of the solver!

import numpy as np
import nashpy as nash

#Object that stores strategy info.
class EquilibriaStrategy:

	#The constructor takes a set of strategy matrices, calculates the game with nashpy,
	#and stores the resulting mixed strategies and utilities for either player.
	def __init__(self, reward_matrix):

		game = nash.Game(reward_matrix)
		equilibriaGenerator = game.vertex_enumeration()
		equilibria = list(equilibriaGenerator)

		if len(equilibria) == 0:
			#if there are 0 found equilibria (degenerate), make an equally randomly distribution
			self.mixed_strategies = EquilibriaStrategy.create_even_mixed_strategy(len(reward_matrix))
			self.utilities = game[self.mixed_strategies]
		else:
			#if there are multiple, choose 1?
			#way to find average?
			for eq in equilibria:
				#this for-loop ends up using the last equilibria, whatever that may be
				self.mixed_strategies = eq
				self.utilities = game[self.mixed_strategies]

	#Create a completely random mixed strategy with a certain number of options
	def create_even_mixed_strategy(number_of_choices):
		even_mixed = [1/number_of_choices] * number_of_choices
		return [even_mixed, even_mixed]

#Adds a given 1d adder array to all the rows of an array
def add_to_rows(array, adder):
	for x in range(0, len(adder)):
		for y in range(0, len(adder)):
			array[x][y] += adder[y]

#Adds a given 1d adder array to all the columns of an array
def add_to_columns(array, adder):
	for x in range(0, len(adder)):
		for y in range(0, len(adder)):
			array[x][y] += adder[x]

#Returns a list of all adjacent nodes to a given node in the adjacency_matrix
def get_neighbors(node):
	length = len(adjacency_matrix)
	neighbors = []
	for i in range(0, length):
		if adjacency_matrix[node][i] == 1:
			neighbors.append(i)
	return neighbors

#Returns a list of the reward values of all adjacent nodes to a given node in the adjacency_matrix
def get_immediate_rewards(node):
	neighbors = get_neighbors(node)
	rewards = []
	for i in neighbors:
		rewards.append(immediate_rewards[i])
	return rewards

#Creates a numpy array with width and height and all values set to an initial value
def create_2d_matrix(width, height, init_value):
	array = np.array([init_value])
	array = np.tile(array, (width, height))
	return array

#Negates the main diagonal of a given square matrix
def negate_diagonal(matrix):
	for i in range(0, len(matrix)):
		matrix[i][i] *= -1

#Returns a list of the previously calculated total utilities adjacent to a given node with a
#given number of moves left. for_attacker specifies whether to get the attacker or defender's utilies
def get_surrounding_utilities(node, moves_left, for_attacker):
	neighbors = get_neighbors(node)
	utilities = []
	index = 0 if for_attacker else 1
	for i in neighbors:
		#print(solution_chart[i][moves_left].game)
		utilities.append(solution_chart[i][moves_left].utilities[index])
	return utilities

#Solves a state (defined by attacker position and moves left) and stores the result in solution_chart
#(dyanmic programming)
def solve_state(attacker_location, moves_left):
	if solution_chart[attacker_location][moves_left] != None:
		return
	neighbors = get_neighbors(attacker_location)
	num_of_neighbors = len(neighbors)
	reward_matrix = create_2d_matrix(num_of_neighbors, num_of_neighbors, 0.)
	add_to_columns(reward_matrix, get_immediate_rewards(attacker_location))
	negate_diagonal(reward_matrix)
	if moves_left != 0:
		add_to_columns(reward_matrix, get_surrounding_utilities(attacker_location, moves_left - 1, True))
		add_to_rows(reward_matrix, get_surrounding_utilities(attacker_location, moves_left - 1, False))
	strategy = EquilibriaStrategy(reward_matrix)
	solution_chart[attacker_location][moves_left] = strategy

#Solves every state, given the graph and total_moves, using a bottom-up approach
def solve_all_states():
	for moves_left in range(0, total_moves):
		for node in range(0, number_of_nodes):
			solve_state(node, moves_left)

#global variables/input
total_moves = 15 #move 0 = 1 move left
adjacency_matrix = np.array([[1,0,0,0,0,0,1,0],[0,1,1,1,1,0,0,0],[0,1,1,0,0,0,0,0],[0,1,0,1,0,0,0,0],[0,1,0,0,1,1,0,0],[0,0,0,0,1,1,1,1],[1,0,0,0,0,1,1,0],[0,0,0,0,0,1,0,1]])
#immediate_rewards = [1., 3., 5., 2., 1., 6., 2., 4.]
immediate_rewards = [12., 3., 55., 2., 1., 107., 0., 3.]
#immediate_rewards = [0., 0., 0., 0., 100., 100., 100., 100.]
number_of_nodes = len(immediate_rewards)
solution_chart = create_2d_matrix(number_of_nodes, total_moves, None)
solve_all_states()
print(solution_chart[1][1].mixed_strategies)
print(solution_chart[1][1].utilities)