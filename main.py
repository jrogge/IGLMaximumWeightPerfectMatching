import dominoGraph
import vertexGraph
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

'''
Function to visualize the domino tiling on our Aztec diamond
Only effective for seeing for cases strictly less than 18
'''
def visualize(dg, vg, avoid_edges):
	for edge in avoid_edges:
		vg.remove_edge(edge)
	vg.draw()

'''
Displays the height function of the Aztec diamond with fixed point and black square
See vertexGraphs height map function for more details
'''
def height(n, weighted=False, visual=False, test_time=False):
	dg = dominoGraph.DominoGraph(n, weighted=weighted)
	vg = vertexGraph.VertexGraph(n)
	avoid_edges = dg.get_avoid_edges()
	if visual:
		visualize(dg, vg, avoid_edges)
	X, Y, Z = vg.height_map(avoid_edges)

	if not test_time:
		fig = plt.figure()
		ax = fig.gca(projection='3d')
		ax.plot_trisurf(X, Y, Z, linewidth=0.2, antialiased=True, shade=True, cmap=cm.coolwarm)
		plt.show()


'''
Prints time performance for a graph of size n
'''
def get_time_performance(n):
	startTime = time.time()
	height(n, visual=False, weighted=True, test_time=True)
	print(time.time() - startTime)

'''
Prints time performance on all graphs up to size n
'''
def get_time_performances_to(n):
	for i in range(0, n):
		get_time_performance(i)

get_time_performances_to(20)
