import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import bipartite
import random


'''''''''''''''''''''''''''''''''''''''
Surface graph for the Aztec diamond
Use to find maximum weighted perfect matching
'''''''''''''''''''''''''''''''''''''''
class GemFaceGraph:
        def __init__(self, a, n, weighted=False, max_weight=10000):
            self.prod = a*n
            self.n = n
            self.graph = nx.Graph()
            self.mapping = dict()
            for x in range(-a*n, a*n+1):
                for y in range(-n, n):
                    if ((abs(x+0.5) + abs(y+0.5)) <= self.prod and abs(y+0.5) < self.n):
                        self.graph.add_node((0.5+x, 0.5+y))
                        self.mapping[(0.5+x, 0.5+y)] = (0.5+x, 0.5+y)
                        print("node", 0.5+x, 0.5+y)
                    if ((abs(x-0.5) + abs(y+0.5)) <= self.prod and abs(y+0.5) < self.n):
                        self.graph.add_node((0.5-x, 0.5+y))
                        self.mapping[(0.5-x, 0.5+y)] = (0.5-x, 0.5+y)
                        print("node", 0.5-x, 0.5+y)
                    if ((abs(x+0.5) + abs(y-0.5)) <= self.prod and abs(y-0.5) < self.n):
                        self.graph.add_node((0.5+x, 0.5-y))
                        self.mapping[(0.5+x, 0.5-y)] = (0.5+x, 0.5-y)
                        print("node", 0.5+x, 0.5-y)
                    if ((abs(x-0.5) + abs(y-0.5)) <= self.prod and abs(y-0.5) < self.n):
                        self.graph.add_node((0.5-x, 0.5-y))
                        self.mapping[(0.5-x, 0.5-y)] = (0.5-x, 0.5-y)
                        print("node", 0.5-x, 0.5-y)

            for x in range(-a*n, a*n+1):
                for y in range(-n, n):
                    print(x, y)
                    if ((abs(x+0.5) + abs(y+0.5)) <= self.prod and abs(y+0.5) < self.n):
                        print("adding neighbors for", x+0.5, y+0.5)
                        self.add_neighbors(0.5+x, 0.5+y)
                    if ((abs(x-0.5) + abs(y+0.5)) <= self.prod and abs(y+0.5) < self.n):
                        print("adding neighbors for", x+0.5, y+0.5)
                        self.add_neighbors(0.5-x, 0.5+y)
                    if ((abs(x+0.5) + abs(y-0.5)) <= self.prod and abs(y-0.5) < self.n):
                        print("adding neighbors for", x+0.5, y+0.5)
                        self.add_neighbors(0.5+x, 0.5-y)
                    if ((abs(x-0.5) + abs(y-0.5)) <= self.prod and abs(y-0.5) < self.n):
                        print("adding neighbors for", x+0.5, y+0.5)
                        self.add_neighbors(0.5-x, 0.5-y)
            #print(self.mapping)



        def add_neighbors(self, x, y):
            if ((abs(x+1) + abs(y)) <= self.prod and abs(y) < self.n):
                self.graph.add_edge((x,y), (x+1, y))
                #self.mapping[(x+1, y)] = (x+1, y)
                print("neighbor", x+1, y)
            if ((abs(x-1) + abs(y)) <= self.prod and abs(y) < self.n):
                self.graph.add_edge((x,y), (x-1, y))
                #self.mapping[(x-1, y)] = (x-1, y)
                print("neighbor", x-1, y)
            if ((abs(x) + abs(y+1)) <= self.prod and abs(y+1) < self.n):
                self.graph.add_edge((x,y), (x, y+1))
                #self.mapping[(x, y+1)] = (x, y+1)
                print("neighbor", x, y+1)
            if ((abs(x) + abs(y-1)) <= self.prod and abs(y-1) < self.n):
                self.graph.add_edge((x,y), (x, y-1))
                #self.mapping[(x, y-1)] = (x, y-1)
                print("neighbor", x, y-1)
        
        def draw(self):
                fig = plt.figure()
                ax = fig.gca()
                ax.grid(False)
                nx.draw_networkx(self.graph, pos= self.mapping, ax = ax, with_labels = False, node_size = 10)
                plt.axis('equal')
                plt.show()

G = GemFaceGraph(2,3)
G.draw()
