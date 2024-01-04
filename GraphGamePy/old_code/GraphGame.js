//old draft of the js playable game

class Node {
	constructor() {

	}
}

class Graph {
	constructor(size) {
		// Create one dimensional array 
		this.edges = new Array(size); 
  
		// Loop to create 2D array using 1D array 
		for (var i = 0; i < this.edges.length; i++) { 
    		this.edges[i] = []; 
		} 
		var h = 0; 
		var s = "1111111111111000111000001101000011001100100011111000011010000001"; 
  
		// Loop to initilize 2D array elements. 
		for (var i = 0; i < size; i++) { 
    		for (var j = 0; j < size; j++) { 
  
        		this.edges[i][j] = s[h++]; 
    		} 
		}
	}

	getAllAdjacent(node) {
		var adjacentNodes = [];
		for (var i = 0; i < this.edges.length; i++) {
			if (this.edges[node][i] == "1")
				adjacentNodes.push(i);
		}
		return adjacentNodes;
	}
}

var playerOnNode = 1;

var myGraph = new Graph(8);

while (true) {
	var answer = prompt("Which node to move to? " + myGraph.getAllAdjacent(playerOnNode));
	
}

prompt(myGraph.getAllAdjacent(1));