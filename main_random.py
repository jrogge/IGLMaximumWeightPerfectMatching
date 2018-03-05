#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 08:58:48 2018

@author: shulinfang
"""
import numpy as np
import dominoGraph
import vertexGraph
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import scipy.stats as stats
import matplotlib.mlab as mlab

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
def height(n, prev, weighted=False, visual=False, previous=False):
	dg = dominoGraph.DominoGraph(n, weighted=weighted)
	vg = vertexGraph.VertexGraph(n)
	avoid_edges = dg.get_avoid_edges()
	if visual:
		visualize(dg, vg, avoid_edges)
	X, Y, Z = vg.height_map(avoid_edges)
	height.x = X
	height.y = Y
	height.f = Z
	if previous:
		height.sum = np.add(Z,prev)
'''
	fig = plt.figure()
	ax = fig.gca(projection='3d')
	ax.plot_trisurf(X, Y, Z, linewidth=0.2, antialiased=True, shade=True, cmap=cm.coolwarm)
	plt.show()

height(100, 0, visual=False, weighted=True, previous=False)
'''
n = 20
iteration = 20
height(n, 0, visual=False, weighted=True, previous=False)
h = []
for i in range(iteration):
	h.append(height.f)
	height(n, height.f, visual=False, weighted=True, previous=True)

Ef = height.sum/iteration

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_trisurf(height.x, height.y, Ef, linewidth=0.2, antialiased=True, shade=True, cmap=cm.coolwarm)
plt.show()


'''
Graph - Distribution of Heights
'''
h = np.sum(h, axis=1)
fig = plt.figure()
plt.hist(h)
plt.title('Distribution of Heights')
plt.show()
'''
Graph - Probability distribution of Heights
'''
fig = plt.figure()
h_sorted = np.sort(h)
mu = np.mean(h_sorted) 
sigma = np.std(h_sorted) 
x = mu + sigma * np.random.randn(10000)
num_bins = iteration
n, bins, patches = plt.hist(x, num_bins, normed=1, facecolor='orange', alpha=0.75)
y = mlab.normpdf(bins, mu, sigma)
l = plt.plot(bins, y, 'r--', linewidth=1)
plt.title('Probability Distribution of Heights')
plt.show()

