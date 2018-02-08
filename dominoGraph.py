import matplotlib.pyplot as plt
import networkx as nx

'''''''''''''''''''''''''''''''''''''''
Surface graph for the Aztec diamond
Use to find maximum weighted perfect matching
'''''''''''''''''''''''''''''''''''''''
class SurfaceGraph:
	def __init__(self, n):
		self.n = 1
		self.G = nx.Graph()
		self.mapping = dict()
		initial_vertices = [(-0.5, -0.5), (-0.5, 0.5), (0.5, -0.5), (0.5, 0.5)]
		initial_edges = [((-0.5, -0.5), (-0.5, 0.5)), ((-0.5, -0.5),(0.5, -0.5)), ((0.5, -0.5), (0.5, 0.5)), ((-0.5, 0.5), (0.5, 0.5))]
		self.G.add_nodes_from(initial_vertices)
		self.G.add_edges_from(initial_edges)



		for vertex in initial_vertices:
			self.mapping[vertex] = vertex
		for i in range (n - 1):
			self.add_layer()

	'''
	Adds a layer to our surface graph
	Can parallelize this eventually
	'''
	def add_layer(self):
		for i in range(0, self.n):
			top_right = (self.n - (i + 0.5), (i + 0.5))
			top_left = (-(self.n - (i + 0.5)), (i + 0.5))
			bottom_right = (self.n - (i + 0.5), -(i + 0.5))
			botton_left = (-(self.n - (i + 0.5)), -(i + 0.5))

			#top right quadrant
			self.G.add_node((top_right[0], top_right[1] + 1))
			self.G.add_node((top_right[0] + 1, top_right[1]))
			self.G.add_edge(top_right, (top_right[0], top_right[1] + 1))
			self.G.add_edge(top_right, (top_right[0] + 1, top_right[1]))
			self.mapping[(top_right[0], top_right[1] + 1)] = (top_right[0], top_right[1] + 1)
			self.mapping[(top_right[0] + 1, top_right[1])] = (top_right[0] + 1, top_right[1])

			#top left quadrant
			self.G.add_node((top_left[0] - 1, top_left[1]))
			self.G.add_node((top_left[0], top_left[1] + 1))
			self.G.add_edge(top_left, (top_left[0] - 1, top_left[1]))
			self.G.add_edge(top_left, (top_left[0], top_left[1] + 1))
			self.mapping[(top_left[0] - 1, top_left[1])] = (top_left[0] - 1, top_left[1])
			self.mapping[(top_left[0], top_left[1] + 1)] = (top_left[0], top_left[1] + 1)

			#bottom right quadrant
			self.G.add_node((bottom_right[0] + 1, bottom_right[1]))
			self.G.add_node((bottom_right[0], bottom_right[1] - 1))
			self.G.add_edge(bottom_right, (bottom_right[0] + 1, bottom_right[1]))
			self.G.add_edge(bottom_right, (bottom_right[0], bottom_right[1] - 1))
			self.mapping[(bottom_right[0] + 1, bottom_right[1])] = (bottom_right[0] + 1, bottom_right[1])
			self.mapping[(bottom_right[0], bottom_right[1] - 1)] = (bottom_right[0], bottom_right[1] - 1)

			#botton left quadrant
			self.G.add_node((botton_left[0] - 1, botton_left[1]))
			self.G.add_node((botton_left[0], botton_left[1] - 1))
			self.G.add_edge(botton_left, (botton_left[0] - 1, botton_left[1]))
			self.G.add_edge(botton_left, (botton_left[0], botton_left[1] - 1))
			self.mapping[(botton_left[0] - 1, botton_left[1])] = (botton_left[0] - 1, botton_left[1])
			self.mapping[(botton_left[0], botton_left[1] - 1)] = (botton_left[0], botton_left[1] - 1)


		self.n += 1
		#connect middle nodes
		self.G.add_edge((0.5, self.n - 0.5), (-0.5, self.n - 0.5))
		self.G.add_edge((self.n - 0.5, 0.5),((self.n - 0.5), -0.5))
		self.G.add_edge((-self.n + 0.5, 0.5), ((-self.n + 0.5), -0.5))
		self.G.add_edge((0.5, -self.n + 0.5), (-0.5, -self.n + 0.5))



			
	'''
	Draws the graph
	'''
	def draw(self):
		fig = plt.figure()
		ax = fig.gca()
		ax.grid(True)
		nx.draw_networkx(self.G, pos= self.mapping, ax = ax, with_labels = False, node_size = 20)
		plt.show()

G = SurfaceGraph(5)
G.draw()


