import networkx as nx
import math
import random as ran
import copy as cp
import numpy as np
from datetime import datetime

import Rules as rules

#A network of nodes with reward values
class NetworkGame:

	#create a new network game
	def __init__(self, adjacency_matrix, game_rules):
		self.adjacency_matrix = adjacency_matrix
		self.immediate_rewards = game_rules.immediate_rewards
		self.number_of_nodes = len(self.adjacency_matrix)
		self.game_rules = game_rules

	#Returns a list of all adjacent nodes to a given node in the adjacency_matrix
	def get_neighbors(self, node):
		length = self.number_of_nodes
		neighbors = []
		for i in range(0, length):
			if self.adjacency_matrix[node,i] == 1:
				neighbors.append(i)
		return neighbors

	#check if graph is connected
	def connectedness_check(directed, graph):
		if directed:
			return nx.is_semiconnected(graph)
		else:
			return nx.is_connected(graph)

	#generate a completely random network game. any optional parameter not supplied will be chosen randomly
	def create_random_network_game(
		number_of_nodes=None, connectedness=None, random_reward_range=range(5,20), rewards=None,
		caught_reward_policy=None, random_caught_cost_range=range(5,20), caught_cost=None, number_of_end_nodes=None,
		random_end_node_value_range=range(50,200), end_node_values=None, can_be_caught_on_end_node=None, caught_policy=None,
		directed=None, self_connected=None, planar=True): #set self_connected to full, semi, or none

		#ensure a connected graph using a sharp threshold
		#lower_bound = math.log(number_of_nodes) / number_of_nodes
		#new_connectedness = lower_bound + ((1 - lower_bound) * connectedness)
		#graph = nx.erdos_renyi_graph(number_of_nodes, new_connectedness)
		#if not nx.is_connected(graph):
		#	return get_random_network_game(number_of_nodes, connectedness)

		if number_of_nodes == None:
			number_of_nodes = ran.randrange(10,25)
		if connectedness == None:
			connectedness = ran.uniform(0.05, 0.25)

		if directed == None:
			directed = ran.choice([True, False])
		if self_connected == None:
			self_connected = ran.choice(["full", "semi", "none"])

		if number_of_end_nodes == None:
			number_of_end_nodes = ran.randrange(0, math.floor(number_of_nodes / 5))

		print("Getting random graph. May take forever with the wrong parameters.")
		start_node = None
		while True:
			while True:
				graph = nx.erdos_renyi_graph(number_of_nodes, connectedness, directed=directed)
				start_node = NetworkGame.find_usable_start_node(graph)
				end_nodes = NetworkGame.find_usable_end_nodes(directed, graph, number_of_end_nodes, start_node)

				if not planar or nx.check_planarity(graph):
					if NetworkGame.connectedness_check(directed, graph) and start_node != -1 and end_nodes != -1:
						break

			if not directed:
				NetworkGame.remove_edges_between_end_nodes(graph, end_nodes)
				if nx.is_connected(graph) and NetworkGame.usable_start_node(graph, start_node):
					break
			else:
				NetworkGame.remove_edges_from_end_nodes(graph, end_nodes)
				if nx.is_weakly_connected(graph) and NetworkGame.usable_start_node(graph, start_node):
					break

		adjacency_matrix = np.array(nx.adjacency_matrix(graph).todense())

		#handle node self-connected
		for i in range(0, number_of_nodes):
			if self_connected == "full":
				adjacency_matrix[i,i] = 1
			elif self_connected == "none":
				adjacency_matrix[i,i] = 0
			elif self_connected == "semi":
				r = ran.random()
				if r <= connectedness:
					adjacency_matrix[i,i] = 1
				else:
					adjacency_matrix[i,i] = 0

		if rewards == None:
			reward_list = []
			for i in range(0, number_of_nodes):
				reward_list.append(ran.choice(random_reward_range))
		else:
			reward_list = rewards

		#game rules time

		if caught_reward_policy == None:
			caught_reward_policy = ran.choice([rules.Options.caught_negate_from_reward, rules.Options.caught_subtract_from_reward, rules.Options.caught_subtract_from_0])

		if caught_cost == None:
			caught_cost = []
			for i in range(0, number_of_nodes):
				caught_cost.append(ran.choice(random_caught_cost_range))

		if end_node_values == None:
			end_node_values = []
			for i in range(0, number_of_end_nodes):
				end_node_values.append(ran.choice(random_end_node_value_range))

		if caught_policy == None:
			caught_policy = ran.choice([rules.Options.caught_policy_continue, rules.Options.caught_policy_end_game, rules.Options.caught_policy_block, rules.Options.caught_policy_return_to_start])


		if can_be_caught_on_end_node == None:
			can_be_caught_on_end_node = ran.choice([True, False])

		game_rules = rules.GameRules(reward_list, start_node, end_nodes, end_node_values, can_be_caught_on_end_node, caught_reward_policy, caught_cost, caught_policy)

		return NetworkGame(adjacency_matrix, game_rules)

	#finds a start node using the below function
	def find_usable_start_node(graph):
		nodes_to_try = list(range(0, graph.number_of_nodes()))
		ran.shuffle(nodes_to_try)
		for n in nodes_to_try:
			if NetworkGame.usable_start_node(graph, n):
				return n
		return -1
	#a usuable start node has to be able to access all other nodes in the graph
	def usable_start_node(graph, node):
		usable = True
		for n in range(0, graph.number_of_nodes()):
			if not nx.has_path(graph, node, n):
				usable = False
				break
		return usable

	#finds end nodes using the below function
	def find_usable_end_nodes(directed, graph, number_of_end_nodes, start_node):
		end_nodes = []
		nodes_to_try = list(range(0, graph.number_of_nodes()))
		ran.shuffle(nodes_to_try)
		index = 0
		while len(end_nodes) < number_of_end_nodes:
			if index >= graph.number_of_nodes():
				return -1
			if NetworkGame.usable_end_node(directed, graph, nodes_to_try[index], end_nodes) and nodes_to_try[index] != start_node and not nodes_to_try[index] in end_nodes:
				end_nodes.append(nodes_to_try[index])
			index += 1
		return end_nodes
	#only allow end nodes that aren't chokepoints (i.e. removing them would result in a disconnected graph)
	def usable_end_node(directed, graph, end_node, other_end_nodes):
		graph_copy = cp.deepcopy(graph)
		if directed:
			NetworkGame.remove_edges_from_end_nodes(graph_copy, [end_node] + other_end_nodes)
		graph_copy.remove_node(end_node)
		one_usable = NetworkGame.connectedness_check(directed, graph_copy)
		for n in other_end_nodes:
			graph_copy.remove_node(n)
		all_usable = NetworkGame.connectedness_check(directed, graph_copy)
		return one_usable and all_usable

	#remove edges going from end nodes
	def remove_edges_from_end_nodes(graph, end_nodes):
		for end in end_nodes:
			for edge in range(0, graph.number_of_nodes()):
				if graph.has_edge(end, edge):
					graph.remove_edge(end, edge)
	#remove edges going between end nodes
	def remove_edges_between_end_nodes(graph, end_nodes):
		for e1 in end_nodes:
			for e2 in end_nodes:
				if graph.has_edge(e1, e2):
					graph.remove_edge(e1, e2)
				if graph.has_edge(e2, e1):
					graph.remove_edge(e2, e1)