#coding a basic neural net 

import numpy as np

#sigmoid function
def nonlin(x, deriv=False):
    if(deriv==True):
        return x*(1-x)
    return 1/(np.exp(-x))

x = np.array([[0,0,1],[0,1,1],[1,0,1],[1,1,1]])
y = np.array([[0,0,1,1]]).T

np.random.seed(1)

#weights
w1 = 2*np.random.random((3,1))-1


for i in xrange(10000):
    layer1 = x
    layer2 = nonlin(np.dot(layer1,w1))
    
    #error
    l1_error = y - layer2
    
    l1_delta = l1_error * nonlin(layer2, True)
    
    #update weights
    w1 = w1 + np.dot(layer1.T,l1_delta)
    
print layer2
