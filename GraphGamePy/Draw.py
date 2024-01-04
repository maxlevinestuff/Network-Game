#Handles drawing. Create Draw with a specific network game, then call each of the functions to add to the drawing.
#To print, use show(), and to clear use clear()

import networkx as nx 
import matplotlib.pyplot as plt
import os.path as path

NODE_SIZE = 400 #Size of a regular node
FREQUENCY_MULTIPLIER = 1800 #how much to scale up the color circles around the nodes indicating the visitation frequencies

class Draw:

	#Initialize with a matrix game
	def __init__(self, network_game):

		self.nx_graph = nx.from_numpy_matrix(network_game.adjacency_matrix, create_using=nx.DiGraph)
		self.pos = nx.networkx.kamada_kawai_layout(self.nx_graph)
		#self.pos = nx.networkx.planar_layout(self.nx_graph)
		self.network_game = network_game

	#Get the pos and set to make another graph with same number of nodes to have the same layout
	def get_pos(self):
		return self.pos
	def set_pos(self, new_pos):
		self.pos = new_pos

	#draws the game rules above the image
	def draw_rules(self):
		plt.figtext(0,1,self.network_game.game_rules.get_display_string(), color="black")

	#Draws the imm. reward, caught cost, and node numbers on each node
	def draw_labels(self):

		draw_caught_cost_per_node = True
		if self.network_game.game_rules.caught_cost == None or not isinstance(self.network_game.game_rules.caught_cost, list):
			draw_caught_cost_per_node = False

		truncated_reward_values = []
		#get rid of the .0 at the end of the immediate rewards
		for i in self.network_game.game_rules.immediate_rewards_revised:
			label = truncate_float(i)
			if draw_caught_cost_per_node:
				label += "\n"
			truncated_reward_values.append(label)

		node_to_reward_dictionary = two_lists_to_dictionary(range(0, self.network_game.number_of_nodes), truncated_reward_values)

		nx.draw_networkx_labels(self.nx_graph, self.pos, labels=node_to_reward_dictionary, font_weight="bold", font_color="#FF0000", font_size=7)

		if draw_caught_cost_per_node:

			truncated_caught_values = []
			#get rid of the .0 at the end of the immediate rewards
			for i in self.network_game.game_rules.caught_cost:
				label = "\n" + truncate_float(i)
				truncated_caught_values.append(label)

			node_to_reward_dictionary = two_lists_to_dictionary(range(0, self.network_game.number_of_nodes), truncated_caught_values)

			nx.draw_networkx_labels(self.nx_graph, self.pos, labels=node_to_reward_dictionary, font_weight="bold", font_color="#00ccff", font_size=7)

		#node number
		node_num_label = list(range(0, self.network_game.number_of_nodes))
		for i in range(0, self.network_game.number_of_nodes):
			node_num_label[i] = "         " + str(node_num_label[i])
		node_to_reward_dictionary = two_lists_to_dictionary(range(0, self.network_game.number_of_nodes), node_num_label)
		nx.draw_networkx_labels(self.nx_graph, self.pos, labels=node_to_reward_dictionary, font_weight="bold", font_color="white", font_size=6)

		#nx.draw(self.nx_graph, with_labels=True)

	#Draws a ton of txt on each node with all the mixed strategies and utilities
	def draw_labels_solution(self, network_game_solution, moves_left):
		
		labels = []

		for i in range(0, network_game_solution.number_of_nodes):

			solution_for_node_i = network_game_solution.get_solution(i, moves_left)
			neighbors_of_node_i = network_game_solution.get_neighbors(i)

			label_string = ""
			label_string += "node: " + str(i) + "\n"
			label_string += "imm. reward: " + truncate_float(network_game_solution.get_immediate_rewards()[i]) + "\n"
			label_string += "utility: " + truncate_float(solution_for_node_i.utilities[0],2) + "\n"

			for index in [0, 1]:
				label_string += ["attacker strat.:\n", "defender strat.:\n"][index]
				for j in range(0, len(solution_for_node_i.mixed_strategies[0])):
					label_string += "to node " + str(neighbors_of_node_i[j]) + ": " + truncate_float(solution_for_node_i.mixed_strategies[index][j]*100, 2) + "% \n"

			labels.append(label_string)

		node_to_reward_dictionary = two_lists_to_dictionary(range(0, len(labels)), labels)

		nx.draw_networkx_labels(self.nx_graph, self.pos, labels=node_to_reward_dictionary, font_size=5, font_weight="bold")

	#Draws different sized nodes depending on the frequency of visitation in the simulations
	def draw_nodes_simulation_frequencies(self, results):

		nx.draw_networkx_nodes(self.nx_graph, self.pos, node_color="#FF0000", alpha=.4, node_size=[i * FREQUENCY_MULTIPLIER + (NODE_SIZE if i!=0 else 0) for i in results.attacker_move_history])
		nx.draw_networkx_nodes(self.nx_graph, self.pos, node_color="#0000ff", alpha=.4, node_size=[i * FREQUENCY_MULTIPLIER + (NODE_SIZE if i!=0 else 0) for i in results.defender_move_history])
		#nx.draw_networkx_edges(self.nx_graph, self.pos, color="#808080", alpha=0.2, width=2.0)

	#Draws the textual results of the simulation
	def draw_simulation_labels(self, results):
		string = "attacker strategy: " + results.attacker_strategy.name + ", score: " + str(results.actual_reward)
		string += "\ndefender strategy: " + results.defender_strategy.name
		string += "\nnumber of simulations: " + str(results.number_of_simulations)
		string += "                expected rational score: " + str(results.expected_reward)
		plt.figtext(0,0,string,color="black") #FFFFFF

	#Makes a histogram of the results
	#Should be used seperately (in between clear()) from everything else!
	def draw_simulation_histogram(self, results):
		#label = results.attacker_strategy.name + " attacker, " + results.defender_strategy.name + " defender"
		#plt.hist(results.ratio_list, alpha=0.35, label=label, range=(-15,15), bins=60, log=True)
		plt.hist(results.ratio_list, log=True)
		plt.legend(loc='upper right')

	#Draw all the nodes and edges, you'll always want to call this one
	def draw_nodes_and_edges(self):

		non_start_or_end_nodes = []
		for i in range(self.network_game.number_of_nodes):
			if not i in self.network_game.game_rules.end_nodes and not i==self.network_game.game_rules.start_node:
				non_start_or_end_nodes.append(i)

		nx.draw_networkx_nodes(self.nx_graph, self.pos, nodelist=non_start_or_end_nodes, node_shape='o', node_color="#000000", node_size=NODE_SIZE)
		nx.draw_networkx_nodes(self.nx_graph, self.pos, nodelist=self.network_game.game_rules.end_nodes, node_shape='H', node_color="#000000", node_size=NODE_SIZE)
		nx.draw_networkx_nodes(self.nx_graph, self.pos, nodelist=[self.network_game.game_rules.start_node], node_shape='>', node_color="#000000", node_size=NODE_SIZE)

		#nx.draw_networkx_nodes(self.nx_graph, self.pos, alpha=1, node_size=100)
		#nx.draw_networkx_nodes(self.nx_graph, self.pos, alpha=0.3, node_size=500)

		nx.draw_networkx_edges(self.nx_graph, self.pos, color="#808080", width=2.0, arrows=True)

	#Output the image to image_output
	def show(self, show=False):
		plt.tight_layout()
		plt.savefig(Draw.get_next_file_name(), transparent=True, bbox_inches='tight', pad_inches=0.1)
		if show:
			plt.show()

	#Used for outputting image
	def get_next_file_name():
		file_number = 1
		while path.isfile("image_output/figure" + str(file_number) + ".png"):
			file_number += 1
		return "image_output/figure" + str(file_number) + ".png"

#Clears the current drawing
def clear():
	plt.clf()

def two_lists_to_dictionary(keys, values):
	return {keys[i]: values[i] for i in range(len(keys))}

def truncate_float(f, round_to=None):
	n = f
	if round_to != None:
		n = round(n, round_to)
	return '{0:g}'.format(n)