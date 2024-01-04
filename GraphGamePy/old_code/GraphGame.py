#old attempt at the solver

#attacker, defender

import numpy as np
import nashpy as nash

class EquilibriaStrategy:

	def __init__(self, choices, reward_matrix):
		self.choices = choices
		game = nash.Game(reward_matrix)
		equilibria = game.support_enumeration()
		for eq in equilibria:
			self.mixed_strategies = eq
			self.utilities = security_game[eq]

class Graph:
		
	def __init__(self, adjacency_matrix, immediate_rewards, start, end, total_moves):
		self.adjacency_matrix = adjacency_matrix
		self.immediate_rewards = immediate_rewards
		self.start = start
		self.end = end
		self.numberOfNodes = len(adjacency_matrix)
		self.total_moves = total_moves
		self.solution_chart = np.zeros((self.numberOfNodes, self.total_moves))

	def get_utility(self, node, moves_left): #side effect: populates solution_chart
		already_calculated = self.solution_chart[node][moves_left];
		if moves_left == 0 or node == self.end:
			return [self.immediate_rewards[node], -self.immediate_rewards[node]] #DOESNT SEEM RIGHT
		if already_calculated != 0:
			return already_calculated.utilities

		neighbors = self.get_neighbors(node)
		strategy = EquilibriaStrategy(neighbors, self.get_reward_matrix(node, moves_left))
		self.solution_chart[node][moves_left] = strategy
		return strategy.utilities

	def get_neighbors(self, node): #could improve with dynamic?
		neighbors = []
		for i in range(0, self.numberOfNodes):
			if self.adjacency_matrix[node][i] == 1:
				neighbors.append(i)
		return neighbors

	def get_reward_matrix(self, node, moves_left):
		neighbors = self.get_neighbors(node)
		rewards = []
		print(neighbors)
		for i in range(0, len(neighbors)):
			rewards.append(self.get_utility(neighbors[i], moves_left - 1))
		return self.array_to_reward(rewards)
	#helper for above, combine?
	def array_to_reward(self, array): #turns a list of rewards into the 2d array required by nashpy
		print(array)
		for i in range(0, len(array)):
			array[i][i] *= -1


#test data
adj = np.array([[1,1,1,1,1,1,1,1],[1,1,1,1,1,0,0,0],[1,1,1,0,0,0,0,0],[1,1,0,1,0,0,0,0],[1,1,0,0,1,1,0,0],[1,0,0,0,1,1,1,1],[1,0,0,0,0,1,1,0],[1,0,0,0,0,0,0,1]])
imm = [0, 3, 5, 2, 1, 6, 2, 100]
st = 0
en = 7
moves = 5

graph = Graph(adj, imm, st, en, moves)
print(graph.get_neighbors(6))
graph.array_to_reward([10,1])
print(graph.get_reward_matrix(1,1))