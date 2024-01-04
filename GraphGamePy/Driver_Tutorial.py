#This driver will walk you through using all of the various code features

#Import all the dependencies
import numpy as np
import Simulator as sim
import Solver as solve
import Draw as dr
import NetworkGame as net
import Rules as rules
import JSONExport as jse
import time
import matplotlib.pyplot as plt

#Set the immediate rewards for each node (8 nodes here)
immediate_rewards = [1., 3., 5., 2., 1., 6., 2., 4.]
#Create some transition chances
#So if land on node 7, 50% chance to go to node 3, 50% to go to node 0, and similar for node 2
transition_chances = rules.TransitionChances([7,2],[(3,0),(3,0)],[(0.5,0.5),(0.4,0.6)])
#Use the transition chances in addition to more options to create the game rules
game_rules = rules.GameRules(immediate_rewards, start_node=0, end_nodes=[7], end_node_values=[50.],
	can_be_caught_on_end_node=True, caught_reward_policy=rules.Options.caught_subtract_from_0,
	caught_cost=50., caught_policy=rules.Options.caught_policy_continue,
	transition_chances=transition_chances)
#Create an adjacency matrix for the graph
adjacency_matrix = np.array([[1,0,0,0,0,0,1,0],[0,1,1,1,1,0,0,0],[0,1,1,0,0,0,0,0],[0,1,0,1,0,0,0,0],
	[0,1,0,0,1,1,0,0],[0,0,0,0,1,1,1,1],[1,0,0,0,0,1,1,0],[0,0,0,0,0,1,0,1]])
#Finally, create the network game from the adjacency matrix and rules
network_game = net.NetworkGame(adjacency_matrix, game_rules)

#We can also generate a random network game instead
#Any non-specified parameter will be randomized
random_network_game = net.NetworkGame.create_random_network_game(
	number_of_nodes=8, connectedness=.1, number_of_end_nodes=2, directed=True,
	caught_policy=rules.Options.caught_policy_continue, can_be_caught_on_end_node=True)

#Now we're ready to solve the network game, and do so for up to 10 moves (can be extended later)
network_game_solution = solve.NetworkGameSolution(10, network_game)

#We can export the network_game_solution(s) to JSON for use in the JS game
json_export = jse.JSONExport()
json_export.add_to_JSON(network_game_solution)
#Will export to json_output
json_export.export_to_JSON()

#Now we can run simulations and get results
simulator = sim.Simulator()
results = simulator.simulate(number_of_simulations=1000, network_game_solution=network_game_solution, total_moves=network_game_solution.total_moves,
	attacker_strategy=sim.StrategyType.rational, defender_strategy=sim.StrategyType.rational)
#You can add GameStats from different simulations (of different graphs) with "+" but make sure to divide the GameStats object by however many you do to average them

#We can access the results by calling them, but lets use Draw to draw the results
draw = dr.Draw(network_game)
#Now we can call various functions to add different things to the drawing
draw.draw_rules()
draw.draw_nodes_simulation_frequencies(results)
draw.draw_simulation_labels(results)
draw.draw_nodes_and_edges()
draw.draw_labels()
#The image will be outputted to image_output
draw.show()
dr.clear()