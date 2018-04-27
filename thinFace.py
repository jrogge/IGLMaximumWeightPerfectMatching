import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import bipartite
import random

class thinFace:
	def __init__(self, a, b, n, weighted=False, max_weight=10000):
		self.n = 1
		self.a = a
		self.b = b
		self.x = a
		self.y = b
		self.G = nx.Graph()
		self.mapping = dict()
		self.weighted = weighted
		self.max_weight = max_weight
		initial_vertices = []
		for i in range(0, a):
			for j in range(0, b):
				initial_vertices.append((0.5+i, 0.5+j))
				initial_vertices.append((0.5+i, -0.5-j))
				initial_vertices.append((-0.5-i, 0.5+j))
				initial_vertices.append((-0.5-i, -0.5-j))
		if weighted:
			self.G.add_edge((0.5+i, 0.5), (0.5+i, 0.5-1), weight=random.randint(1, self.max_weight + 1))
			self.G.add_edge((0.5+i, 0.5), (0.5+i-1, 0.5), weight=random.randint(1, self.max_weight + 1))
			self.G.add_edge((-0.5-i, -0.5), (-0.5-i+1, -0.5), weight=random.randint(1, self.max_weight + 1))
			self.G.add_edge((-0.5-i, -0.5), (-0.5-i, -0.5+1), weight=random.randint(1, self.max_weight + 1))
			for i in range(1, a):
				self.G.add_edge((0.5+i, 0.5), (0.5+i-1, 0.5), weight=random.randint(1, self.max_weight + 1))
				self.G.add_edge((0.5+i, -0.5), (0.5+i-1, -0.5), weight=random.randint(1, self.max_weight + 1))
				self.G.add_edge((0.5+i, 0.5), (0.5+i, -0.5), weight=random.randint(1, self.max_weight + 1))
				self.G.add_edge((-0.5-i, 0.5), (-0.5-i+1, 0.5), weight=random.randint(1, self.max_weight + 1))
				self.G.add_edge((-0.5-i, -0.5), (-0.5-i+1, -0.5), weight=random.randint(1, self.max_weight + 1))
				self.G.add_edge((-0.5-i, 0.5), (-0.5-i, -0.5), weight=random.randint(1, self.max_weight + 1))
			for j in range(1, b):
				self.G.add_edge((0.5, 0.5+j), (0.5, 0.5+j-1), weight=random.randint(1, self.max_weight + 1))
				self.G.add_edge((-0.5, 0.5+j), (-0.5, 0.5+j-1), weight=random.randint(1, self.max_weight + 1))
				self.G.add_edge((0.5, 0.5+j), (-0.5, 0.5+j), weight=random.randint(1, self.max_weight + 1))
				self.G.add_edge((0.5, -0.5-j), (0.5, -0.5-j+1), weight=random.randint(1, self.max_weight + 1))
				self.G.add_edge((-0.5, -0.5-j), (-0.5, -0.5-j+1), weight=random.randint(1, self.max_weight + 1))
				self.G.add_edge((0.5, -0.5-j), (-0.5, -0.5-j), weight=random.randint(1, self.max_weight + 1))
			if (a != 1 and b !=1):
				self.G.add_edge((0.5,0.5),(0.5,-0.5), weight=random.randint(1, self.max_weight + 1))
				self.G.add_edge((0.5,0.5),(-0.5,0.5), weight=random.randint(1, self.max_weight + 1))
				self.G.add_edge((-0.5,-0.5),(-0.5,0.5), weight=random.randint(1, self.max_weight + 1))
				self.G.add_edge((-0.5,-0.5),(0.5,-0.5), weight=random.randint(1, self.max_weight + 1))
		else:
			self.max_weight = 0
			self.G.add_edge((0.5+i, 0.5), (0.5+i, 0.5-1))
			self.G.add_edge((0.5+i, 0.5), (0.5+i-1, 0.5))
			self.G.add_edge((-0.5-i, -0.5), (-0.5-i+1, -0.5))
			self.G.add_edge((-0.5-i, -0.5), (-0.5-i, -0.5+1))
			for i in range(1, a):
				self.G.add_edge((0.5+i, 0.5), (0.5+i-1, 0.5))
				self.G.add_edge((0.5+i, -0.5), (0.5+i-1, -0.5))
				self.G.add_edge((0.5+i, 0.5), (0.5+i, -0.5))
				self.G.add_edge((-0.5-i, 0.5), (-0.5-i+1, 0.5))
				self.G.add_edge((-0.5-i, -0.5), (-0.5-i+1, -0.5))
				self.G.add_edge((-0.5-i, 0.5), (-0.5-i, -0.5))
			for j in range(1, b):
				self.G.add_edge((0.5, 0.5+j), (0.5, 0.5+j-1))
				self.G.add_edge((-0.5, 0.5+j), (-0.5, 0.5+j-1))
				self.G.add_edge((0.5, 0.5+j), (-0.5, 0.5+j))
				self.G.add_edge((0.5, -0.5-j), (0.5, -0.5-j+1))
				self.G.add_edge((-0.5, -0.5-j), (-0.5, -0.5-j+1))
				self.G.add_edge((0.5, -0.5-j), (-0.5, -0.5-j))
			if (a != 1 and b !=1):
				self.G.add_edge((0.5,0.5),(0.5,-0.5))
				self.G.add_edge((0.5,0.5),(-0.5,0.5))
				self.G.add_edge((-0.5,-0.5),(-0.5,0.5))
				self.G.add_edge((-0.5,-0.5),(0.5,-0.5))
		for vertex in initial_vertices:
			self.mapping[vertex] = vertex
		for i in range (n - 1):
			self.add_layer()


	'''
	Adds a layer to our surface graph
	Can parallelize this eventually
	'''
	def add_layer(self):
		self.x += self.a
		self.y += self.b
		vertices = []
		count = 0
		l = 0
		for i in range(0, self.x):	
			if (count == self.a):
				l += 1
				count = 0
			for j in range(0, self.b):
				self.G.add_nodes_from([(i+0.5,self.y-0.5-j-l*self.b),(i+0.5,-self.y+0.5+j+l*self.b),(-i-0.5,self.y-0.5-j-l*self.b),(-i-0.5,-self.y+0.5+j+l*self.b)])
				self.mapping[(i+0.5,self.y-0.5-j-l*self.b)] = (i+0.5,self.y-0.5-j-l*self.b)
				self.mapping[(i+0.5,-self.y+0.5+j+l*self.b)] = (i+0.5,-self.y+0.5+j+l*self.b)
				self.mapping[(-i-0.5,self.y-0.5-j-l*self.b)] = (-i-0.5,self.y-0.5-j-l*self.b)
				self.mapping[(-i-0.5,-self.y+0.5+j+l*self.b)] = (-i-0.5,-self.y+0.5+j+l*self.b)
				vertices.append([i+0.5,self.y-0.5-j-l*self.b])
				vertices.append([i+0.5,-self.y+0.5+j+l*self.b])
				vertices.append([-i-0.5,self.y-0.5-j-l*self.b])
				vertices.append([-i-0.5,-self.y+0.5+j+l*self.b])
			count += 1
		for v in range(0, len(vertices)):
			#add edges across y-axis
			if(vertices[v][0] == 0.5 or vertices[v][0] == -0.5):
				for j in range(0,self.b):
					self.G.add_edge((0.5,self.y-0.5-j),(-0.5,self.y-0.5-j), weight=random.randint(1, self.max_weight + 1))
					self.G.add_edge((0.5,-self.y+0.5+j),(-0.5,-self.y+0.5+j), weight=random.randint(1, self.max_weight + 1))
					self.G.add_edge((0.5,self.y-0.5-j),(0.5,self.y-0.5-j-1), weight=random.randint(1, self.max_weight + 1))
					self.G.add_edge((-0.5,self.y-0.5-j),(-0.5,self.y-0.5-j-1), weight=random.randint(1, self.max_weight + 1))
					self.G.add_edge((0.5,-self.y+0.5+j),(0.5,-self.y+0.5+j+1), weight=random.randint(1, self.max_weight + 1))
					self.G.add_edge((-0.5,-self.y+0.5+j),(-0.5,-self.y+0.5+j+1), weight=random.randint(1, self.max_weight + 1))
			#add edges across x-axis
			elif(vertices[v][1] == 0.5 or vertices[v][1] == -0.5):		
				for i in range(0,self.a):
					self.G.add_edge((self.x-0.5-i,0.5),(self.x-0.5-i,-0.5), weight=random.randint(1, self.max_weight + 1))
					self.G.add_edge((-self.x+0.5+i,0.5),(-self.x+0.5+i,-0.5), weight=random.randint(1, self.max_weight + 1))
					self.G.add_edge((self.x-0.5-i,0.5),(self.x-0.5-i-1,0.5), weight=random.randint(1, self.max_weight + 1))
					self.G.add_edge((self.x-0.5-i,-0.5),(self.x-0.5-i-1,-0.5), weight=random.randint(1, self.max_weight + 1))
					self.G.add_edge((-self.x+0.5+i,0.5),(-self.x+0.5+i+1,0.5), weight=random.randint(1, self.max_weight + 1))
					self.G.add_edge((-self.x+0.5+i,-0.5),(-self.x+0.5+i+1,-0.5), weight=random.randint(1, self.max_weight + 1))
			else:
				#top right
				if(vertices[v][0]>0 and vertices[v][1]>0):
					self.G.add_edge((vertices[v][0],vertices[v][1]),(vertices[v][0]-1,vertices[v][1]), weight=random.randint(1, self.max_weight + 1))
					self.G.add_edge((vertices[v][0],vertices[v][1]),(vertices[v][0],vertices[v][1]-1), weight=random.randint(1, self.max_weight + 1))
				#top left
				if(vertices[v][0]<0 and vertices[v][1]>0):
					self.G.add_edge((vertices[v][0],vertices[v][1]),(vertices[v][0]+1,vertices[v][1]), weight=random.randint(1, self.max_weight + 1))
					self.G.add_edge((vertices[v][0],vertices[v][1]),(vertices[v][0],vertices[v][1]-1), weight=random.randint(1, self.max_weight + 1))
				#bottom right
				if(vertices[v][0]>0 and vertices[v][1]<0):
					self.G.add_edge((vertices[v][0],vertices[v][1]),(vertices[v][0]-1,vertices[v][1]), weight=random.randint(1, self.max_weight + 1))
					self.G.add_edge((vertices[v][0],vertices[v][1]),(vertices[v][0],vertices[v][1]+1), weight=random.randint(1, self.max_weight + 1))
				#bottom left
				if(vertices[v][0]<0 and vertices[v][1]<0):
					self.G.add_edge((vertices[v][0],vertices[v][1]),(vertices[v][0]+1,vertices[v][1]), weight=random.randint(1, self.max_weight + 1))
					self.G.add_edge((vertices[v][0],vertices[v][1]),(vertices[v][0],vertices[v][1]+1), weight=random.randint(1, self.max_weight + 1))
			
	'''
	Finds a perfect matching. We are assuming the graph is unweighted for now.
	maxcardinality is set to true for the needs of this project
	'''
	def perfect_matching(self):
		if self.weighted:
			return nx.max_weight_matching(self.G, maxcardinality = True)
		else:
			return bipartite.hopcroft_karp_matching(self.G)

	'''
	Gets the edges we must avoid in the surface graph.
	Returns a hashset for good query time
	'''
	def get_avoid_edges(self):
		hs = set()
		matching = self.perfect_matching()
		for match in matching.items():
			(x1, y1), (x2, y2) = match if self.weighted else (match, matching[match])
			if(x1 == x2):
				#vertical edge
				bigY = y1 if (y1 >= y2) else y2
				smallY = y1 if (y1 < y2) else y2
				hs.add(((x1 - 0.5, smallY + 0.5), (x2 + 0.5, bigY - 0.5)))
			else:
				#horiztonal edge 
				bigX = x1 if (x1 >= x2) else x2
				smallX = x1 if (x1 < x2) else x2
				hs.add(((smallX + 0.5, y1 - 0.5), (bigX - 0.5, y1 + 0.5)))
		return hs
			
	'''
	Draws the graph
	'''
	def draw(self):
		fig = plt.figure()
		ax = fig.gca()
		ax.grid(False)
		nx.draw_networkx(self.G, pos= self.mapping, ax = ax, with_labels = False, node_size = 10)
		plt.axis('equal')
		plt.show()

G = thinFace(1,3,5)
G.draw()
