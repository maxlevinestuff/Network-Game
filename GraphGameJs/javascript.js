//global variables
var game, nodes, edges, container, data, options, network, currentNode, currentMove, userIs, attackerScore, gameOver, defendedNode, attackedNode

//load sounds
var soundWin = new Audio('sounds/win.wav');
var soundLose = new Audio('sounds/lose.wav');
var soundEnd = new Audio('sounds/end.wav');

//checks whether a node is adjacent to another node
function isAdjacent(node1, node2) {
    return JSON.parse(game["adjacency_matrix"])[node1 + node2 * game["number_of_nodes"]] == 1
}

//gets all nodes adjacent to a given node
function getNeighbors(node) {
	var neighbors = []
	for (var i = 0; i < game["number_of_nodes"]; i++) {
		if (isAdjacent(i, node)) {
			neighbors.push(i)
		}
	}
	return neighbors
}

//gets immediate reward from the node
function getImmediateRewardsRevised(node) {
	return JSON.parse(game["immediate_rewards_revised"])[node]
}

//gets caught cost from the node
function getCaughtCost(node) {
	if (game["caught_reward_policy"] == "caught_negate_from_reward")
		return -getImmediateRewardsRevised(node)
	if (Array.isArray(JSON.parse(game["caught_cost"])))
		return -(JSON.parse(game["caught_cost"]))[node]
	else
		return -JSON.parse(game["caught_cost"])
}

//gets the mixed strategy for either player at any state
function getMixedStrategy(node, movesLeft, forAttacker) {
	var searchString = "node" + node.toString() + ",move" + (movesLeft-1).toString() + ":"
	if (forAttacker)
		searchString = searchString + "attacker_mixed_strategy"
	else
		searchString = searchString + "defender_mixed_strategy"
	return JSON.parse(game[searchString])
}
//get the utility for either player at any state
function getUtility(node, movesLeft, forAttacker) {
	var searchString = "node" + node.toString() + ",move" + (movesLeft-1).toString() + ":attacker_utility"
	var attackerUtility = JSON.parse(game[searchString])
	if (forAttacker) {return attackerUtility} else {return -attackerUtility}
}

//set the node labels. called every turn since the labels the attacker is adjacent to change
function setNodeLabels() {
	if (userIs == "attacker") {
		var multiplier = 1
		var specificLabel = "Caught"
	} else {
		var multiplier = -1
		var specificLabel = "Attack"
	}
	for (var id = 0; id < game["number_of_nodes"]; id++) {
		var label = "Node " + id
		label = label + "\nReward: " + (multiplier*getImmediateRewardsRevised(id)).toString()
		if (! (game["end_nodes"].includes(id) && !(game["can_be_caught_on_end_node"]=="True")))
			var label = label + "\nIf caught:  " + (multiplier*getCaughtCost(id)).toString()
		nodes.update({id: id, labelA: label})
	}
	if (!gameOver) {
		var currentNodeNeighbors = getNeighbors(currentNode)
		var currentMixedStrategy = getMixedStrategy(currentNode, currentMove, userIs != "attacker")
		for (var n = 0; n < currentNodeNeighbors.length; n++) {
			var oldLabel = nodes.get(currentNodeNeighbors[n]).labelA
			var newLabel = oldLabel + "\n" + specificLabel + " chance: " + (Math.round(currentMixedStrategy[n] * 1000) / 1000)
			if (! (game["end_nodes"].includes(currentNodeNeighbors[n]) && !(game["can_be_caught_on_end_node"]=="True")))
				;
			else {
				if (userIs == "attacker")
					var newLabel = newLabel + "\nCan't be caught"
				else
					var newLabel = newLabel + "\nCan't defend"
			}
			nodes.update({id: currentNodeNeighbors[n], labelA: newLabel})
		}
	}
}

//loads a game from game data (the game num'th one) and sets everything up
function loadGame(gameNum) {

	game = JSON.parse(gameData[gameNum])
	//randomly choose who player is
	if (Math.round(Math.random()) == 0)
		userIs = "attacker"
	else
		userIs = "defender"

	//initial values
	currentMove = parseInt(game["total_moves"])
	currentNode = parseInt(game["start_node"])
	attackerScore = 0
	gameOver = false
	defendedNode = -1
	attackedNode = -1

	//add all the nodes
	nodes = new vis.DataSet()
	for (var i = 0; i < game["number_of_nodes"]; i++) {
		var shape = 'dot'
		if (game["end_nodes"].includes(i))
			shape = 'hexagon'
		if (game["start_node"] == i)
			shape = 'triangle'
    	nodes.add({id: i, shapeA: shape, shape: 'dot'})
	}

	//set the node labels
	setNodeLabels()

	//add the edges
	edges = new vis.DataSet()
	for (var i = 0; i < game["number_of_nodes"]; i++) {
    	for (var j = 0; j < game["number_of_nodes"]; j++) {
        	if (isAdjacent(i, j)) {
            	edges.add({from: i, to: j, transition: false})
        	}
    	}
	}
	//add the transition edges (rare)
	for (var i = 0; i < (JSON.parse(game["branch_start_nodes"])).length; i++) {
		for (var j = 0; j < ((JSON.parse(game["destination_nodes"])[i])).length; j++) {
			edges.add({to: (JSON.parse(game["branch_start_nodes"]))[i], from: ((JSON.parse(game["destination_nodes"])[i][j])),
				transition: true, label: "<b>" + (JSON.parse(game["destination_nodes_chances"])[i][j]).toString() + "</b>",
				dashes: true, width: 2})
		}
	}

	// create a network
	container = document.getElementById('mynetwork')

	// put the nodes and edges in the vis format
	data = {
    	nodes: nodes,
    	edges: edges
	}

	//set up all the options to be fed to vis
	options = {
		interaction: {
			dragNodes: false
		},
		nodes: {
			borderWidth: 2,
			borderWidthSelected: 0.5,
			size: 15,
			color: {
				background: '#808080',
  				border: '#A9A9A9',
  				highlight: {
  					border: '#ff615d',
  					background: 'red'
  				}
			}
		},
		edges: {
			    font: {
			      color: 'black',
			      size: 15, // px
			      face: 'bold sans-serif',
			      background: 'none',
			      strokeWidth: 3, // px
			      strokeColor: '#bec3e4',
			      align: 'horizontal',
			      multi: true,
			    },
			color: {
  				color: '#808080',
  				highlight: 'red'
			},
			arrows: {
				from: {
					enabled: true
				},
				middle: {
					enabled: true,
					scaleFactor: -1.5
				}
			}
		},
		physics: {
			enabled: true,
			hierarchicalRepulsion: {
				centralGravity: 0.0,
        		springLength: 100,
        		springConstant: 0.001,
        		nodeDistance: 120,
        		damping: 1
			},
			solver: 'hierarchicalRepulsion'
		}
	}

	//initialize the network
	network = new vis.Network(container, data, options)

	//"select" the right things (technically changing the colors, no actual selection)
	setSelect()

	//print out all the relevant game rules to the html
	rules = "<u>Game Rules</u>"
	if (userIs == "attacker")
		rules = rules + "<br>You are playing as the <b>attacker</b>. Try to move about the network and collect rewards without being caught."
	else
		rules = rules + "<br>You are playing as the <b>defender</b>. The attacker is moving around the network. Try to guess where they will go and catch them."
	rules = rules + "<br>The expected rational score for you is <b>" + (Math.round(getUtility(currentNode, currentMove, userIs == "attacker") * 1000) / 1000) + "</b>. See if you can match that score."
	if (game["caught_reward_policy"] == "caught_negate_from_reward") {
		if (userIs == "attacker")
			rules = rules + "<br>If you are caught, you will receive the <b>negation of the reward</b> on the targeted node."
		else
			rules = rules + "<br>If you catch the attacker, you will <b>receive the reward on the targeted node</b>."
	} else if (game["caught_reward_policy"] == "caught_subtract_from_reward") {
		if (userIs == "attacker")
			rules = rules + "<br>If you are caught, you will still receive <b>the reward on the node but with a penalty</b>."
		else
			rules = rules + "<br>If you catch the attacker, you will <b>still lose the points on the targeted node, but will gain back the points for defending</b>."
	} else if (game["caught_reward_policy"] == "caught_subtract_from_0") {
		if (userIs == "attacker")
			rules = rules + "<br>If you are caught, you will <b>lose the set amount of points instead of gaining any</b>."
		else
			rules = rules + "<br>If you catch the attacker, you will <b>gain the set amount of points</b>."
	}
	if (game["caught_policy"] == "caught_policy_continue")
		rules = rules + "<br>If the attacker is caught, they will still receive the penalty but are allowed to <b>continue</b> to the target node."
	else if (game["caught_policy"] == "caught_policy_end_game")
		rules = rules + "<br>If the attacker is <b>caught once, the game ends</b>."
	else if (game["caught_policy"] == "caught_policy_block")
		rules = rules + "<br>If the attacker is caught, they will be <b>blocked</b> and won't move to the target node."
	else if (game["caught_policy"] == "caught_policy_return_to_start")
		rules = rules + "<br>If the attacker is caught, they will move <b>back to start</b>."
	if (game["can_be_caught_on_end_node"]=="True")
		rules = rules + "<br>The attacker <b>can be caught on the end node</b>."
	else
		rules = rules + "<br>The attacker <b>cannot be caught on the end node</b>."
	rules = rules + "<br>The end nodes are hexagons, and the start node is a triangle."
	if ((JSON.parse(game["branch_start_nodes"])).length > 0)
		rules = rules + "<br><b>Transition nodes are present.</b> If the attacker lands one one, they will be randomly brought to a different node along the green, dotted path."
	document.getElementById("rulesoutput").innerHTML = rules
	document.getElementById("moveoutput").innerHTML = "<u>Move 0/" + parseInt(game["total_moves"]) + "</u><br>To begin, click on a node adjacent to the starting node."
}

//on page load, load a random game from GameData.json
loadGame(Math.floor(Math.random() * gameData.length))

//gets the move for whoever the player is not on a given node/turn
function getOpponentNextMove() {
	var strategy = getMixedStrategy(currentNode, currentMove, userIs != "attacker")
	var neighbors = getNeighbors(currentNode)
	//chosen with random
	var random_number = Math.random()
	var threshold = 0
	for (var i = 0; i < strategy.length; i++) {
		threshold = threshold + strategy[i]
		if (random_number < threshold)
			return neighbors[i]
	}
}

//"select" the right things (technically changing the colors, no actual selection)
function setSelect() {

	network.unselectAll()

	//set everything to grey to start
	var allNodes = nodes.getIds()
	for (var i = 0; i < allNodes.length; i++)
		nodes.update({id: allNodes[i], color: {background: '#808080', border: '#A9A9A9'}}) //grey
	var allEdges = edges.getIds()
	for (var i = 0; i < allEdges.length; i++)
		edges.update({id: allEdges[i], color: '#808080'}) //grey

	//set current node red
	nodes.update({id: currentNode, color: {background: 'red', border: '#ff615d'}}) //red
	edges.update({color: '#808080'}) //grey

	//set the attacked, defended, current nodes to their colors
	if (attackedNode != -1) {
		if (attackedNode == defendedNode && (! (game["end_nodes"].includes(attackedNode) && !(game["can_be_caught_on_end_node"]=="True"))))
			nodes.update({id: attackedNode, color: {background: 'purple', border: '#b000af'}}) //purple
		else {
			if (! (game["end_nodes"].includes(defendedNode) && !(game["can_be_caught_on_end_node"]=="True")))
				nodes.update({id: defendedNode, color: {background: 'blue', border: '#3b7e93'}}) //blue
			nodes.update({id: currentNode, color: {background: 'red', border: '#ff615d'}}) //red
		}
	}

	//set all edges adjacent to current to red
	if (!gameOver) {
	    var edgesToSelect = edges.getIds({
	  		filter: function (item) {
	    	return item.to == currentNode;
	  	}});
	  	for (var i = 0; i < edgesToSelect.length; i++)
	  		edges.update({id: edgesToSelect[i], color: 'red'})
  	}

  	//if there are any transition edges, set them to green
  	var edgesToSelect = edges.getIds({
  		filter: function (item) {
    	return item.transition == true;
  	}});
  	for (var i = 0; i < edgesToSelect.length; i++)
  		edges.update({id: edgesToSelect[i], color: 'green'})
}

//click event when a node is clicked
network.on( 'click', function(properties) {
	//only adjacent nodes to current is an actual move
    if (isAdjacent(properties.nodes[0], currentNode) && !gameOver) {

    	//# of moves left
    	var moveText = "<u>Move " + (((parseInt(game["total_moves"]))-(currentMove))+1) + "/" + (parseInt(game["total_moves"])) + "</u>"

    	//get the players' moves
    	if (userIs == "attacker") {
    		attackerMove = properties.nodes[0]
    		defenderMove = getOpponentNextMove()
    	} else {
    		defenderMove = properties.nodes[0]
    		attackerMove = getOpponentNextMove()
    	}
    	defendedNode = defenderMove
    	attackedNode = attackerMove

    	//handle the move location and scores
    	var scoreChange
    	if (attackerMove != defenderMove || (game["end_nodes"].includes(attackerMove) && !(game["can_be_caught_on_end_node"]=="True"))) {
    		if (game["end_nodes"].includes(attackerMove)) {
    			gameOver = true
    			moveText = moveText + "<br>Attacker reached end node."
    		}
    		scoreChange = getImmediateRewardsRevised(attackerMove)
    		attackerScore = attackerScore + scoreChange
    		currentNode = attackerMove
    		moveText = moveText + "<br>Attacker was not caught."
    		if (userIs == "attacker")
    			soundWin.play()
    		else
    			soundLose.play()
    	} else {
    		if (game["caught_reward_policy"] == "caught_negate_from_reward") {
    			scoreChange = -getImmediateRewardsRevised(attackerMove)
    			attackerScore = attackerScore + scoreChange
    		} else if (game["caught_reward_policy"] == "caught_subtract_from_reward") {
    			scoreChange = (getImmediateRewardsRevised(attackerMove) + getCaughtCost(attackerMove))
    			attackerScore = attackerScore + scoreChange
    		} else if (game["caught_reward_policy"] == "caught_subtract_from_0") {
    			scoreChange = getCaughtCost(attackerMove)
    			attackerScore = attackerScore + scoreChange
    		}
    		moveText = moveText + "<br>Attacker was caught."
    		if (userIs == "attacker")
    			soundLose.play()
    		else
    			soundWin.play()

    		if (game["caught_policy"] == "caught_policy_continue") {
    			currentNode = attackerMove
    			moveText = moveText + "<br>The attacker continues to the target node."
    		}
    		else if (game["caught_policy"] == "caught_policy_end_game") {
    			gameOver = true
    			moveText = moveText + "<br>The attacker was caught, which ends the game."
    		} else if (game["caught_policy"] == "caught_policy_block") {
    			moveText = moveText + "<br>The attacker was blocked from moving."
    		} else if (game["caught_policy"] == "caught_policy_return_to_start") {
    			currentNode = game["start_node"]
    			moveText = moveText + "<br>The attacker was sent back to the start."
    		}
    	}

    	//check for game end states
    	if (game["end_nodes"].includes(currentNode))
    		gameOver = true
    	currentMove = currentMove - 1
    	if (currentMove <= 0)
    		gameOver = true
    	currentNode = getTransition(currentNode)
    	if (getNeighbors(currentNode).length == 0)
    		gameOver = true
    	if (gameOver)
    		soundEnd.play()

    	//display the score
    	var scoreChangeDefender = -scoreChange
    	if (scoreChange > 0) {scoreChangeStringAttacker = "+" + scoreChange} else if (scoreChange < 0) {scoreChangeStringAttacker = "" + scoreChange} else {scoreChangeStringAttacker = "+0"}
    	if (scoreChangeDefender > 0) {scoreChangeStringDefender = "+" + scoreChangeDefender} else if (scoreChangeDefender < 0) {scoreChangeStringDefender = "" + scoreChangeDefender} else {scoreChangeStringDefender = "+0"}
    	if (gameOver) {
    		moveText = moveText + "<br>The game is over."
    		if (userIs == "attacker") {
    			moveText = moveText + "<br><b>Your final score: " + attackerScore + "</b>"
    			moveText = moveText + "<br>Defender final score: " + -attackerScore
    		} else {
    			moveText = moveText + "<br><b>Your final score: " + -attackerScore + "</b>"
    			moveText = moveText + "<br>Attacker final score: " + attackerScore
    		}

    	} else {
    		if (userIs == "attacker") {
    			moveText = moveText + "<br><b>Your score: " + (attackerScore - scoreChange) + " (" + scoreChangeStringAttacker + ")</b>"
    			moveText = moveText + "<br>Defender score: " + -(attackerScore - scoreChange) + " (" + scoreChangeStringDefender + ")"
    		} else {
    			moveText = moveText + "<br><b>Your score: " + -(attackerScore - scoreChange) + " (" + scoreChangeStringDefender + ")</b>"
    			moveText = moveText + "<br>Attacker score: " + (attackerScore - scoreChange) + " (" + scoreChangeStringAttacker + ")"
    		}
    	}

    	//set how everything looks
    	document.getElementById("moveoutput").innerHTML = moveText
    	setNodeLabels()
    }
    setSelect()

});

//chooses randomly between the nodes when attacker lands on a transition node
function getTransition(currentNode) {
	if ((JSON.parse(game["branch_start_nodes"])).includes(currentNode)) {
		for (var i = 0; i < (JSON.parse(game["branch_start_nodes"])).length; i++) {
			if ((JSON.parse(game["branch_start_nodes"]))[i] == currentNode) {
				var randomNumber = Math.random()
				var threshold = 0
				for (var j = 0; j < (JSON.parse(game["branch_start_nodes"])).length; j++) {
					threshold = threshold + (JSON.parse(game["destination_nodes_chances"])[i][j])
					if (randomNumber < threshold)
						return (JSON.parse(game["destination_nodes"])[i][j])
				}
			}
		}
	} else
		return currentNode
}

//this function redraws most of what is on the canvas, since the regular options weren't able to do some things
//redraws the nodes and labels.
network.on("afterDrawing", function (ctx)
{
	allNodes = []
	for (var i = 0; i < game["number_of_nodes"]; i++)
		allNodes.push(i)
    var percent = 50
    const r = 30;
    var pos = network.getPositions(allNodes);
    ctx.lineWidth = 3

    for (var i = 0; i < game["number_of_nodes"]; i++) {
    	thisNode = nodes.get(i)
	    var x = pos[i].x
	    var y = pos[i].y
	    ctx.beginPath();
	    if (thisNode.shapeA == 'hexagon')
	    	sides = 6;
	    else if (thisNode.shapeA == 'triangle')
	    	sides = 3
	    else if (thisNode.shapeA == 'dot')
	    	sides = 50
	    const a = (Math.PI * 2) / sides;
	    ctx.moveTo(x , y + r);
	    for (let i = 1; i < sides; i++) {
	        ctx.lineTo(x + r * Math.sin(a * i), y + r * Math.cos(a * i));
	    }
	    ctx.closePath();
	    ctx.save();
	    var textColor = 'black'
	    if (thisNode.color.background == '#808080') {
	    	ctx.fillStyle = '#808080';
	    	ctx.strokeStyle = '#A9A9A9'
	    } else if (thisNode.color.background == 'red') {
	    	ctx.fillStyle = '#ff0000';
	    	ctx.strokeStyle = '#ff615d'
	    } else if (thisNode.color.background == 'blue') {
	    	ctx.fillStyle = '#0000ff';
	    	ctx.strokeStyle = '#3b7e93'
	    	textColor = 'white'
	    } else if (thisNode.color.background == 'purple') {
	    	ctx.fillStyle = '#800080';
	    	ctx.strokeStyle = '#b000af'
	    	textColor = 'white'
	    }
	    ctx.fill(); 
	    ctx.stroke();
	    ctx.restore();

	    ctx.font = "bold 11px sans-serif";
	    ctx.fillStyle = textColor
	    ctx.textAlign = 'center'
	    printAt(ctx, thisNode.labelA, x, y)
	}
});
//draws text on the canvas, for use in the above function
function printAt( c , txt, x, y)
{
	var lineheight = 11;
	var lines = txt.split('\n');
	c.textAlign = 'center'

	for (var i = 0; i<lines.length; i++)
	    c.fillText(lines[i], x, y + (i*lineheight) -lineheight);
}