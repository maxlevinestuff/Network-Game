#This code solves the ransomware flow chart

import numpy as np

import Simulator as sim
import Solver as solve
import Draw as dr
import NetworkGame as net
import Rules as rules
import JSONExport as jse
import time
import matplotlib.pyplot as plt

#This was created partially with NetworkX, but weirdly it bugged out for part of it. Starting from an edge list would be
#easier, to build a graph.
adjacency_matrix= np.array([[0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
		[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

#Create the transition chances
transition_chances = rules.TransitionChances([7,8,9,4],[(2,10),(2,11),(2,12),(2,6)],[(0.,1.),(.4,.6),(.6,.4),(.5,.5)])

immediate_rewards = [0., -50., 0., 0., -34., -200., 0., 0., 0., 0., 0., 0., 0., 45000., 70000., 90000.]

#since the defender is ignored here, the caught costs are just the negation of the rewards, so it doesn't matter if the
#defender catches or not
costs = [ -x for x in immediate_rewards]

total_moves = 30

game_rules = rules.GameRules(immediate_rewards, start_node=0, end_nodes=[], end_node_values=[],
	can_be_caught_on_end_node=True, caught_reward_policy=rules.Options.caught_subtract_from_0,
	caught_cost=costs, caught_policy=rules.Options.caught_policy_continue,
	transition_chances=transition_chances)

network_game = net.NetworkGame(adjacency_matrix, game_rules)

for n in range(0, network_game.number_of_nodes):
	print(str(n) + ": " + str(network_game.get_neighbors(n)))

draw = dr.Draw(network_game)
draw.draw_rules()
draw.draw_nodes_and_edges()
draw.draw_labels()
draw.show()
dr.clear()
network_game_solution = solve.NetworkGameSolution(total_moves, network_game)

mixed_strategies = []
for i in reversed(range(0, total_moves)):
	mixed_strategies.append(network_game_solution.get_solution(6, i).mixed_strategies[0][2])
print(sum(mixed_strategies)/len(mixed_strategies))
ax = plt.gca()
ax.set_axis_off()
plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
            hspace = 0, wspace = 0)
plt.margins(0,0)
plt.plot(mixed_strategies, color='black')
plt.fill_between(list((range(0,total_moves))), 0, mixed_strategies, color='black')

json_export = jse.JSONExport()
json_export.add_to_JSON(network_game_solution)
json_export.export_to_JSON()

print(network_game_solution.get_solution_no_zero(network_game.game_rules.start_node,total_moves).utilities[0])

for strat in [sim.StrategyType.rational, sim.StrategyType.random, sim.StrategyType.highest_mixed, sim.StrategyType.myopic, sim.StrategyType.path_to_highest_imm]:
	print(strat)
	simulator = sim.Simulator()
	res = simulator.simulate(number_of_simulations=100000, network_game_solution=network_game_solution, total_moves=total_moves, attacker_strategy=strat, defender_strategy=sim.StrategyType.rational)
	print(res.actual_reward)
	draw.draw_rules()
	draw.draw_nodes_simulation_frequencies(res)
	draw.draw_simulation_labels(res)
	draw.draw_nodes_and_edges()
	draw.draw_labels()
	draw.show()
	dr.clear()