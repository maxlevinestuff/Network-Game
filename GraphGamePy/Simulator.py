#Simulates network games and records the results

import numpy as np
import networkx as nx
import random as ran
import copy as cp
import time
from enum import Enum

import Solver as solve
import NetworkGame as net
import Draw as draw
import Rules as rules
import Common as com

#Strategies that the attacker and defender can be set to follow
class StrategyType(Enum):
	rational = 1                 #Chooses based on the mixed strategies
	random = 2                   #Chooses completely randomly
	myopic = 3                   #Chooses the node with the highest immediate reward
	highest_mixed = 4            #Chooses the highest weighted choice in the mixed strategy
	path_to_highest_imm = 5.     #Finds the highest reward node and chooses a node that will decrease distance to it
	noisy_rational = 6           #Applies noise to the rational strategy and then uses that strategy, set noise level and type with noise_level and noise_blocky
	user = 7                     #Lets the user input the moves

class Simulator:

	#If you are oriented to the attacker's side, set this to True, else false
	def __init__(self, for_attacker=True):
		self.expected_utility_index = 0 if for_attacker else 1

	#This class keeps track of a simulation's results. They can be added together over multiple simulations, and then
	#divided to average them
	class GameStats:

		def __init__(self, number_of_simulations, expected_reward, actual_reward, attacker_move_history, defender_move_history, attacker_strategy, defender_strategy, ratio_list):
			self.number_of_simulations = number_of_simulations
			self.expected_reward = expected_reward
			self.actual_reward = actual_reward
			self.attacker_move_history = attacker_move_history
			self.defender_move_history = defender_move_history
			self.attacker_strategy = attacker_strategy
			self.defender_strategy = defender_strategy
			self.ratio_list = ratio_list

		def get_zero_stat(number_of_nodes):
			return Simulator.GameStats(0, 0., 0., [0]*number_of_nodes, [0]*number_of_nodes, None, None, [])

		def __add__(self, other):
			added_number_of_simulations = self.number_of_simulations + other.number_of_simulations
			added_expected_reward = self.expected_reward + other.expected_reward
			added_actual_reward = self.actual_reward + other.actual_reward
			if len(self.attacker_move_history) == len(other.attacker_move_history):
				added_attaker_move_history = add_lists(self.attacker_move_history, other.attacker_move_history)
				added_defender_move_history = add_lists(self.defender_move_history, other.defender_move_history)
			else:
				#multiple graphs are being simulated, discard this per-node data
				added_attaker_move_history = [0]
				added_defender_move_history = [0]
			added_attacker_strategy = other.attacker_strategy
			added_defender_strategy = other.defender_strategy
			added_ratio_list = self.ratio_list + other.ratio_list
			return Simulator.GameStats(added_number_of_simulations, added_expected_reward, added_actual_reward, added_attaker_move_history, added_defender_move_history, added_attacker_strategy, added_defender_strategy, added_ratio_list)

		def __truediv__(self, other):
			return Simulator.GameStats(self.number_of_simulations, self.expected_reward / other, self.actual_reward / other,
				[x / other for x in self.attacker_move_history], [x / other for x in self.defender_move_history],
				self.attacker_strategy, self.defender_strategy, self.ratio_list)

	#Simulates a single game, returning a GameStat
	#Takes a network game solution to simulate, the total moves, the players' strategies, and if there is a noisy
	#strategy, also set the noise level/blocky
	def simulate_one_game(
		self,
		network_game_solution,
		total_moves,
		attacker_strategy=StrategyType.rational, defender_strategy=StrategyType.rational,
		noise_level=0.25, noise_blocky=True):

		self.setup_sim(network_game_solution, attacker_strategy, defender_strategy, noise_level, noise_blocky)
		self.network_game_solution.extend_moves(total_moves)

		current_node = self.game_rules.start_node
		#print("Starting " + str(self.game_rules.start_node))
		current_move = total_moves
		attacker_score = 0

		attacker_move_history = [0] * self.network_game_solution.number_of_nodes
		defender_move_history = [0] * self.network_game_solution.number_of_nodes

		game_over = False
		while current_move > 0:
			current_move -= 1
			attacker_move = self.get_next_move(True, current_node, current_move)
			attacker_move_history[attacker_move] += 1
			defender_move = self.get_next_move(False, current_node, current_move)
			defender_move_history[defender_move] += 1
			#current_node = attacker_move
			
			move_result = self.get_move_result(current_node, attacker_move, defender_move)
			current_node = move_result[2]
			attacker_score += move_result[0]

			if self.user_is_playing():
				self.display_move_result(move_result, attacker_score, current_move)

			if move_result[1]:
				break

			#print("Move to " + str(attacker_move) + " (defending " + str(attacker_move) + ")")
		#Return expected rational reward, total reward, ratio between those, times visited each node, and list of moves
		#and time made each decision per node

		expected_reward = self.network_game_solution.get_solution_no_zero(self.game_rules.start_node, total_moves).utilities[self.expected_utility_index]

		return Simulator.GameStats(1, expected_reward,
			attacker_score, attacker_move_history, defender_move_history, attacker_strategy, defender_strategy, [attacker_score / expected_reward])

	#Checks if a person is playing
	def user_is_playing(self):
		return self.attacker_strategy == StrategyType.user or self.defender_strategy == StrategyType.user
	#Displays the move info if a person is playing
	def display_move_result(self, results, score, current_move):
		if results[3]:
			print("Attacker was caught")
		else:
			print("Attacker was not caught")
		previous_score = score - results[0]
		if self.attacker_strategy == StrategyType.user:
			print("Attacker score: " + str(previous_score) + " + " + str(results[0]) + " = " + str(score))
		if self.defender_strategy == StrategyType.user:
			print("Defender score: " + str(-previous_score) + " + " + str(-results[0]) + " = " + str(-score))
		print()
		if results[1] or current_move==0:
			print("Game over")
			print()
		else:
			print("Attacker location: " + str(results[2]))
			
	#Returns the change in score resulting from the players' moves and whether the game ends or not
	#Return format: (score change, is game over, next node to move to, whether was caught)
	def get_move_result(self, previous_node, attacker_move, defender_move):
		caught = False
		current_node = attacker_move
		score_change = self.network_game_solution.get_immediate_rewards()[current_node]
		caught_cost = self.game_rules.get_caught_cost(current_node)
		game_over = False

		node_to_move_to = self.game_rules.transition_chances.get_node_to_move_to(attacker_move)

		#if stuck, game is over
		if len(self.network_game_solution.get_neighbors(node_to_move_to)) == 0:
			game_over = True

		if self.game_rules.end_nodes:
			for e in range(0, len(self.game_rules.end_nodes)):
				if current_node == self.game_rules.end_nodes[e]:
					game_over = True
					score_change = self.game_rules.end_node_values[e]
					if not self.game_rules.can_be_caught_on_end_node:
						return (score_change, game_over, node_to_move_to, caught)

		if attacker_move == defender_move:

			caught = True

			if self.game_rules.caught_policy == rules.Options.caught_policy_end_game:
				game_over = True
			elif self.game_rules.caught_policy == rules.Options.caught_policy_block:
				game_over = False
				node_to_move_to = previous_node
			elif self.game_rules.caught_policy == rules.Options.caught_policy_return_to_start:
				game_over = False
				node_to_move_to = self.game_rules.start_node

			#handle collisons
			if self.game_rules.caught_reward_policy == rules.Options.caught_negate_from_reward:
				return (-score_change, game_over, node_to_move_to, caught)
			elif self.game_rules.caught_reward_policy == rules.Options.caught_subtract_from_reward:
				return (score_change - caught_cost, game_over, node_to_move_to, caught)
			elif self.game_rules.caught_reward_policy == rules.Options.caught_subtract_from_0:
				return (-caught_cost, game_over, node_to_move_to, caught)
		else:
			return (score_change, game_over, node_to_move_to, caught)

	#Simulates many games, returning an averaged GameStat
	#Takes a network game solution to simulate, the total moves, the players' strategies, and if there is a noisy
	#strategy, also set the noise level/blocky
	def simulate(
		self,
		number_of_simulations,
		network_game_solution,
		total_moves,
		attacker_strategy=StrategyType.rational, defender_strategy=StrategyType.rational,
		noise_level=0.25, noise_blocky=True):

		self.setup_sim(network_game_solution, attacker_strategy, defender_strategy, noise_level, noise_blocky)

		#Average the data from simulate_one_game()
		total_game = Simulator.GameStats.get_zero_stat(network_game_solution.number_of_nodes)
		for i in range(number_of_simulations):
			total_game += self.simulate_one_game(network_game_solution, total_moves, attacker_strategy, defender_strategy, noise_level, noise_blocky)
		total_game /= number_of_simulations

		return total_game

	#Sets up the global variables for use in simulate or simulate_one_game
	def setup_sim(self, network_game_solution,
		attacker_strategy=StrategyType.rational, defender_strategy=StrategyType.rational,
		noise_level=0.25, noise_blocky=True):

		self.game_rules = network_game_solution.game_rules
		self.network_game_solution = network_game_solution
		self.attacker_strategy = attacker_strategy
		self.defender_strategy = defender_strategy
		self.networkx_graph = nx.from_numpy_matrix(network_game_solution.network_game.adjacency_matrix)
		self.noise_level = noise_level
		self.noise_blocky = noise_blocky

	#Gets the next move depending on the set strategies
	def get_next_move(self, for_attacker, attacker_location, moves_left):
		strategy = self.attacker_strategy if for_attacker else self.defender_strategy
		index = 0 if for_attacker else 1
		mixed_strategy = self.network_game_solution.get_solution(attacker_location, moves_left).mixed_strategies[index]
		neighbors = self.network_game_solution.get_neighbors(attacker_location)
		num_of_neighbors = len(neighbors)
		if strategy == StrategyType.rational:
			return Simulator.choose_rational_move(mixed_strategy, neighbors)
		elif strategy == StrategyType.random:
			return Simulator.choose_random_move(neighbors)
		elif strategy == StrategyType.myopic:
			return Simulator.choose_myopic_move(neighbors, for_attacker, self.network_game_solution.game_rules.get_surrounding_immediate_rewards_revised(neighbors), self.network_game_solution.game_rules.get_surrounding_caught_costs(neighbors))
		elif strategy == StrategyType.highest_mixed:
			return Simulator.choose_highest_mixed_move(mixed_strategy, neighbors)
		elif strategy == StrategyType.user:
			return Simulator.choose_user_move(neighbors)
		elif strategy == StrategyType.path_to_highest_imm:
			return Simulator.choose_path_to_highest_imm_move(for_attacker, attacker_location, self.networkx_graph, self.game_rules, neighbors)
		elif strategy == StrategyType.noisy_rational:
			return Simulator.choose_noisy_rational_move(mixed_strategy, neighbors, self.noise_level, self.noise_blocky, moves_left)

	#Applies noise to the rational strategy and then uses that strategy
	#Blocky is deterministic per mixed strategy, so it won't get averaged out over time
	def choose_noisy_rational_move(mixed_strategy_raw, neighbors, noise_level, noise_blocky, moves_left):
		mixed_strategy = []
		#Weirdly sometimes mixed strategies come back as infinitesimally negative, which messes things up
		for i in mixed_strategy_raw:
			if i > 0:
				mixed_strategy.append(i)
			else:
				mixed_strategy.append(0)
		if noise_blocky:
			ran.seed(str(mixed_strategy))
		while True:
			mixed_strategy_distr = []
			for i in range(0, len(mixed_strategy)):
				if i == 0:
					mixed_strategy_distr.append(mixed_strategy[0])
				else:
					mixed_strategy_distr.append(mixed_strategy_distr[i-1] + mixed_strategy[i])
			for i in range(0, len(mixed_strategy_distr) - 1):
				mixed_strategy_distr[i] += ran.uniform(-noise_level, noise_level)
			within_bounds = True
			for i in range(1, len(mixed_strategy_distr)):
				if mixed_strategy_distr[i - 1] > mixed_strategy_distr[i]:
					within_bounds = False
			if within_bounds:
				break
		for i in reversed(range(1, len(mixed_strategy_distr))):
			mixed_strategy_distr[i] -= mixed_strategy_distr[i - 1]
		if noise_blocky:
			ran.seed(str(time.process_time_ns())+str(moves_left)+str(mixed_strategy)) #turn back to random for everyone else
		return Simulator.choose_rational_move(mixed_strategy_distr, neighbors)

	#Finds the highest reward node and chooses a node that will decrease distance to it
	def choose_path_to_highest_imm_move(for_attacker, attacker_location, graph, game_rules, neighbors):
		if for_attacker:
			reward_func = game_rules.get_immediate_reward_revised
		else:
			reward_func = game_rules.get_caught_cost
		highest_node = 0
		for i in range(0, graph.number_of_nodes()):
			if reward_func(i) > reward_func(highest_node):
				highest_node = i
		current_shortest_path = nx.shortest_path_length(graph, attacker_location, highest_node)
		possible_options = []
		for n in neighbors:
			if nx.shortest_path_length(graph, n, highest_node) < current_shortest_path:
				possible_options.append(n)
		if len(possible_options) == 0:
			for n in neighbors:
				if nx.shortest_path_length(graph, n, highest_node) == current_shortest_path:
					possible_options.append(n)
		if len(possible_options) == 0:
			possible_options += neighbors
		return Simulator.choose_random_move(possible_options)

	#Chooses based on the mixed strategies
	def choose_rational_move(mixed_strategy, neighbors):
		random_number = ran.random()
		threshold = 0
		for i in range(0, len(mixed_strategy)):
			threshold += mixed_strategy[i]
			if random_number < threshold:
				return neighbors[i]

	#Chooses completely randomly
	def choose_random_move(options):
		return options[ran.randrange(0, len(options))]

	#Chooses then node with the highest immediate reward
	def choose_myopic_move(options, for_attacker, immediate_rewards, caught_costs):
		if for_attacker:
			rewards = immediate_rewards
		else:
			rewards = caught_costs
		highest = rewards[0]
		for i in range(0, len(options)):
			if rewards[i] > highest:
				highest = rewards[i]
		options = Simulator.get_all_duplicates(options, rewards, highest)
		return Simulator.choose_random_move(options)

	#Chooses the highest weighted choice in the mixed strategy
	def choose_highest_mixed_move(mixed_strategy, neighbors):
		highest = 0
		for i in range(0, len(mixed_strategy)):
			if mixed_strategy[i] > mixed_strategy[highest]:
				highest = i
		highest_strategy = mixed_strategy[highest]
		options = Simulator.get_all_duplicates(neighbors, mixed_strategy, highest_strategy)
		return Simulator.choose_random_move(options)

	#Lets the user input a move
	def choose_user_move(options):
		answer = -1
		while not answer in options:
			try:
				print("Options: " + str(options))
				answer = int(input("Pick a node: "))
				if not answer in options:
					print("That's not a valid choice")
			except ValueError:
				print("That's not a valid choice")
		return answer

	#When there are equal options to choose from, find them all and then pick randomly
	def get_all_duplicates(options, option_values, value):
		possible_options = []
		for i in range(0, len(options)):
			if option_values[i] == value:
				possible_options.append(options[i])
		return possible_options

#Adds 2 lists
def add_lists(list1, list2):
	res_list = []
	for i in range(0, len(list1)):
		res_list.append(list1[i] + list2[i]) 
	return res_list