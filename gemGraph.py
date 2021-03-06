import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import vertexGraph
from matplotlib.colors import LinearSegmentedColormap

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Object gem graph
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
class GemGraph:
	'''
	Defined by D_n = {(x,y) in Z^2 : |x|+|y| \leq a*n, |y| \leq n}
	'''
	def __init__(self, n, a, compare=False):
		if a < 0:
			a = -a
		self.a = n
		self.n = n
		if not compare:
			#keep track of nodes for adding layers horizontally
			self.highest_right = (0, n)
			#Height n, width n
			vg = vertexGraph.VertexGraph(n - 1)
			self.G, self.mapping = vg.graph()
			while self.a < a*n:
				self.add_horizontal_layer()
				self.a += 1
			self.a = a
		else:
			vals = [x for x in range(-a*n, a*n + 1)]
			self.mapping = dict()
			nodes = [(x, y) for x in vals for y in vals if (abs(x) + abs(y) <= a*n and abs(y) <= n)]
			hs = set(nodes)
			self.G = nx.Graph()
			self.G.add_nodes_from(nodes)
			for node in nodes:	
				self.mapping[node] = node	
				(x, y) = node	
				if (x - 1, y) in hs:	
					self.G.add_edge((x, y), (x - 1, y))	
				if (x, y - 1) in hs:	
					self.G.add_edge((x, y), (x, y - 1))



	'''
	Adds a layer to 
	'''
	def add_horizontal_layer(self):
		x, y = self.highest_right
		x += 1
		self.highest_right = (x, y)
		self.mapping[self.highest_right] = self.highest_right
		for i in range(self.n):
			#top right
			self.mapping[(x, y)] = (x, y)
			self.G.add_node((x, y))
			self.G.add_edge((x, y), (x - 1, y))
			self.G.add_edge((x, y), (x, y - 1))
			#top left
			self.mapping[(-x, y)] = (-x, y)
			self.G.add_node((-x, y))
			self.G.add_edge((-x, y), (-x + 1, y))
			self.G.add_edge((-x, y), (-x, y - 1))
			#bottom right
			self.mapping[(x, -y)] = (x, -y)
			self.G.add_node((x, -y))
			self.G.add_edge((x, -y), (x - 1, -y))
			self.G.add_edge((x, -y), (x, -y + 1))
			#bottom left
			self.mapping[(-x, -y)] = (-x, -y)
			self.G.add_node((-x, -y))
			self.G.add_edge((-x, -y), (-x + 1, -y))
			self.G.add_edge((-x, -y), (-x, -y + 1))

			x += 1
			y -= 1

		#right-most node
		self.mapping[(x, y)] = (x, y)
		self.G.add_node((x, y))
		self.G.add_edge((x, y), (x - 1, y))
		#left-most node
		self.mapping[(-x, y)] = (-x, y)
		self.G.add_node((-x, y))
		self.G.add_edge((-x, y), (-x + 1, y))

	'''
	Adds a layer by growing n by one
	'''
	def add_layer(self):
		x, y = self.highest_right
		self.highest_right = (x - 1, y + 1)
		#add the top layer
		for i in range(-x + 1, x):
			self.mapping[(i, y + 1)] = (i, y + 1)
			self.mapping[(i, -y - 1)] = (i, -y - 1)
			self.G.add_node((i, y + 1))
			self.G.add_node((i, -y - 1))

			self.G.add_edge((i, y), (i, y + 1))
			self.G.add_edge((i, -y), (i, -y - 1))

		for i in range (-x + 1, x - 1):
			self.G.add_edge((i, y + 1), (i + 1, y + 1))
			self.G.add_edge((i, -y - 1), (i + 1, -y - 1))

		self.n+=1

		for i in range(self.a):
			self.add_horizontal_layer()




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
		return self.height_wrap(matching, X, Y, Z, self.n, 0, self.n * self.a, 0, 0)
	
	'''
	Wrapper function for finding the height function of our Aztec diamond via layers
	'''
	def height_wrap(self, matching, X, Y, Z, n, h, curX, curY, count):
		if(n == 0):
			X[count] = curX
			Y[count] = curY
			Z[count] = h
			count += 1
			initX = curX
				#take advantage of symmetry, at innermost layer (flat line)
			while curX != -initX:
				curX -= 1
				#current square is black
				h = h - 3 if ((curX, curY), (curX + 1, curY)) in matching or ((curX + 1, curY), (curX, curY)) in matching else h + 1
				X[count] = curX
				Y[count] = curY
				Z[count] = h
				count += 1
				curX += -1
				h = h + 3 if ((curX, curY), (curX + 1, curY)) in matching or ((curX + 1, curY), (curX, curY)) in matching else h - 1
				X[count] = curX
				Y[count] = curY
				Z[count] = h
				count += 1
			return X, Y, Z

		X, Y, Z, h, curX, curY, count = self.traverse(matching, X, Y, Z, n, h, curX, curY, count, -1, 1)
		return self.height_wrap(matching, X, Y, Z, n - 1, h, curX, 0, count)

	'''
	Helper function to traverse each layer of the Aztec diamond
	The function calls itself to travel each side of the diamond
	'''
	def traverse(self, matching, X, Y, Z, n, h, curX, curY, count, dirX, dirY):
		if(n <= 0):
			return X, Y, Z, h, curX, curY, count
		X[count] = curX
		Y[count] = curY
		Z[count] = h
		count += 1

		if (dirX == -1 and dirY == 1) or (dirX == 1 and dirY == -1):
			#top right and starting by moving left or bottom left moving right
			for i in range(n):
				h = h - 3 if ((curX, curY), (curX + dirX, curY)) in matching or ((curX + dirX, curY), (curX, curY)) in matching else h + 1
				curX += dirX
				X[count] = curX
				Y[count] = curY
				Z[count] = h
				count += 1
				
				h = h - 3 if ((curX, curY), (curX, curY + dirY)) in matching or ((curX, curY + dirY), (curX, curY)) in matching else h + 1
				curY += dirY
				if(i != n - 1):
					X[count] = curX
					Y[count] = curY
					Z[count] = h
					count += 1
				
			if(dirX == -1 and dirY == 1):
				return self.traverse(matching, X, Y, Z, n, h, curX, curY, count, -1, 0)
			else:
				return self.traverse(matching, X, Y, Z, n, h, curX, curY, count, 1, 0)
		elif (dirX == -1 and dirY == -1) or (dirX == 1 and dirY == 1):
			#top left or bottom right side
			for i in range(n):
				h = h + 3 if ((curX, curY), (curX, curY + dirY)) in matching or ((curX, curY + dirY), (curX, curY)) in matching else h - 1
				curY += dirY
				if(i != n - 1):
					X[count] = curX
					Y[count] = curY
					Z[count] = h
					count += 1
				
				h = h + 3 if ((curX, curY), (curX + dirX, curY)) in matching or ((curX + dirX, curY), (curX, curY)) in matching else h - 1
				curX += dirX
				if(i != n - 1):
					X[count] = curX
					Y[count] = curY
					Z[count] = h
					count+= 1
				
			if(dirX == -1 and dirY == -1):
				return self.traverse(matching, X, Y, Z, n, h, curX, curY, count, 1, -1)
			else:
				#sixth side, finish
				curX -= 1 #(at (n, 0))
				h = h - 3 if ((curX, curY), (curX + dirX, curY)) in matching or ((curX + dirX, curY), (curX, curY)) in matching else h + 1
				#this assumes a > 1
				curX -= 1 #(at (n - 1, 0))
				h = h + 3 if ((curX, curY), (curX + dirX, curY)) in matching or ((curX + dirX, curY), (curX, curY)) in matching else h - 1
			
				return X, Y, Z, h, curX, curY, count
		else:
			#flat edges
			if(dirX != 0 and dirY == 0):
				#always starts at black square
				initX = curX
				#take advantage of symmetry
				while curX != -initX:
					curX += dirX
					#current square is black
					h = h - 3 if ((curX, curY), (curX - dirX, curY)) in matching or ((curX - dirX, curY), (curX, curY)) in matching else h + 1
					X[count] = curX
					Y[count] = curY
					Z[count] = h
					count += 1
					curX += dirX
					h = h + 3 if ((curX, curY), (curX - dirX, curY)) in matching or ((curX - dirX, curY), (curX, curY)) in matching else h - 1
					X[count] = curX
					Y[count] = curY
					Z[count] = h
					count += 1
				#sets up position for next traversal
				count -= 1
				if dirX < 0:
					return self.traverse(matching, X, Y, Z, n, h, curX, curY, count, -1, -1)
				else:
					return self.traverse(matching, X, Y, Z, n, h, curX, curY, count, 1, 1)
			else:
				print("Failed")
				return



	'''
	Gets the midpoints of every edge and returns the list of points
	Returns a list in tuple for by default. Set tuple=False for two
	corresponding lists
	'''
	def get_midpoints(self, tup=True):
		edges = self.G.edges()
		i = 0
		if tup:
			midpoints = np.zeros(len(edges), dtype=('f8, f8'))
			for edge in edges:
				(x1, y1), (x2, y2) = edge
				midpoints[i][0] = (x1 + x2)/2
				midpoints[i][1] = (y1 + y2)/2
				i+=1
			return midpoints
		else:
			X = np.zeros(len(edges))
			Y = np.zeros(len(edges))
			for edge in edges:
				(x1, y1), (x2, y2) = edge
				X[i] = (x1 + x2)/2
				Y[i] = (y1 + y2)/2
				i+=1
			return X, Y


	'''
	Plots the figure and displays it
	Ignore imbalanced checkboard for now
	'''
	def draw(self, avoid_edges = set()):
		fig = plt.figure()
		ax = fig.gca()
		ax.grid(False)
		plt.axis([-self.n, self.n, -self.n, self.n])
		
		# Draws the checkerboard pattern
		k = self.n+1
		nrows, ncols = 2*k, 2*k
		image = np.zeros((nrows,ncols))
		
		if len(avoid_edges)==0:
			nx.draw_networkx(self.G, pos=self.mapping, ax = ax, with_labels = False, node_size = 2, width=.5)
			for i in range(1,k):
				for j in range(k-i,k+i,2):
					image[i,j] = 1					# i in up y-axis, j in right x-axis
					image[nrows-1-i,ncols-1-j] = 1	# make sure nw and se boundaries are white/0
		else:
			for u,v in avoid_edges:
				imin = int(min(u[0],v[0]))+k
				jmin = int(min(u[1],v[1]))+k
				increment = .25*((imin+jmin+k)%2)
				if u[0]==v[0]:
					image[jmin  ,imin-1] = .25 + increment
					image[jmin  ,imin  ] = .25 + increment
				else:
					image[jmin-1,imin  ] = .75 + increment
					image[jmin  ,imin  ] = .75 + increment
		
		colors = [(1,1,1),(1, 0, 0), (0, 0, 1), (0, 1, 0), (0,0,0)]	#W->R->B->G->K
		my_cmap = LinearSegmentedColormap.from_list('my_list', colors, N=5)
		plt.matshow(image,0, cmap=my_cmap, origin = 'lower', extent=(-k,k,-k,k))
		plt.axis('equal')
		plt.show()

#G = VertexGraph(10)
#G.draw()
