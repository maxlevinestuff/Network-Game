#very old driver code

#move 0 = 1 move left
adjacency_matrix = np.array([[1,0,0,0,0,0,1,0],[0,1,1,1,1,0,0,0],[0,1,1,0,0,0,0,0],[0,1,0,1,0,0,0,0],
	[0,1,0,0,1,1,0,0],[0,0,0,0,1,1,1,1],[1,0,0,0,0,1,1,0],[0,0,0,0,0,1,0,1]])

immediate_rewards = [12., 3., 55., 2., 1., 107., 0., 3.]

immediate_rewards = [0., 0., 0., 0., 0., 50., 100., 1.]

immediate_rewards = [1., 3., 5., 2., 1., 6., 2., 4.]

network_game_solution = solve.NetworkGameSolution(10, network_game)

simulator = sim.Simulator()
res = simulator.simulate(number_of_simulations=10000, network_game_solution=network_game_solution, starting_node=1, total_moves=10, attacker_strategy=sim.StrategyType.random, defender_strategy=sim.StrategyType.rational)
print(res.actual_reward)
print(res.expected_reward)
print(res.attacker_move_history)
print(res.defender_move_history)

simulator.simulate_200_games(1,15)
print(simulator.simulate_one_game(1,15))

print(network_game_solution.get_solution_no_zero(1,10).utilities[0])
print(network_game_solution.get_solution_average_utility(range(0,8), 10))

draw = draw.Draw(network_game_solution.network_game)
draw.draw_nodes_and_edges()
draw.draw_labels_solution(network_game_solution, 4)
draw.show()
print(network_game_solution.get_neighbors(1))
print(network_game_solution.get_solution(1,5).mixed_strategies)
print(network_game_solution.get_solution(1,5).game)