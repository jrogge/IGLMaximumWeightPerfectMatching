import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import bipartite
import random


'''''''''''''''''''''''''''''''''''''''
Surface graph for the Aztec diamond
Use to find maximum weighted perfect matching
'''''''''''''''''''''''''''''''''''''''
class GemFaceGraph:
    def __init__(self, n, a, weighted=False, max_weight=10000):
        self.prod = a*n
        self.n = n
        self.graph = nx.Graph()
        self.weighted = weighted
        self.mapping = dict()
        for x in range(-a*n, a*n+1):
            for y in range(-n, n):
                if ((abs(x+0.5) + abs(y+0.5)) < self.prod and abs(y+0.5) < self.n):
                    self.graph.add_node((0.5+x, 0.5+y))
                    self.mapping[(0.5+x, 0.5+y)] = (0.5+x, 0.5+y)
                if ((abs(x-0.5) + abs(y+0.5)) < self.prod and abs(y+0.5) < self.n):
                    self.graph.add_node((0.5-x, 0.5+y))
                    self.mapping[(0.5-x, 0.5+y)] = (0.5-x, 0.5+y)
                if ((abs(x+0.5) + abs(y-0.5)) < self.prod and abs(y-0.5) < self.n):
                    self.graph.add_node((0.5+x, 0.5-y))
                    self.mapping[(0.5+x, 0.5-y)] = (0.5+x, 0.5-y)
                if ((abs(x-0.5) + abs(y-0.5)) < self.prod and abs(y-0.5) < self.n):
                    self.graph.add_node((0.5-x, 0.5-y))
                    self.mapping[(0.5-x, 0.5-y)] = (0.5-x, 0.5-y)

        for x in range(-a*n, a*n+1):
            for y in range(-n, n):
                if ((abs(x+0.5) + abs(y+0.5)) < self.prod and abs(y+0.5) < self.n):
                    self.add_neighbors(0.5+x, 0.5+y)
                if ((abs(x-0.5) + abs(y+0.5)) < self.prod and abs(y+0.5) < self.n):
                    self.add_neighbors(0.5-x, 0.5+y)
                if ((abs(x+0.5) + abs(y-0.5)) < self.prod and abs(y-0.5) < self.n):
                    self.add_neighbors(0.5+x, 0.5-y)
                if ((abs(x-0.5) + abs(y-0.5)) < self.prod and abs(y-0.5) < self.n):
                    self.add_neighbors(0.5-x, 0.5-y)
        #print(self.mapping)



    def add_neighbors(self, x, y):
        if ((abs(x+1) + abs(y)) < self.prod and abs(y) < self.n):
            self.graph.add_edge((x,y), (x+1, y))
            #self.mapping[(x+1, y)] = (x+1, y)
        if ((abs(x-1) + abs(y)) < self.prod and abs(y) < self.n):
            self.graph.add_edge((x,y), (x-1, y))
            #self.mapping[(x-1, y)] = (x-1, y)
        if ((abs(x) + abs(y+1)) < self.prod and abs(y+1) < self.n):
            self.graph.add_edge((x,y), (x, y+1))
            #self.mapping[(x, y+1)] = (x, y+1)
        if ((abs(x) + abs(y-1)) < self.prod and abs(y-1) < self.n):
            self.graph.add_edge((x,y), (x, y-1))
            #self.mapping[(x, y-1)] = (x, y-1)

    '''
    Finds a perfect matching. We are assuming the graph is unweighted for now.
    maxcardinality is set to true for the needs of this project
    '''
    def perfect_matching(self):
        if self.weighted:
            return nx.max_weight_matching(self.graph, maxcardinality = True)
        else:
            return bipartite.hopcroft_karp_matching(self.graph)

    '''
    Gets the edges we must avoid in the surface graph.
    Returns a hashset for good query time
    '''
    def get_avoid_edges(self):
        hs = set()
        matching = self.perfect_matching()
        for match in matching:
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
        
    def draw(self):
        fig = plt.figure()
        ax = fig.gca()
        ax.grid(False)
        nx.draw_networkx(self.graph, pos= self.mapping, ax = ax, with_labels = False, node_size = 10)
        plt.axis('equal')
        plt.show()
