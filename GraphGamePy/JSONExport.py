#Exports NetworkGameSolution(s) to JSON for use in the javascript game. It doesn't actually export JSON, but instead exports
#a js file containing a js array that contains all of the JSON strings.

import json as js
import Solver as solve
import numpy as np
import copy as cp
import os

class JSONExport:

	#create the object and it will have a blank amount of network_game_solutions
	def __init__(self):
		self.JSON_network_game_solutions = []

	#add a network game solution to the JSON object
	def add_to_JSON(self, network_game_solution):

		adjacency_matrix_1d = []
		for x in range(0, network_game_solution.number_of_nodes):
			for y in range(0, network_game_solution.number_of_nodes):
				adjacency_matrix_1d.append(network_game_solution.network_game.adjacency_matrix[x][y])

		#just turns the tuples into lists for json
		transition_chances_cp = cp.deepcopy(network_game_solution.game_rules.transition_chances)
		for i in range(0, len(transition_chances_cp.branch_start_nodes)):
			transition_chances_cp.destination_nodes[i] = list(network_game_solution.game_rules.transition_chances.destination_nodes[i])
			transition_chances_cp.destination_nodes_chances[i] = list(network_game_solution.game_rules.transition_chances.destination_nodes_chances[i])

		dictionary = {
			"adjacency_matrix": str(adjacency_matrix_1d),
			"number_of_nodes": str(network_game_solution.number_of_nodes),
			"total_moves": str(network_game_solution.total_moves),
			"expected_reward": str(network_game_solution.get_solution_no_zero(network_game_solution.game_rules.start_node, network_game_solution.total_moves).utilities[0]),
			"immediate_rewards": str(network_game_solution.game_rules.immediate_rewards),
			"immediate_rewards_revised": str(network_game_solution.game_rules.immediate_rewards_revised),
			"start_node": str(network_game_solution.game_rules.start_node),
			"end_nodes": str(network_game_solution.game_rules.end_nodes),
			"end_node_values": str(network_game_solution.game_rules.end_node_values),
			"can_be_caught_on_end_node": str(network_game_solution.game_rules.can_be_caught_on_end_node),
			"caught_reward_policy": str(network_game_solution.game_rules.caught_reward_policy.name),
			"caught_cost": str(network_game_solution.game_rules.caught_cost),
			"caught_policy": str(network_game_solution.game_rules.caught_policy.name),
			"branch_start_nodes": str(transition_chances_cp.branch_start_nodes),
			"destination_nodes": str(transition_chances_cp.destination_nodes),
			"destination_nodes_chances": str(transition_chances_cp.destination_nodes_chances)
		}

		for node in range(0, network_game_solution.number_of_nodes):
			for move in range(0, network_game_solution.total_moves):
				coords = "node" + str(node) + ",move" + str(move) + ":"
				dictionary[coords + "attacker_mixed_strategy"] = str(list(network_game_solution.get_solution(node, move).mixed_strategies[0]))
				dictionary[coords + "defender_mixed_strategy"] = str(list(network_game_solution.get_solution(node, move).mixed_strategies[1]))
				dictionary[coords + "attacker_utility"] = str(network_game_solution.get_solution(node, move).utilities[0])

		self.JSON_network_game_solutions.append(js.dumps(dictionary))

	#exports all of the network game solutions that have been added (appending to the file if already exists)
	def export_to_JSON(self):
		output_string = ""
		for s in self.JSON_network_game_solutions:
			output_string += "'" + s + "',"
		if os.path.exists("json_output/GameData.json"):
			f = open("json_output/GameData.json", "r")
			old_string = f.read()
			f.close()
			old_string = old_string[:-1]
			f = open("json_output/GameData.json", "w")
			f.write(old_string + output_string + "]")
			f.close()
		else:
			f = open("json_output/GameData.json", "w")
			f.write("gameData = [" + output_string + "]")
			f.close()