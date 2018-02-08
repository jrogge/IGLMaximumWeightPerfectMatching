import dominoGraph
import vertexGraph

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

visualize(5)