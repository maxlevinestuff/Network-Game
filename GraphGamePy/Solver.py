#Solves a network game by calculating all the rational mixed strategies

import numpy as np
import nashpy as nash

import NetworkGame as net
import Rules as rules

class NetworkGameSolution:

	#Takes a network game and solves it for a certain maximum number of moves
	def __init__(self, total_moves, network_game):
		self.game_rules = network_game.game_rules
		self.total_moves = total_moves
		self.network_game = network_game
		self.number_of_nodes = len(self.network_game.adjacency_matrix)
		self.solution_chart = create_2d_matrix(self.number_of_nodes, self.total_moves, None)
		self.solve_all_states(0)

	#For when the last move is 0
	def get_solution(self, node, moves_left):
		self.extend_moves(moves_left + 1)
		return self.solution_chart[node][moves_left]

	#For when the last move is 1, not 0 (confusing)
	def get_solution_no_zero(self, node, moves_left):
		return NetworkGameSolution.get_solution(self, node, moves_left - 1)

	#Gets the neighbors of a node
	def get_neighbors(self, node):
		return self.network_game.get_neighbors(node)

	#Get a list of the immediate rewards
	def get_immediate_rewards(self):
		return self.network_game.immediate_rewards

	#Object that stores a state's strategy info.
	class EquilibriaStrategy:

		#The constructor takes a set of strategy matrices, calculates the game with nashpy,
		#and stores the resulting mixed strategies and utilities for either player.
		def __init__(self, reward_matrix):

			game = nash.Game(reward_matrix)
			#self.game = game #don't need
			equilibriaGenerator = game.support_enumeration()
			equilibria = list(equilibriaGenerator)

			if len(equilibria) == 0:
				#try vertex enumeration
				equilibriaGenerator = game.vertex_enumeration()
				equilibria = list(equilibriaGenerator)
				#if there are still 0 found equilibria (degenerate), make an equally random distribution
				if len(equilibria) == 0:
					self.mixed_strategies = NetworkGameSolution.EquilibriaStrategy.create_even_mixed_strategy(len(reward_matrix))
					self.utilities = game[self.mixed_strategies]
				else:
					for eq in equilibria:
						self.mixed_strategies = eq
						self.utilities = game[eq]
			else:
				#average all of the equilibria
				attacker_strategy = np.array([0.] * len(reward_matrix))
				defender_strategy = np.array([0.] * len(reward_matrix))
				for eq in equilibria:
					attacker_strategy = attacker_strategy + np.array(eq[0])
					defender_strategy = defender_strategy + np.array(eq[1])
				attacker_strategy /= len(equilibria)
				defender_strategy /= len(equilibria)
				self.mixed_strategies = [attacker_strategy, defender_strategy]
				self.utilities = game[self.mixed_strategies]
			#print(game)
			#print(self.utilities)

		#Create a completely random mixed strategy with a certain number of options
		def create_even_mixed_strategy(number_of_choices):
			even_mixed = [1/number_of_choices] * number_of_choices
			return [even_mixed, even_mixed]

	#Adds a given 1d adder array to all the rows of an array
	def add_to_rows(array, adder): #dont need anymore
		for x in range(0, len(adder)):
			for y in range(0, len(adder)):
				array[x][y] += adder[y]

	#Adds a given 1d adder array to all the columns of an array
	def add_to_columns(array, adder):
		for x in range(0, len(adder)):
			for y in range(0, len(adder)):
				array[x][y] += adder[x]

	#Modifies the diagonal (caught) values via the appropriate function
	def handle_collision(reward_matrix, game_rules, neighbors):
		NetworkGameSolution.change_all_diagonal_values(
			reward_matrix, NetworkGameSolution.get_collision_operation_function(game_rules), game_rules.get_surrounding_caught_costs(neighbors))

	#Get the appropriate function based on the game rules to handle attacker caught (diagonal)
	def get_collision_operation_function(game_rules):
		if game_rules.caught_reward_policy == rules.Options.caught_negate_from_reward:
			return NetworkGameSolution.diagonal_value_negate
		elif game_rules.caught_reward_policy == rules.Options.caught_subtract_from_reward:
			return NetworkGameSolution.diagonal_value_subtract_from
		elif game_rules.caught_reward_policy == rules.Options.caught_subtract_from_0:
			return NetworkGameSolution.diagonal_value_set_to_negative

	#Changes ALL the diagonal values of a matrix using the given function
	def change_all_diagonal_values(matrix, func, amount=None):
		for i in range(0, len(matrix)):
			NetworkGameSolution.change_diagonal_value(matrix, i, func, amount)
	#Changes A diagonal value of a matrix using the given function
	def change_diagonal_value(matrix, i, func, amount=None):
		func(matrix, i, amount)
	#Negates a single diagonal value
	def diagonal_value_negate(matrix, i, amt=None):
		matrix[i][i] *= -1
	#Subtracts from a single diagonal value
	def diagonal_value_subtract_from(matrix, i, amt):
		if isinstance(amt, list):
			matrix[i][i] -= amt[i]
		else:
			matrix[i][i] -= amt
	#Sets a single diagonal value to negative
	def diagonal_value_set_to_negative(matrix, i, amt):
		if isinstance(amt, list):
			matrix[i][i] = -amt[i]
		else:
			matrix[i][i] = -amt
	#Adds to a single diagonal value
	def diagonal_value_add_to(matrix, i, amt):
		if isinstance(amt, list):
			matrix[i][i] += amt[i]
		else:
			matrix[i][i] += amt

	#Returns a list of the previously calculated total utilities adjacent to a given node with a
	#given number of moves left. for_attacker specifies whether to get the attacker or defender's utilies
	def get_surrounding_utilities(self, node, moves_left, for_attacker):
		neighbors = self.network_game.get_neighbors(node)
		utilities = []
		for i in neighbors:
			utilities.append(self.get_weighted_utility(i, moves_left, for_attacker))
		return utilities

	#Gets the utility of a given node but also considers transition nodes if there are any, and combines weighted portions of the
	#nodes possible to transition to
	def get_weighted_utility(self, node, moves_left, for_attacker):
		index = 0 if for_attacker else 1
		for t in range(0, len(self.game_rules.transition_chances.branch_start_nodes)):
			if self.game_rules.transition_chances.branch_start_nodes[t] == node:
				total_utility = 0.
				for i in range(0, len(self.game_rules.transition_chances.destination_nodes[t])):
					total_utility += self.solution_chart[self.game_rules.transition_chances.destination_nodes[t][i]][moves_left].utilities[index] * self.game_rules.transition_chances.destination_nodes_chances[t][i]
				return total_utility
		return self.solution_chart[node][moves_left].utilities[index]

	#sets the end reward values (no future utility added)
	def set_end_reward(self, reward_matrix, neighbors, attacker_location, moves_left, game_rules):
		for n in range(0, len(neighbors)):
			for e in range(0, len(game_rules.end_nodes)):
				if neighbors[n] == game_rules.end_nodes[e]:
					NetworkGameSolution.set_row(reward_matrix, n, game_rules.end_node_values[e])
					if game_rules.can_be_caught_on_end_node:
						func = NetworkGameSolution.get_collision_operation_function(game_rules)
						func(reward_matrix, n, game_rules.get_surrounding_caught_costs(neighbors))
						if moves_left != 0:
							if game_rules.caught_policy == rules.Options.caught_policy_block:
								NetworkGameSolution.diagonal_value_add_to(reward_matrix, n, self.get_weighted_utility(attacker_location, moves_left - 1, True))
							elif game_rules.caught_policy == rules.Options.caught_policy_return_to_start:
								NetworkGameSolution.diagonal_value_add_to(reward_matrix, n, self.get_weighted_utility(attacker_location, moves_left - 1, True))
	#used for setting the end values
	def set_row(array, row, value):
		for y in range(0, len(array)):
			array[row][y] = value

	#Solves a state (defined by attacker position and moves left) and stores the result in solution_chart
	#using bottom-up dynamic programming
	def solve_state(self, attacker_location, moves_left):
		#if already calculated, exit
		if self.solution_chart[attacker_location][moves_left] != None:
			return
		neighbors = self.network_game.get_neighbors(attacker_location)
		num_of_neighbors = len(neighbors)
		#create the reward matrix
		reward_matrix = create_2d_matrix(num_of_neighbors, num_of_neighbors, 0.)
		#add the immediate reward values to the matrix
		NetworkGameSolution.add_to_columns(reward_matrix, self.network_game.game_rules.get_surrounding_immediate_rewards(neighbors))
		#Handle the diagonal (caught) values
		NetworkGameSolution.handle_collision(reward_matrix, self.game_rules, neighbors)

		#if there are future moves, add future utility
		if moves_left != 0:
			surrounding_utilities = self.get_surrounding_utilities(attacker_location, moves_left - 1, True)
			NetworkGameSolution.add_to_columns(reward_matrix, surrounding_utilities)

			if self.game_rules.caught_policy != rules.Options.caught_policy_continue:
				#subtract the just-added future utilities from the diagonal
				NetworkGameSolution.change_all_diagonal_values(reward_matrix, NetworkGameSolution.diagonal_value_subtract_from, surrounding_utilities)

				if self.game_rules.caught_policy == rules.Options.caught_policy_block:
					#set all future utilities to current node
					NetworkGameSolution.change_all_diagonal_values(reward_matrix, NetworkGameSolution.diagonal_value_add_to, self.get_weighted_utility(attacker_location, moves_left - 1, True))
				elif self.game_rules.caught_policy == rules.Options.caught_policy_return_to_start:
					#set all future utilities to start node
					NetworkGameSolution.change_all_diagonal_values(reward_matrix, NetworkGameSolution.diagonal_value_add_to, self.get_weighted_utility(self.game_rules.start_node, moves_left - 1, True))

		if self.game_rules.end_nodes:
			self.set_end_reward(reward_matrix, neighbors, attacker_location, moves_left, self.game_rules) #for end goal node

		#if no options (isolated node), set reward matrix to 0
		if len(reward_matrix) == 0:
			reward_matrix = create_2d_matrix(1, 1, 0.)

		strategy = self.EquilibriaStrategy(reward_matrix)
		self.solution_chart[attacker_location][moves_left] = strategy

	#Solves every state, given the graph and total_moves, using a bottom-up approach. Can start at a certain move count
	#to avoid going over already-calculated
	def solve_all_states(self, moves_start):
		for moves_left in range(moves_start, self.total_moves):
			for node in range(0, self.number_of_nodes):
				self.solve_state(node, moves_left)

	#Can extend the solution chart to allow for more moves, and solves them
	def extend_moves(self, new_total_moves):
		if (new_total_moves > self.total_moves):
			extender = create_2d_matrix(self.number_of_nodes, new_total_moves - self.total_moves, None)
			new_chart = np.append(self.solution_chart, extender, axis=1)
			old_total_moves = self.total_moves
			self.solution_chart = new_chart
			self.total_moves = new_total_moves
			self.solve_all_states(old_total_moves)

#Creates a numpy array with width and height and all values set to an initial value
def create_2d_matrix(width, height, init_value):
	array = np.array([init_value])
	array = np.tile(array, (width, height))
	return array