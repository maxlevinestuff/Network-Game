#Times the runtime of varying numbers of nodes/connectedness

import numpy as np

import Simulator as sim
import Solver as solve
import Draw as dr
import NetworkGame as net
import Rules as rules
import JSONExport as jse
import time
import matplotlib.pyplot as plt

nodes_range = range(5, 40, 5)
nodes_avg = 10

connectedness_range = [0.15, 0.20, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
connectedness_avg = 0.07

moves_avg = 10

node_times = []
for i in nodes_range:
	network_game = net.NetworkGame.create_random_network_game(number_of_nodes=i, connectedness=connectedness_avg, caught_policy=rules.Options.caught_policy_continue, number_of_end_nodes=0)
	start = time.process_time()
	network_game_solution = solve.NetworkGameSolution(moves_avg, network_game)
	simulator = sim.Simulator()
	simulator.simulate(10000, network_game_solution, moves_avg)
	node_times.append(time.process_time() - start)
	print("progress node " + str(i))
print("done nodes")
print("nodes")
print(node_times)

connectedness_times = []
for i in connectedness_range:
	network_game = net.NetworkGame.create_random_network_game(number_of_nodes=nodes_avg, connectedness=i, caught_policy=rules.Options.caught_policy_continue, number_of_end_nodes=0)
	start = time.process_time()
	network_game_solution = solve.NetworkGameSolution(moves_avg, network_game)
	simulator = sim.Simulator()
	simulator.simulate(10000, network_game_solution, moves_avg)
	connectedness_times.append(time.process_time() - start)
	print("progress connect " + str(i))
print("done connected")
print("connectedness")
print(connectedness_times)

print()
print("nodes")
print(node_times)
print("connectedness")
print(connectedness_times)