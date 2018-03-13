import utils

n = 15
X, Y, Z = utils.expected_surface_parallel(n, 90, 5)
#utils.plot(X, Y, Z,"Height Function")
X1,Y1,Z1 = utils.transform(n,X,Y,Z)
#utils.plot(X1,Y1,Z1,"Height Function range(-1,1)")

X_int, Y_int, Z_int = utils.interpolate_grid(n, X, Y, Z, method='cubic')
utils.plot(X_int, Y_int, Z_int,"Height Function by Midpoints")
X_n, Y_n, Z_n = utils.transform(n, X_int, Y_int, Z_int)
# for i in range(len(X_n)):
# 	if(Z_n[i] > 0.7):
# 		print(X_n[i], Y_n[i], Z_n[i])
utils.plot(X_n, Y_n, Z_n,"height Function by Midpoints range(-1,1)")
err = Z_n-(X_n*Y_n)
utils.plot(X_n,Y_n,err,"Error of Height Function")
innerProduct = sum(Z_n)/(n**2)
print(innerProduct)






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
