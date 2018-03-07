import dominoGraph
import vertexGraph
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import math
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
	for edge in avoid_edges:
		vg.remove_edge(edge)
	vg.draw()

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
def height(n, weighted=False, visual=False, test_time=False):
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
		queue.close()
	else:
		return X, Y, Z/samples

'''
Does the expected_surface function in parallel
'''
def expected_surface_parallel(n, samples, num_process):
	processes = []
	h = []
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
Interpolates points and returns the associated function
This is used to approximate the height at different points where
we have no vertices for
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


#get_time_performances_to(25)
#parallel_time_to(25, 5)
#height(18, weighted=True, visual=False)
#X, Y, Z = expected_surface(15, 30)
#plot(X, Y, Z)
n = 15
X, Y, Z = expected_surface_parallel(n, 20, 5)
plot(X, Y, Z)
xi, yi, zi = interpolate_grid(n, X, Y, Z, method='cubic')
plot(xi, yi, zi)

#plot(X, Y, Z)
#
#
#
#'''
#Graph - Distribution of Heights
#'''
#h = expected_surface_parallel.h
#h = np.sum(h, axis=1)
#fig = plt.figure()
#plt.hist(h)
#plt.title('Distribution of Heights')
#plt.show()
#'''
#Graph - Probability distribution of Heights
#'''
#fig = plt.figure()
#h_sorted = np.sort(h)
#mu = np.mean(h_sorted) 
#sigma = np.std(h_sorted) 
#x = mu + sigma * np.random.randn(10000)
#num_bins = 10
#n, bins, patches = plt.hist(x, num_bins, normed=1, facecolor='orange', alpha=0.75)
#y = mlab.normpdf(bins, mu, sigma)
#l = plt.plot(bins, y, 'r--', linewidth=1)
#plt.title('Probability Distribution of Heights')
#plt.show()
