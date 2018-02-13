import dominoGraph
import vertexGraph
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

'''
Function to visualize the domino tiling on our Aztec diamond
Only effective for seeing for cases strictly less than 18
'''
def visualize(n):
	dg = dominoGraph.DominoGraph(n)
	vg = vertexGraph.VertexGraph(n)
	avoid_edges = dg.get_avoid_edges()
	for edge in avoid_edges:
		vg.remove_edge(edge)
	vg.draw()


def height(n):
	dg = dominoGraph.DominoGraph(n)
	vg = vertexGraph.VertexGraph(n)
	avoid_edges = dg.get_avoid_edges()
	X, Y, Z = vg.height_map(avoid_edges)
	
	for i in range(len(X)):
		print(X[i], Y[i], Z[i])

	fig = plt.figure()
	ax = fig.gca(projection='3d')
	ax.plot_trisurf(X, Y, Z, linewidth=0.2, antialiased=True)
	plt.show()


#visualize(2)
height(153)
