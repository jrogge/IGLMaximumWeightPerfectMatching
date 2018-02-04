import networkx as nx
import matplotlib.pyplot as pyplot

class SurfaceGraph:
    def __init__(self, size):
        self.graph = nx.Graph()
        self.graph.add_node((0,0))
        self.size = 0
        for i in xrange(self.size, size):
            self.add_layer()

    def add_layer(self):
        self.size += 1
        self.graph.add_node((0,-self.size)) # nodes at top or bottom of graph
        self.graph.add_edge((0,-self.size), (0, 1 - self.size)) # connecting edge
        for i in xrange(1 - self.size, self.size - 1): # nodes between top and bottom
            # nodes on right edge of diamond
            self.graph.add_node((i, self.size-i))
            self.graph.add_edge((i-1, self.size-i), (i, self.size-i))
            # nodes on left edge of diamond
            self.graph.add_node((-i, self.size-i))
            self.graph.add_edge((1-i, self.size-i), (-i, self.size-i))
        self.graph.add_node((0, self.size))
        self.graph.add_edge((0, self.size), (0, self.size-1))

    def draw(self):
        nx.draw(self.graph, with_labels=True, font_weight='bold')
        pyplot.show()

test = SurfaceGraph(5)
test.draw()
