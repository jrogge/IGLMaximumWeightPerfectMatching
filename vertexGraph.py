import networkx as nx
import matplotlib.pyplot as plt

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Object for Aztec diamond vertex graph
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
class VertexGraph:
	def __init__(self, n):
		#starting at -1 is the graph with only (0,0)
		self.n = -1
		self.G = nx.Graph()
		self.mapping = dict()
		self.G.add_node((0,0))
		self.mapping[(0,0)] = (0,0)
		
		for i in range (-1, n):
			self.add_layer()
	'''
	Adds a layer to our diamond and increments count
	'''
	def add_layer(self):
		self.n += 1
		#add the points on the x and y axis
		self.G.add_nodes_from([(-self.n - 1, 0), (self.n + 1, 0), (0, -self.n - 1), (0, self.n + 1)])
		self.G.add_edge((-self.n - 1, 0), (-self.n, 0))
		self.G.add_edge((self.n + 1, 0), (self.n, 0))
		self.G.add_edge((0, -self.n - 1), (0, -self.n))
		self.G.add_edge((0, self.n + 1), (0, self.n))
		self.mapping[(-self.n - 1, 0)] = (-self.n - 1, 0)
		self.mapping[(self.n + 1, 0)] = (self.n + 1, 0)
		self.mapping[(0, -self.n - 1)] = (0, -self.n - 1)
		self.mapping[(0, self.n + 1)] = (0, self.n + 1)

		#adds the remaining vertices of the layer; can paralleize this
		for i in range (1, self.n + 1):
			self.G.add_nodes_from([(i, self.n - i + 1), (-i, self.n - i + 1), (i, -self.n + i - 1), (-i, -self.n + i - 1)])
			self.mapping[(i, self.n - i + 1)] = (i, self.n - i + 1)
			self.mapping[(-i, self.n - i + 1)] = (-i, self.n - i + 1)
			self.mapping[(i, -self.n + i - 1)] = (i, -self.n + i - 1)
			self.mapping[(-i, -self.n + i - 1)] = (-i, -self.n + i - 1)
			#top right edges
			self.G.add_edge((i, self.n - i), (i, self.n - i + 1))
			self.G.add_edge((i - 1, self.n - i + 1), (i, self.n - i + 1))
			#top left edges
			self.G.add_edge((-i, self.n - i + 1), (-i, self.n - i))
			self.G.add_edge((-i, self.n - i + 1), (-i + 1, self.n - i + 1))
			#bottom right edges
			self.G.add_edge((i, -self.n + i - 1), (i - 1, -self.n + i - 1))
			self.G.add_edge((i, -self.n + i - 1), (i, -self.n + i))
			#bottom left edges
			self.G.add_edge((-i, -self.n + i - 1), (-i + 1, -self.n + i - 1))
			self.G.add_edge((-i, -self.n + i - 1), (-i, -self.n + i))


	'''
	Given an edge, removes the two associated edges
	'''
	def remove_edge(self, e):
		u, v = e
		self.G.remove_edge(u, v)

	'''
	Plots the figure and displays it
	'''
	def draw(self):
		fig = plt.figure()
		ax = fig.gca()
		ax.grid(True)
		nx.draw_networkx(self.G, pos=self.mapping, ax = ax, with_labels = False, node_size = 20)
		plt.show()

#G = VertexGraph(10)
#G.draw()
