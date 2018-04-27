import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.colors import LinearSegmentedColormap


class thinDiamond:
	'''
	D_n = {(x,y) \in Z^2 : a|x| + b|y| \le ab n}.
	'''
	def __init__(self, a, b, n):
		self.n = -1
		self.a = a
		self.b = b
		self.x = 0
		self.y = 0
		self.G = nx.Graph()
		self.mapping = dict()
		self.G.add_node((0,0))
		self.mapping[(0,0)] = (0,0)
		
		for i in range (-1, n):
			self.add_layer()

	def add_layer(self):
		self.n += 1
		self.x += self.a
		self.y += self.b
		#add the points on the x axis
		for i in range(1,self.a+1):
			self.G.add_nodes_from([(self.x-self.a+i, 0), (-self.x+self.a-i, 0)])
			self.G.add_edge((self.x-self.a+i, 0), (self.x-self.a+i-1, 0))
			self.G.add_edge((-self.x+self.a-i, 0), (-self.x+self.a-i+1, 0))
			self.mapping[(self.x-self.a+i, 0)] = (self.x-self.a+i, 0)
			self.mapping[(-self.x+self.a-i, 0)] = (-self.x+self.a-i, 0)
		#add the points on the y axis
		for i in range(-1,self.b-1):
			self.G.add_nodes_from([(0, self.y-self.b+i), (0, -self.y+self.b-i)])
			self.G.add_edge((0, self.y-self.b+i), (0, self.y-self.b+i-1))
			self.G.add_edge((0, -self.y+self.b-i), (0, -self.y+self.b-i+1))
			self.mapping[(0, self.y-self.b+i)] = (0, self.y-self.b+i)
			self.mapping[(0, -self.y+self.b-i)] = (0, -self.y+self.b-i)
		#adds the remaining vertices of the layer
		for i in range(0, self.x-1):
			for j in range(1, self.b+1):
				self.G.add_nodes_from([(self.x-i-1, i*self.b+j), (self.x-i-1, -i*self.b-j), (-self.x+i+1, i*self.b+j), (-self.x+i+1, -i*self.b-j)])
				self.mapping[(self.x-i-1, i*self.b+j)] = (self.x-i-1, i*self.b+j)
				self.mapping[(self.x-i-1, -i*self.b-j)] = (self.x-i-1, -i*self.b-j)
				self.mapping[(-self.x+i+1, i*self.b+j)] = (-self.x+i+1, i*self.b+j)
				self.mapping[(-self.x+i+1, -i*self.b-j)] = (-self.x+i+1, -i*self.b-j)
				#top right edges
				self.G.add_edge((self.x-i-1, i*self.b+j),(self.x-i-1-1, i*self.b+j))
				self.G.add_edge((self.x-i-1, i*self.b+j),(self.x-i-1, i*self.b+j-1))
				#bottom right edges
				self.G.add_edge((self.x-i-1, -i*self.b-j),(self.x-i-1-1, -i*self.b-j))
				self.G.add_edge((self.x-i-1, -i*self.b-j),(self.x-i-1, -i*self.b-j+1))
				#top left edges
				self.G.add_edge((-self.x+i+1, i*self.b+j),(-self.x+i+1+1, i*self.b+j))
				self.G.add_edge((-self.x+i+1, i*self.b+j),(-self.x+i+1, i*self.b+j-1))
				#bottom left edges
				self.G.add_edge((-self.x+i+1, -i*self.b-j),(-self.x+i+1+1, -i*self.b-j))
				self.G.add_edge((-self.x+i+1, -i*self.b-j),(-self.x+i+1, -i*self.b-j+1))
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
		return self.height_wrap(matching, X, Y, Z, self.n, 0, self.a*self.n + 1, 0, 0)
	'''
	Wrapper function for finding the height function of our Aztec diamond via layers
	'''
	def height_wrap(self, matching, X, Y, Z, n, h, curX, curY, count):
		if(curX <= 0):
			X[count] = 0
			Y[count] = curY
			Z[count] = h
			return X, Y, Z

		X, Y, Z, h, curX, curY, count = self.traverse(matching, X, Y, Z, n, h, curX, curY, count, -1, 1)
		return self.height_wrap(matching, X, Y, Z, n - 2, h, curX, 0, count)

	'''
	Helper function to traverse each layer of the Aztec diamond
	The function calls itself to travel each side of the diamond
	'''
	def traverse(self, matching, X, Y, Z, n, h, curX, curY, count, dirX, dirY):
		if(n < 0):
			return X, Y, Z, h, curX, curY, count
		X[count] = curX
		Y[count] = curY
		Z[count] = h
		count += 1
	
		if (dirX == -1 and dirY == 1) or (dirX == 1 and dirY == -1):
			#top right of diamond and starting by moving left or bottom left of diamond moving right
			for i in range(n + 1):
				h = h - 3 if ((curX, curY), (curX + dirX, curY)) in matching or ((curX + dirX, curY), (curX, curY)) in matching else h + 1
				curX += dirX
				if(i != n):
					X[count] = curX
					Y[count] = curY
					Z[count] = h
					count+= 1
				
				h = h - 3 if ((curX, curY), (curX, curY + dirY)) in matching or ((curX, curY + dirY), (curX, curY)) in matching else h + 1
				curY += dirY
				if(i != n):
					X[count] = curX
					Y[count] = curY
					Z[count] = h
					count += 1
				
			if(dirX == -1 and dirY == 1):
				return self.traverse(matching, X, Y, Z, n, h, curX, curY, count, -1, -1)
			else:
				return self.traverse(matching, X, Y, Z, n, h, curX, curY, count, 1, 1)
		else:
			#top left of diamond moving down or bottom right moving up
			for i in range(n + 1):
				h = h + 3 if ((curX, curY), (curX, curY + dirY)) in matching or ((curX, curY + dirY), (curX, curY)) in matching else h - 1
				curY += dirY
				if(i != n):
					X[count] = curX
					Y[count] = curY
					Z[count] = h
					count += 1
				
				h = h + 3 if ((curX, curY), (curX + dirX, curY)) in matching or ((curX + dirX, curY), (curX, curY)) in matching else h - 1
				curX += dirX
				if(i != n):
					X[count] = curX
					Y[count] = curY
					Z[count] = h
					count+= 1
				
			if(dirX == -1 and dirY == -1):
				return self.traverse(matching, X, Y, Z, n, h, curX, curY, count, 1, -1)
			else:
				#fourth side of diamond, finish
				curX -= 1 #(at (n, 0))
				h = h - 3 if ((curX, curY), (curX + dirX, curY)) in matching or ((curX + dirX, curY), (curX, curY)) in matching else h + 1
	
				if(n != 0):
					curX -= 1 #(at (n - 1, 0))
					h = h + 3 if ((curX, curY), (curX + dirX, curY)) in matching or ((curX + dirX, curY), (curX, curY)) in matching else h - 1
			
				return X, Y, Z, h, curX, curY, count
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

G = thinDiamond(1,3,5)
G.draw()


