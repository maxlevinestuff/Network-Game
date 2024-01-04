#Tests all the strategies against some random network games and plots the results

import numpy as np

import Simulator as sim
import Solver as solve
import Draw as dr
import NetworkGame as net
import Rules as rules
import JSONExport as jse
import time
import random as ran
import matplotlib.pyplot as plt

def get_strat(s):
	if s=="Rational":
		return sim.StrategyType.rational
	if s=="Random":
		return sim.StrategyType.random
	if s=="Myopic":
		return sim.StrategyType.myopic
	if s=="Highest Mixed":
		return sim.StrategyType.highest_mixed
	if s=="Path to Highest Imm.":
		return sim.StrategyType.path_to_highest_imm

random_network_games = []
def add_network_game(network_game):
	random_network_games.append(network_game)
	draw = dr.Draw(network_game)
	draw.draw_rules()
	draw.draw_nodes_and_edges()
	draw.draw_labels()
	draw.show()
	dr.clear()
print("done random graph gen")

NUMBER_OF_NETWORKS = 10

NUMBER_OF_SIMULATIONS = 12000

#did these 1 at a time with seeds so I could replace a specific one if there was an issue
ran.seed(234)
add_network_game(net.NetworkGame.create_random_network_game(planar=True, number_of_nodes=ran.randrange(8,17), caught_policy=rules.Options.caught_policy_continue))
ran.seed(100)
add_network_game(net.NetworkGame.create_random_network_game(planar=True, number_of_nodes=ran.randrange(8,17), caught_policy=rules.Options.caught_policy_continue))
ran.seed(101)
add_network_game(net.NetworkGame.create_random_network_game(planar=True, number_of_nodes=ran.randrange(8,17), caught_policy=rules.Options.caught_policy_continue))
ran.seed(19)
add_network_game(net.NetworkGame.create_random_network_game(planar=True, number_of_nodes=ran.randrange(8,17), caught_policy=rules.Options.caught_policy_continue))
ran.seed(100)
add_network_game(net.NetworkGame.create_random_network_game(planar=True, number_of_nodes=ran.randrange(8,17), caught_policy=rules.Options.caught_policy_continue))
ran.seed(34235)
add_network_game(net.NetworkGame.create_random_network_game(planar=True, number_of_nodes=ran.randrange(8,17), caught_policy=rules.Options.caught_policy_end_game))
ran.seed(23522)
add_network_game(net.NetworkGame.create_random_network_game(planar=True, number_of_nodes=ran.randrange(8,17), caught_policy=rules.Options.caught_policy_continue))
ran.seed(987)
add_network_game(net.NetworkGame.create_random_network_game(planar=True, number_of_nodes=ran.randrange(8,17), caught_policy=rules.Options.caught_policy_block))
ran.seed(124)
add_network_game(net.NetworkGame.create_random_network_game(planar=True, number_of_nodes=ran.randrange(8,17), caught_policy=rules.Options.caught_policy_continue))
ran.seed(643)
add_network_game(net.NetworkGame.create_random_network_game(planar=True, number_of_nodes=ran.randrange(8,17), caught_policy=rules.Options.caught_policy_continue))
ran.seed(1)
add_network_game(net.NetworkGame.create_random_network_game(planar=True, number_of_nodes=ran.randrange(8,17), caught_policy=rules.Options.caught_policy_return_to_start))

json_export = jse.JSONExport()

random_network_games_solutions = []
for i in range(0, NUMBER_OF_NETWORKS):
	random_network_games_solutions.append(solve.NetworkGameSolution(ran.randrange(8,20), random_network_games[i]))
	json_export.add_to_JSON(random_network_games_solutions[i])
	print("solved " + str(i))
json_export.export_to_JSON()

game_stats_a = {
  "Rational": sim.Simulator.GameStats.get_zero_stat(1),
  "Highest Mixed": sim.Simulator.GameStats.get_zero_stat(1),
  "Random": sim.Simulator.GameStats.get_zero_stat(1),
  "Myopic": sim.Simulator.GameStats.get_zero_stat(1),
  "Path to Highest Imm.": sim.Simulator.GameStats.get_zero_stat(1)
}

game_stats_d = {
  "Rational": sim.Simulator.GameStats.get_zero_stat(1),
  "Highest Mixed": sim.Simulator.GameStats.get_zero_stat(1),
  "Random": sim.Simulator.GameStats.get_zero_stat(1),
  "Myopic": sim.Simulator.GameStats.get_zero_stat(1),
  "Path to Highest Imm.": sim.Simulator.GameStats.get_zero_stat(1)
}

titles = ["Rational", "Highest Mixed", "Random", "Myopic", "Path to Highest Imm."]

simulator = sim.Simulator(for_attacker=True)
for stat in game_stats_a:
	for sol in random_network_games_solutions:
		game_stats_a[stat] += simulator.simulate(number_of_simulations=NUMBER_OF_SIMULATIONS, network_game_solution=sol, total_moves=sol.total_moves, attacker_strategy=get_strat(stat), defender_strategy=sim.StrategyType.rational)
		game_stats_a[stat] /= NUMBER_OF_NETWORKS
		print("did sim " + stat + "a")

simulator = sim.Simulator(for_attacker=False)
for stat in game_stats_d:
	for sol in random_network_games_solutions:
		game_stats_d[stat] += simulator.simulate(number_of_simulations=NUMBER_OF_SIMULATIONS, network_game_solution=sol, total_moves=sol.total_moves, attacker_strategy=sim.StrategyType.rational, defender_strategy=get_strat(stat))
		game_stats_d[stat] /= NUMBER_OF_NETWORKS
		print("did sim " + stat + "d")

plt.tight_layout()
dumb_network_game = net.NetworkGame.create_random_network_game(number_of_nodes=5)
draw = dr.Draw(dumb_network_game)
actual_to_expected = []
print("Attacker")
for stat in game_stats_a:
 	print()
 	print(game_stats_a[stat].actual_reward / game_stats_a[stat].expected_reward)
 	actual_to_expected.append(game_stats_a[stat].actual_reward / game_stats_a[stat].expected_reward)
 	plt.title(stat + " Attacker, Rational Defender")
 	draw.draw_simulation_histogram(game_stats_a[stat])
 	plt.gca().get_legend().remove()
 	draw.show()
 	dr.clear()
x_pos = [i for i, _ in enumerate(titles)]
plt.bar(x_pos, actual_to_expected)
#plt.gca().set_ylim([0.7,1.45])
plt.title("Various Attacker vs. Rational Defender")
plt.xlabel("Attacker Strategy")
plt.ylabel("Actual to Expected")
plt.xticks(x_pos, titles)
plt.savefig(dr.Draw.get_next_file_name(), transparent=True, bbox_inches='tight', pad_inches=0.1)
dr.clear()

dumb_network_game = net.NetworkGame.create_random_network_game(number_of_nodes=5)
draw = dr.Draw(dumb_network_game)
actual_to_expected = []
print("Attacker")
for stat in game_stats_d:
 	print()
 	print(game_stats_d[stat].actual_reward / game_stats_d[stat].expected_reward)
 	actual_to_expected.append(game_stats_d[stat].actual_reward / game_stats_d[stat].expected_reward)
 	plt.title(stat + " Defender, Rational Attacker")
 	draw.draw_simulation_histogram(game_stats_d[stat])
 	plt.gca().get_legend().remove()
 	draw.show()
 	dr.clear()
actual_to_expected_negated = [ -x for x in actual_to_expected]
x_pos = [i for i, _ in enumerate(titles)]
plt.bar(x_pos, actual_to_expected_negated)
#plt.gca().set_ylim([0.7,1.45])
plt.title("Various Defender vs. Rational Attacker")
plt.xlabel("Defender Strategy")
plt.ylabel("Actual to Expected")
plt.xticks(x_pos, titles)
plt.savefig(dr.Draw.get_next_file_name(), transparent=True, bbox_inches='tight', pad_inches=0.1)
dr.clear()