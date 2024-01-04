#demonstrates how pyplot cuts off the edges of nodes

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

adjacency_matrix = np.array([[1,0,0,0,0,0,1,0],[0,1,1,1,1,0,0,0],[0,1,1,0,0,0,0,0],[0,1,0,1,0,0,0,0],
    [0,1,0,0,1,1,0,0],[0,0,0,0,1,1,1,1],[1,0,0,0,0,1,1,0],[0,0,0,0,0,1,0,1]])

nx_graph = nx.from_numpy_matrix(adjacency_matrix)
pos = nx.networkx.kamada_kawai_layout(nx_graph)

nx.draw_networkx_nodes(nx_graph, pos, node_color="#000000", node_size=10000)

nx.draw_networkx_edges(nx_graph, pos, color="#808080", alpha=0.2, width=2.0)

plt.axis('off')
axis = plt.gca()
axis.set_xlim([1.5*x for x in axis.get_xlim()])
axis.set_ylim([1.5*y for y in axis.get_ylim()])
plt.tight_layout()
plt.show()