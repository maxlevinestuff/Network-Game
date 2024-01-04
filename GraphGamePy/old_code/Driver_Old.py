#driver for testing stuff

import numpy as np

import Simulator as sim
import Solver as solve
import Draw as dr
import NetworkGame as net
import Rules as rules
import JSONExport as jse
import time
import matplotlib.pyplot as plt

# nodes_TEST = 5
# connected_TEST = 0.15
# #moves_TEST = 5

# results = []

# for moves_TEST in [10, 15, 20, 25]:
# 	start_time = time.time()
# 	network_game = net.NetworkGame.create_random_network_game(nodes_TEST, connected_TEST)
# 	network_game_solution = solve.NetworkGameSolution(moves_TEST, network_game)
# 	simulator = sim.Simulator()
# 	res = simulator.simulate(number_of_simulations=100, network_game_solution=network_game_solution, starting_node=1, total_moves=m5ves_TEST, attacker_strategy=sim.StrategyType.rational, defender_strategy=sim.StrategyType.rational)
# 	results.append((time.time() - start_time))

# print(results)

adjacency_matrix = np.array([[1,0,0,0,0,0,1,0],[0,1,1,1,1,0,0,0],[0,1,1,0,0,0,0,0],[0,1,0,1,0,0,0,0],
	[0,1,0,0,1,1,0,0],[0,0,0,0,1,1,1,1],[1,0,0,0,0,1,1,0],[0,0,0,0,0,1,0,1]])

#immediate_rewards = [1., 3., 5., 2., 1., 6., 2., 4.]
immediate_rewards = [0., 0., 0., 0., 0., 0., 0., 1000.]

transition_chances = rules.TransitionChances([7,2],[(3,0),(3,0)],[(0.5,0.5),(0.4,0.6)])

game_rules = rules.GameRules(immediate_rewards, start_node=0, end_nodes=[], end_node_values=[],
	can_be_caught_on_end_node=True, caught_reward_policy=rules.Options.caught_subtract_from_0,
	caught_cost=50., caught_policy=rules.Options.caught_policy_continue,
	transition_chances=transition_chances)

network_game = net.NetworkGame(adjacency_matrix, game_rules)
#network_game = net.NetworkGame.create_random_network_game(10, .1, number_of_end_nodes=2, directed=True, caught_policy=rules.Options.caught_policy_continue, can_be_caught_on_end_node=True)

for n in range(0, network_game.number_of_nodes):
	print(str(n) + ": " + str(network_game.get_neighbors(n)))

draw = dr.Draw(network_game)
#draw.draw_rules()
draw.draw_nodes_and_edges()
draw.draw_labels()
#draw.show()
dr.clear()
network_game_solution = solve.NetworkGameSolution(10, network_game)

json_export = jse.JSONExport()
json_export.add_to_JSON(network_game_solution)
json_export.export_to_JSON()

print(network_game_solution.get_solution_no_zero(network_game.game_rules.start_node,10).utilities[0])

for strat in [sim.StrategyType.rational, sim.StrategyType.random, sim.StrategyType.highest_mixed, sim.StrategyType.myopic, sim.StrategyType.path_to_highest_imm]:
	print(strat)
	simulator = sim.Simulator()
	res = simulator.simulate(number_of_simulations=10000, network_game_solution=network_game_solution, total_moves=10, attacker_strategy=strat, defender_strategy=sim.StrategyType.rational)
	print(res.actual_reward)
	draw.draw_rules()
	draw.draw_nodes_simulation_frequencies(res)
	draw.draw_simulation_labels(res)
	draw.draw_nodes_and_edges()
	draw.draw_labels()
	draw.draw_labels(immediate_rewards)
	draw.show()
	dr.clear()

num_of_different_graphs = 1 #20
num_of_simulations = 1000

rational_stat = sim.Simulator.GameStats.get_zero_stat(15)
random_stat = sim.Simulator.GameStats.get_zero_stat(15)
myopic_stat = sim.Simulator.GameStats.get_zero_stat(15)
highest_mixed_stat = sim.Simulator.GameStats.get_zero_stat(15)
path_to_highest_imm_stat = sim.Simulator.GameStats.get_zero_stat(15)

d_rational_stat = sim.Simulator.GameStats.get_zero_stat(15)
d_random_stat = sim.Simulator.GameStats.get_zero_stat(15)
d_myopic_stat = sim.Simulator.GameStats.get_zero_stat(15)
d_highest_mixed_stat = sim.Simulator.GameStats.get_zero_stat(15)
d_path_to_highest_imm_stat = sim.Simulator.GameStats.get_zero_stat(15)
network_game = net.NetworkGame.create_random_network_game(15, .2, number_of_end_nodes=2, directed=True, caught_policy=rules.Options.caught_policy_continue, can_be_caught_on_end_node=True)


draw = dr.Draw(network_game)
draw.draw_rules()
draw.draw_nodes_and_edges()
draw.draw_labels()
draw.show()
dr.clear()
network_game_solution = solve.NetworkGameSolution(15, network_game)

simulator = sim.Simulator()

rational_stat += simulator.simulate(number_of_simulations=num_of_simulations, network_game_solution=network_game_solution, total_moves=15, attacker_strategy=sim.StrategyType.rational, defender_strategy=sim.StrategyType.rational)
random_stat += simulator.simulate(number_of_simulations=num_of_simulations, network_game_solution=network_game_solution, total_moves=15, attacker_strategy=sim.StrategyType.random, defender_strategy=sim.StrategyType.rational)
myopic_stat += simulator.simulate(number_of_simulations=num_of_simulations, network_game_solution=network_game_solution, total_moves=15, attacker_strategy=sim.StrategyType.myopic, defender_strategy=sim.StrategyType.rational)
highest_mixed_stat += simulator.simulate(number_of_simulations=num_of_simulations, network_game_solution=network_game_solution, total_moves=15, attacker_strategy=sim.StrategyType.highest_mixed, defender_strategy=sim.StrategyType.rational)
path_to_highest_imm_stat += simulator.simulate(number_of_simulations=num_of_simulations, network_game_solution=network_game_solution, total_moves=15, attacker_strategy=sim.StrategyType.path_to_highest_imm, defender_strategy=sim.StrategyType.rational)

d_rational_stat += simulator.simulate(number_of_simulations=num_of_simulations, network_game_solution=network_game_solution, total_moves=15, attacker_strategy=sim.StrategyType.rational, defender_strategy=sim.StrategyType.rational)
d_random_stat += simulator.simulate(number_of_simulations=num_of_simulations, network_game_solution=network_game_solution, total_moves=15, attacker_strategy=sim.StrategyType.rational, defender_strategy=sim.StrategyType.random)
d_myopic_stat += simulator.simulate(number_of_simulations=num_of_simulations, network_game_solution=network_game_solution, total_moves=15, attacker_strategy=sim.StrategyType.rational, defender_strategy=sim.StrategyType.myopic)
d_highest_mixed_stat += simulator.simulate(number_of_simulations=num_of_simulations, network_game_solution=network_game_solution, total_moves=15, attacker_strategy=sim.StrategyType.rational, defender_strategy=sim.StrategyType.highest_mixed)
d_path_to_highest_imm_stat += simulator.simulate(number_of_simulations=num_of_simulations, network_game_solution=network_game_solution, total_moves=15, attacker_strategy=sim.StrategyType.rational, defender_strategy=sim.StrategyType.path_to_highest_imm)

rational_stat /= (num_of_different_graphs * num_of_simulations)
random_stat /= (num_of_different_graphs * num_of_simulations)
myopic_stat /= (num_of_different_graphs * num_of_simulations)
highest_mixed_stat /= (num_of_different_graphs * num_of_simulations)
path_to_highest_imm_stat /= (num_of_different_graphs * num_of_simulations)

d_rational_stat /= (num_of_different_graphs * num_of_simulations)
d_random_stat /= (num_of_different_graphs * num_of_simulations)
d_myopic_stat /= (num_of_different_graphs * num_of_simulations)
d_highest_mixed_stat /= (num_of_different_graphs * num_of_simulations)
d_path_to_highest_imm_stat /= (num_of_different_graphs * num_of_simulations)

needed_network_game = net.NetworkGame.create_random_network_game(number_of_nodes=15)
draw = dr.Draw(needed_network_game)
actual_to_expected = []
titles = ["Rational", "Highest Mixed", "Random", "Myopic", "Path to Highest Immediate"]
print("Attacker")
for stat in [rational_stat, highest_mixed_stat, random_stat, myopic_stat, path_to_highest_imm_stat]:
	print()
	print(stat.actual_reward / stat.expected_reward)
	actual_to_expected.append(stat.actual_reward / network_game_solution.get_solution_no_zero(network_game.game_rules.start_node, 15).utilities[0])
	draw.draw_simulation_histogram(stat)
draw.show()
dr.clear()
x_pos = [i for i, _ in enumerate(titles)]
plt.bar(x_pos, actual_to_expected)
plt.xlabel("Attacker Strategy")
plt.ylabel("Actual to Expected")
plt.xticks(x_pos, titles)
plt.show()
dr.clear()

actual_to_expected2 = []
titles = ["Rational", "Highest Mixed", "Random", "Myopic", "Path to Highest Immediate"]
print("Defender")
for stat in [d_rational_stat, d_highest_mixed_stat, d_random_stat, d_myopic_stat, d_path_to_highest_imm_stat]:
	print()
	print(stat.actual_reward / stat.expected_reward)
	actual_to_expected2.append(stat.actual_reward / network_game_solution.get_solution_no_zero(network_game.game_rules.start_node, 15).utilities[1])
	draw.draw_simulation_histogram(stat)
draw.show()
dr.clear()
x_pos = [i for i, _ in enumerate(titles)]
plt.bar(x_pos, actual_to_expected2)
plt.xlabel("Defender Strategy")
plt.ylabel("Actual to Expected")
plt.xticks(x_pos, titles)
plt.show()
dr.clear()
