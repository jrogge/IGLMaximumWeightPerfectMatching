import networkx as nx
import matplotlib.pyplot as plt

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Utility file to generate an Aztec Diamond in the form of a NetworkX graph
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


'''
Generates the coordinates of the vertex graph for the Aztec diamond
This is used as a helper function
n - The nth Aztec diamond in the sequence of Aztec diamonds
'''
def generate_grid_coord(n):
	#lazy way of doing this for now
	xvals = [x for x in range(-(n + 1), n + 2)]
	return [(x, y) for x in xvals for y in xvals if abs(x) + abs(y) <= n + 1]

'''
Creates the Aztec diamond graph
n - The nth Aztec diamond in the sequence of Aztec diamonds
Returns a graph as a NetworkX graph object and position mapping for plotting
'''
def create_vertex_graph(n):
	G = nx.Graph()
	nodes = generate_grid_coord(n)
	mapping = dict()
	hs = set(nodes)
	G.add_nodes_from(nodes)

	for node in nodes:
		mapping[node] = node
		(x, y) = node
		if (x - 1, y) in hs:
			G.add_edge((x, y), (x - 1, y))
		if (x, y - 1) in hs:
			G.add_edge((x, y), (x, y - 1))
	return G, mapping

'''
Generates and draws the Aztec diamond
Change n to generate diamonds of different sizes
'''
def draw_aztec_diamond(n):
	G, mapping = create_vertex_graph(n)
	fig = plt.figure()
	ax = fig.gca()
	ax.grid(True)
	nx.draw_networkx(G, pos=mapping, ax = ax, with_labels = False, node_size = 20)
	plt.show()

draw_aztec_diamond(10)
