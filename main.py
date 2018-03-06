import dominoGraph
import vertexGraph
import time
import matplotlib.pyplot as plt
import math
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from multiprocessing import Process, Queue

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
		plot(X, Y, Z)
	return X, Y, Z

def plot(X,Y, Z):
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
	print(n, time.time() - startTime)

'''
Helper function for parallel version. Starts at a base and jumps according to step size
'''
def get_time_performance_jumps(base, step_size, maximum):
	for i in range(base + 1, maximum + 1, step_size):
		get_time_performance(i)

'''
Prints time performance on all graphs up to size n
'''
def get_time_performances_to(n):
	get_time_performance_jumps(0, 1, n)

'''
Computes time performances in parallel
'''
def parallel_time_to(n, num_process):
	processes = []
	for i in range(num_process):
		p = Process(target=get_time_performance_jumps, args=(i, num_process, n))
		processes.append(p)
		p.start()

	for p in processes:
		p.join()

'''
Computes the average of the random surfaces according to corresponding values
'''
def expected_surface(n, samples, parallel=False, queue=None):
	X, Y, Z = height(n, weighted=True, test_time=True)
	for i in range(samples - 1):
		Xi, Yi, Zi = height(n, weighted=True, test_time=True)
		Z += Zi
	if parallel:
		queue.put((X, Y, Z))
		return
	else:
		return X, Y, Z/samples

'''
Does the expected_surface function in parallel
'''
def expected_surface_parallel(n, samples, num_process):
	processes = []
	rem_process = num_process
	rem_samples = samples
	queue = Queue()
	for i in range(num_process):
		p = Process(target=expected_surface, args=(n, math.ceil(rem_samples/rem_process), True, queue))
		rem_samples -= math.ceil(rem_samples/rem_process)
		rem_process -= 1
		processes.append(p)
		p.start()

	X, Y, Z = queue.get()
	while not queue.empty():
		Xi, Yi, Zi = queue.get()
		Z += Zi

	for process in processes:
		process.join()

	return X, Y, Z/samples


#get_time_performances_to(25)
#parallel_time_to(25, 5)
#height(17, weighted=True, visual=True)
#X, Y, Z = expected_surface(10, 50)
#plot(X, Y, Z)
X, Y, Z = expected_surface_parallel(15, 30, 5)
plot(X, Y, Z)


