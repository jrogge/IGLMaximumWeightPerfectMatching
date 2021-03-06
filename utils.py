import dominoGraph
import vertexGraph
import gemGraph
import gemFaceGraph
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import math
import plotly.plotly as py
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from multiprocessing import Process, Queue
from pandas import DataFrame
from scipy import interpolate

'''
Function to print out data to an Excel file
This takes in an filename, sheet name, X, Y, and Z coordinates
Add the extension for the file in filename
'''
def save_to_excel(filename, X, Y, Z, sheet_name='sheet1'):
	df = DataFrame({'X': X, 'Y': Y, 'Heights (Z)': Z})
	df.to_excel(filename, sheet_name = sheet_name, index=False)

'''
Function to visualize the domino tiling on our Aztec diamond
Only effective for seeing for cases strictly less than 18
'''
def visualize(dg, vg, avoid_edges):
#	for edge in avoid_edges:
#		vg.remove_edge(edge)
#	Should not remove edges, as these will affect the graph
	vg.draw(avoid_edges)

'''
Push height data into the javascript file to be visualized
'''
def loadData(heights, order):
        heights = heights[::-1] # necessary because of how the data is stored
        classFilename = "WebGL/Terrain.js"
        renderFilename = "WebGL/boilerplate.js"

        # read render file 
        renderFile = open(renderFilename, "r");
        renderData = renderFile.read().split("\r\n");
        renderData[0] = "var meshSize = {};".format(2 * order)
        # render can be overwritten immediately
        renderFile.close()
        renderFile = open(renderFilename, "wb");
        for line in renderData:
            renderFile.write(line + "\n")
        renderFile.close()

        # read class file so we can add height map
        classFile = open(classFilename, "r");
        classData = classFile.read().split("\r\n");
        classFile.close()

        heightData = "var heightMap = ["
        lastIndex = len(heights)-1
        for i in xrange(lastIndex):
                heightData += str(heights[i]) + ", "
        heightData += str(heights[lastIndex]) + "];"
        classData[0] = heightData
        classFile = open(classFilename, "wb");
        for line in classData:
            classFile.write(line + "\r\n")
        classFile.close()

'''
Displays the height function of the Aztec diamond with fixed point and black square
See vertexGraphs height map function for more details
X, Y, and Z are returned such that for any point, X[i], Y[i], and Z[i] are paired
The order of the array follows the order of traversal in the vertexGraph.py file
See traversal_example.png in the pictures folder for an example
'''
def height(n, a=0, graph='aztec', weighted=False, visual=False, test_time=False):
	if(graph=='gem'):
		dg = gemFaceGraph.GemFaceGraph(n, a, weighted=weighted)
		vg = gemGraph.GemGraph(n, a)
	else:
		dg = dominoGraph.DominoGraph(n, weighted=weighted)
		vg = vertexGraph.VertexGraph(n)
	avoid_edges = dg.get_avoid_edges()
	X, Y, Z = vg.height_map(avoid_edges)
	if visual:
		visualize(dg, vg, avoid_edges)
		loadData(Z, n)

	if not test_time:
		plot(X, Y, Z)
	return X, Y, Z

def plot(X,Y, Z, title):
	fig = plt.figure()
	ax = fig.gca(projection='3d')
	ax.plot_trisurf(X, Y, Z, linewidth=0.2, antialiased=True, shade=True, cmap=cm.coolwarm)
	plt.title(title)
	plt.show()



'''	
Prints time performance for a graph of size n
'''
def get_time_performance(n, a=0, graph='aztec'):
	startTime = time.time()
	if graph=='gem':
		height(n, a, graph, visual=False, weighted=True, test_time=True)
	else:
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
def expected_surface(n, samples, a=0, graph='aztec', parallel=False, queue=None):
	if graph == 'gem':
		X, Y, Z = height(n, a, graph, weighted=True, test_time=True)
	else:
		X, Y, Z = height(n, weighted=True, test_time=True)
	for i in range(samples - 1):
		if graph == 'gem':
			Xi, Yi, Zi = height(n, a, graph, weighted=True, test_time=True)
		else:
			Xi, Yi, Zi = height(n, weighted=True, test_time=True)
		Z += Zi
	if parallel:
		queue.put((X, Y, Z))
		queue.close()
	else:
		return X, Y, Z/samples

'''
Does the expected_surface function in parallel
'''
def expected_surface_parallel(n, samples, num_process, a=0, graph='aztec'):
	processes = []
	h = []
	rem_process = num_process
	rem_samples = samples
	queue = Queue()
	for i in range(num_process):
		p = Process(target=expected_surface, args=(n, math.ceil(rem_samples/rem_process), a, graph, True, queue))
		rem_samples -= math.ceil(rem_samples/rem_process)
		rem_process -= 1
		processes.append(p)
		p.start()

	X, Y, Z = queue.get()
	for i in range(1, len(processes)):
		Xi, Yi, Zi = queue.get()
		h.append(Zi)
		Z += Zi

	for process in processes:
		process.join()

	expected_surface_parallel.h = h
	return X, Y, Z/samples

'''
Function to get the midpoints for every edge in our vertex graph
Can probably do this in a better way...
'''
def find_midpoints(n, tup=False):
	vg = vertexGraph.VertexGraph(n)
	return vg.get_midpoints(tup=tup)

'''
Interpolates points and returns the height for associated points
This is used to approximate the height at different points where
we have no vertices for, i.e. in this case, the edge midpoints
'''
def interpolate_grid(n, X, Y, Z, method='linear'):
	#4n + 5 points in our grid row
	xi = np.fromiter((-n - 1 + 0.5*i for i in range(0, 4*n+5, 1)), float)
	zi = interpolate.griddata((X, Y), Z, (xi[None,:], xi[:,None]), method='linear')
	midX, midY = find_midpoints(n)
	xi_coords = {value: index for index, value in enumerate(xi)}
	yi_coords = {value: index for index, value in enumerate(xi)}
	new_z = np.zeros(len(midX))
	for i in range(len(midX)):
		new_z[i] = zi[xi_coords[midX[i]], yi_coords[midY[i]]]
	return midX, midY, new_z

'''
Finds the distribution of error from a given graph and it's expected graph
'''
def get_errors(error_samples, n, expected_g_samples, threads=5, a=0, graph='aztec'):
	errors = np.zeros(error_samples)
	X, Y, Z = expected_surface_parallel(n, expected_g_samples, threads, a=a, graph=graph)
	for i in range(error_samples):
		Xi, Yi, Zi = height(n, a=a, graph=graph, weighted=True, visual=False, test_time=True)
		for j in range(len(Zi)):
			errors[i] += abs(Zi[j]-Z[j])
	return errors

'''
Plots the total error in the form of a histogram
'''
def plot_errors(error_samples, n, expected_g_samples, threads=5, a=0, graph='aztec'):
	errors = get_errors(error_samples, n, expected_g_samples, threads=threads, a=a, graph=graph)
	plt.hist(errors)
	if graph == 'aztec':
		plt.title("Histogram of errors for Aztec " + str(n))
	else:
		plt.title("Histogram of errors for Gem (" + str(n) + "," + str(a) + ")")
	plt.xlabel("Error")
	plt.ylabel("Frequency")
	plt.show()


'''
Transforms the input set of coordinate values and scales into a range of [-1, 1]
'''
def transform(n, X, Y, Z):
	new_X = scale(X - Y, -1, 1)
	new_Y = scale(X + Y, -1, 1)
	new_Z = scale(Z, -1, 1)
	return new_X, new_Y, new_Z

'''
Scales all the values of an array to fit into a range
Currently probably incorrect for what we need
'''
def scale(X, a, b):
	maximum = np.max(X)
	minimum = np.min(X)
	return (b - a) * (X - minimum * np.ones(len(X)))/(maximum - minimum) + a * np.ones(len(X))
