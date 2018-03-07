import utils

n = 15
X, Y, Z = utils.expected_surface_parallel(n, 20, 5)
utils.plot(X, Y, Z)
xi, yi, zi = utils.interpolate_grid(n, X, Y, Z, method='cubic')
utils.plot(xi, yi, zi)

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
