
███╗░░██╗███████╗████████╗░██╗░░░░░░░██╗░█████╗░██████╗░██╗░░██╗  ░██████╗░░█████╗░███╗░░░███╗███████╗
████╗░██║██╔════╝╚══██╔══╝░██║░░██╗░░██║██╔══██╗██╔══██╗██║░██╔╝  ██╔════╝░██╔══██╗████╗░████║██╔════╝
██╔██╗██║█████╗░░░░░██║░░░░╚██╗████╗██╔╝██║░░██║██████╔╝█████═╝░  ██║░░██╗░███████║██╔████╔██║█████╗░░
██║╚████║██╔══╝░░░░░██║░░░░░████╔═████║░██║░░██║██╔══██╗██╔═██╗░  ██║░░╚██╗██╔══██║██║╚██╔╝██║██╔══╝░░
██║░╚███║███████╗░░░██║░░░░░╚██╔╝░╚██╔╝░╚█████╔╝██║░░██║██║░╚██╗  ╚██████╔╝██║░░██║██║░╚═╝░██║███████╗
╚═╝░░╚══╝╚══════╝░░░╚═╝░░░░░░╚═╝░░░╚═╝░░░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝  ░╚═════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚══════╝ README

Please look at Driver_Tutorial.py for an example of how to use everything.
For more details/parameters, you can look at the code of the specific module, which is commented.
If you have any questions, contact Max Levine at mlevine@unca.edu.

Module overview (presented in the order that they are generally called in):

	Rules - describes the game rules
		You'll have to create one of these, along with an adjacency matrix, to create a network game (or randomly generate a network game)
		See Rules.py for a description of each of what each of the options/parameters do
		The way the optional transition chances parameter works is like this:
		e.g.: [1,2],[(2,4),(3,7)],[(0.5,0.5),(0.3,0.7)]
		so if land on node 1, there would be a 50% chance to move to node 2 and 50% to move to node 4, and similar for node 2

	NetworkGame - defines what the game is
		A combination of game rules and an adjacency matrix.
		Also has support for randomly generating a network game

	Solver - solves a NetworkGame, returning a NetworkGameSolution
		Supply it with a NetworkGame and a number of moves to solve for, and it will solve them.
		If you call it later with more moves than originally asked for, it will add them.
		Stores game solutions for every state in its solution_chart, accessible by using get_solution() and get_solution_no_zero()

	Simulator - simulates NetworkGameSolutions and returns results
		The attacker and defender can be set to use different strategies
		Call simulate() with the appropriate parameters, and it will return an averaged GameStats object, which contains the results of the simulation(s).

	Draw - draws visual output of the network games and everything
		Create a draw object, then call its various functions to add the feature to the drawing, then use show() to produce the image; it will be placed in image_output. Use clear() to start a new drawing.

	JSONExport - exports a set of NetworkGameSolutions to JSON for use in the JS game
		Add all of the NetworkGames to the exporter, then call export_to_JSON. It will export GameData.json to json_output. If there is already a GameData.json in json_output, the exported NetworkGameSolutions will be appended. Note: the file is actually a js file that contains a js array containing JSON strings, not actually a JSON file. Then place the GameData.json in the javascript game directory to play.

Todo:
	* make modules for jupyter notebook for running code on server / chameleon
	* create multi dimensional for loop and record ratios between rational: highest_mixed/myopic
	* draw nodes and edges: with nodes bigger depending on total utility
	* Function that returns a list of all possible GameRules with various options
	* simulate and simulate one game have dup code to put in constructor instead
	* to get needed sample size, make a graph comparing expected to actual rational, and find the asymptote
	* Add saving NetworkGameSolutions as pickle or other method