#Describes the details of the rules of the game. Combined with an adjacency matrix, forms a network game.

from enum import Enum
import random as ran

import NetworkGame as net
import Common as com

#These options are used for the caught_reward_policy and caught_policy parameters, respectively
class Options(Enum):

	#caught reward options
	caught_negate_from_reward = 1        #To get the caught cost, negate the immediate reward value for the node
	caught_subtract_from_reward = 2      #To get the caught cost, subtract the caught cost from the immediate reward value
	caught_subtract_from_0 = 3           #The caught cost is just the set caught cost, negated

	#caught policy options
	caught_policy_continue = 4           #When caught, continue the game
	caught_policy_end_game = 5           #When caught, end the game
	caught_policy_block = 6              #When caught, the attacker is blocked and can't move to where they were trying to
	caught_policy_return_to_start = 7    #When caught, attacker returns to the start node

#Contains the all the environmental transition chances
class TransitionChances:

	#e.g.: [1,2],[(2,4),(3,7)],[(0.5,0.5),(0.3,0.7)]
	#so if land on node 1, there would be a 50% chance to move to node 2 and 50% to move to node 4
	def __init__(self, branch_start_nodes, destination_nodes, destination_nodes_chances):
		self.branch_start_nodes = branch_start_nodes
		self.destination_nodes = destination_nodes
		self.destination_nodes_chances = destination_nodes_chances

	#randomly calculates the node to move to
	def get_node_to_move_to(self, current_node):
		if self.branch_start_nodes:
			for n in range(0, len(self.branch_start_nodes)):
				if current_node == self.branch_start_nodes[n]:
					random_number = ran.random()
					threshold = 0
					for i in range(0, len(self.destination_nodes[n])):
						threshold += self.destination_nodes_chances[n][i]
						if random_number < threshold:
							return self.destination_nodes[n][i]
		return current_node

#Describes all the rules of the game
class GameRules:

	def __init__(self,
		immediate_rewards,
		start_node=0,
		end_nodes=[], end_node_values=[], can_be_caught_on_end_node=False,
		caught_reward_policy=Options.caught_negate_from_reward, caught_cost=None, caught_policy=Options.caught_policy_continue,
		transition_chances=TransitionChances([],[],[])):

		self.immediate_rewards = immediate_rewards

		self.start_node = start_node

		self.end_nodes = end_nodes
		self.end_node_values = end_node_values

		self.caught_reward_policy = caught_reward_policy
		self.can_be_caught_on_end_node = can_be_caught_on_end_node
		self.caught_cost = caught_cost
		self.caught_policy = caught_policy

		self.immediate_rewards_revised = self.get_reward_values_revised()

		self.transition_chances = transition_chances

	#Gives a string describing the game rules. Include_extra will include stuff that will already be represented in Draw graphics
	def get_display_string(self, include_extra=False):
		string = "caught reward policy: " + str(self.caught_reward_policy.name)
		string += "\ncaught policy: " + str(self.caught_policy.name)
		string += "\ncan be caught on end node: " + str(self.can_be_caught_on_end_node)
		if include_extra:
			string += "\nstart node: " + str(self.start_node)
		if include_extra or not isinstance(self.caught_cost, list):
			string += "\ncaught cost: " + str(self.caught_cost)
		if include_extra:
			string += "\nnodes: " + str(list(range(0, len(self.immediate_rewards_revised))))
			string += "\nimmediate_rewards: " + str(self.immediate_rewards_revised)
			string += "\nend nodes: " + str(self.end_nodes)
			string += "\nend node values: " + str(self.end_node_values)
		return string

	#Returns a list of the caught costs of all adjacent nodes to a given node
	def get_surrounding_caught_costs(self, neighbors):
		if not isinstance(self.caught_cost, list):
			return self.caught_cost
		costs = []
		for i in neighbors:
			costs.append(self.caught_cost[i])
		return costs

	#Gets the cost of being caught on a specific node
	def get_caught_cost(self, node):
		if not isinstance(self.caught_cost, list):
			return self.caught_cost
		return self.caught_cost[node]

	#Gets the immediate reward, overwriting the value of a node if it is an end node to the end node value
	def get_immediate_reward_revised(self, node):
		return self.immediate_rewards_revised[node]

	#Returns a list of the reward values of the given nodes
	def get_surrounding_immediate_rewards(self, neighbors):
		rewards = []
		for i in neighbors:
			rewards.append(self.immediate_rewards[i])
		return rewards

	#Returns a list of the reward values of the given nodes
	def get_surrounding_immediate_rewards_revised(self, neighbors):
		rewards = []
		for i in neighbors:
			rewards.append(self.immediate_rewards_revised[i])
		return rewards

	#get the reward values by subsituting in the end node values
	def get_reward_values_revised(self):
		revised_reward_values = self.immediate_rewards[:]
		for e in range(len(self.end_nodes)):
			revised_reward_values[self.end_nodes[e]] = self.end_node_values[e]
		return revised_reward_values