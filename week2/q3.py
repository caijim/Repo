import numpy.linalg as LA
import numpy as np
from numpy import *

def my_matrixinv(mat):
    #join identity
    det = LA.det(mat)
    if det==0:
        return 'Not Invertible'
    indices = range(len(mat))
    working = hstack([mat, eye(len(mat))])
    for i in range(len(mat)):
        mult = 1/float(working[i,i])
        working[i,:] = mult*working[i,:]
        adding_row = working[i,:]
        for j in indices:
            if not j==i:
                interested=working[j,i]
                working[j,:] =-interested*adding_row+working[j,:]
    inverse = working[:,len(mat):]
    return inverse


"""
mat = np.array([[ 1, -1,  3],
       [ 4,  2,  4],
       [-2, -2,  1]])

print invert(mat)
print np.dot(mat, invert(mat))
"""
