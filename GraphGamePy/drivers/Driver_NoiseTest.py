#This code tests varying degrees of noise using the noisy strategy

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

random_network_games = []
def add_network_game(network_game):
	random_network_games.append(network_game)
	draw = dr.Draw(network_game)
	#draw.draw_rules()
	draw.draw_nodes_and_edges()
	draw.draw_labels()
	draw.show()
	dr.clear()

NUMBER_OF_SIMULATIONS = 1000#10000

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

random_network_games_solutions = []
for i in range(0, len(random_network_games)):
	random_network_games_solutions.append(solve.NetworkGameSolution(ran.randrange(15,25), random_network_games[i]))
	print("solved " + str(i))

actual_to_expected_attacker_blocky = []
simulator = sim.Simulator()
for noise in np.arange(0, 1.05, 0.05):
	stat = sim.Simulator.GameStats.get_zero_stat(1)
	for sol in random_network_games_solutions:
		stat += simulator.simulate(number_of_simulations=NUMBER_OF_SIMULATIONS, network_game_solution=sol, total_moves=sol.total_moves, attacker_strategy=sim.StrategyType.noisy_rational, noise_level=noise, noise_blocky=True, defender_strategy=sim.StrategyType.rational)
		print("did sim game " + str(sol.total_moves) + " moves on noise " + str(noise))
	stat /= len(random_network_games)
	actual_to_expected_attacker_blocky.append(stat.actual_reward / stat.expected_reward)
print("attacker blocky")
print(actual_to_expected_attacker_blocky)

actual_to_expected_attacker_nonblocky = []
simulator = sim.Simulator()
for noise in np.arange(0, 1.05, 0.05):
	stat = sim.Simulator.GameStats.get_zero_stat(1)
	for sol in random_network_games_solutions:
		stat += simulator.simulate(number_of_simulations=NUMBER_OF_SIMULATIONS, network_game_solution=sol, total_moves=sol.total_moves, attacker_strategy=sim.StrategyType.noisy_rational, noise_level=noise, noise_blocky=False, defender_strategy=sim.StrategyType.rational)
		print("did sim game " + str(sol.total_moves) + " moves on noise " + str(noise))
	stat /= len(random_network_games)
	actual_to_expected_attacker_nonblocky.append(stat.actual_reward / stat.expected_reward)
print("attacker nonblocky")
print(actual_to_expected_attacker_nonblocky)

actual_to_expected_defender_blocky = []
simulator = sim.Simulator()
for noise in np.arange(0, 1.05, 0.05):
	stat = sim.Simulator.GameStats.get_zero_stat(1)
	for sol in random_network_games_solutions:
		stat += simulator.simulate(number_of_simulations=NUMBER_OF_SIMULATIONS, network_game_solution=sol, total_moves=sol.total_moves, attacker_strategy=sim.StrategyType.rational, noise_level=noise, noise_blocky=True, defender_strategy=sim.StrategyType.noisy_rational)
		print("did sim game " + str(sol.total_moves) + " moves on noise " + str(noise))
	stat /= len(random_network_games)
	actual_to_expected_defender_blocky.append(stat.actual_reward / stat.expected_reward)
print("defender blocky")
print(actual_to_expected_defender_blocky)

actual_to_expected_defender_nonblocky = []
simulator = sim.Simulator()
for noise in np.arange(0, 1.05, 0.05):
	stat = sim.Simulator.GameStats.get_zero_stat(1)
	for sol in random_network_games_solutions:
		stat += simulator.simulate(number_of_simulations=NUMBER_OF_SIMULATIONS, network_game_solution=sol, total_moves=sol.total_moves, attacker_strategy=sim.StrategyType.rational, noise_level=noise, noise_blocky=False, defender_strategy=sim.StrategyType.noisy_rational)
		print("did sim game " + str(sol.total_moves) + " moves on noise " + str(noise))
	stat /= len(random_network_games)
	actual_to_expected_defender_nonblocky.append(stat.actual_reward / stat.expected_reward)
print("defender nonblocky")
print(actual_to_expected_defender_nonblocky)

print("attacker blocky")
print(actual_to_expected_attacker_blocky)
print("attacker nonblocky")
print(actual_to_expected_attacker_nonblocky)
print("defender blocky")
print(actual_to_expected_defender_blocky)
print("defender nonblocky")
print(actual_to_expected_defender_nonblocky)