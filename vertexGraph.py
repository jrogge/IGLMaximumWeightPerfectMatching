import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

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
	Given a matching, defines the height function at every point starting from (n + 1, 0) with the center of the counter-clockwise
	(black) square fixed at (n - 1/2, 1/2)
	The matching comes in as a data structure
	'''
	def height_map(self, matching):
		X = np.zeros(self.G.number_of_nodes())
		Y = np.zeros(self.G.number_of_nodes())
		Z = np.zeros(self.G.number_of_nodes())
		return self.height_wrap(matching, X, Y, Z, self.n, 0, self.n + 1, 0, 0)
	
	def height_wrap(self, matching, X, Y, Z, n, h, curX, curY, count):
		if(curX < 0):
			X[count] = 0
			Y[count] = curY
			Z[count] = h
			print(h)
			return X, Y, Z

		X, Y, Z, h, curX, curY, count = self.traverse(matching, X, Y, Z, n, h, curX, curY, count, -1, 1)
		return self.height_wrap(matching, X, Y, Z, n - 2, h, curX - 1, 0, count)

	'''
	Helper function to traverse each layer of the Aztec diamond
	'''
	def traverse(self, matching, X, Y, Z, n, h, curX, curY, count, dirX, dirY):
		if(n < 0):
			return X, Y, Z, h, curX, curY, count
		X[count] = curX
		Y[count] = curY
		Z[count] = h
		count += 1
		print(curX, curY, h)
		if (dirX == -1 and dirY == 1) or (dirX == 1 and dirY == -1):
			#top right of diamond and starting by moving left
			for i in range(n + 1):
				h = h + 3 if ((curX, curY), (curX + dirX, curY)) in matching or ((curX + dirX, curY), (curX, curY)) in matching else h + 1
				curX += dirX
				if(i != n):
					X[count] = curX
					Y[count] = curY
					Z[count] = h
					count+= 1
				print(curX, curY, h)
				h = h - 3 if ((curX, curY), (curX, curY + dirY)) in matching or ((curX, curY + dirY), (curX, curY)) in matching else h + 1
				curY += dirY
				if(i != n):
					X[count] = curX
					Y[count] = curY
					Z[count] = h
					count += 1
				print(curX, curY, h)
			if(dirX == -1 and dirY == 1):
				return self.traverse(matching, X, Y, Z, n, h, curX, curY, count, -1, -1)
			else:
				return self.traverse(matching, X, Y, Z, n, h, curX, curY, count, 1, 1)
		else:
			for i in range(n + 1):
				h = h + 3 if ((curX, curY), (curX, curY + dirY)) in matching or ((curX, curY + dirY), (curX, curY)) in matching else h - 1
				curY += dirY
				if(i != n):
					X[count] = curX
					Y[count] = curY
					Z[count] = h
					count += 1
				print(curX, curY, h)
				h = h - 3 if ((curX, curY), (curX + dirX, curY)) in matching or ((curX + dirX, curY), (curX, curY)) in matching else h - 1
				curX += dirX
				if(i != n):
					X[count] = curX
					Y[count] = curY
					Z[count] = h
					count+= 1
				print(curX, curY, h)
			if(dirX == -1 and dirY == -1):
				return self.traverse(matching, X, Y, Z, n, h, curX, curY, count, 1, -1)
			else:
				if(n != 0):
					h = h + 3 if ((curX, curY), (curX + dirX, curY)) in matching or ((curX + dirX, curY), (curX, curY)) in matching else h + 1
				curX -= 1 #(at (n, 0))
				h = h + 3 if ((curX, curY), (curX - 1, curY)) in matching or ((curX - 1, curY), (curX, curY)) in matching else h + 1
				return X, Y, Z, h, curX, curY, count


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
