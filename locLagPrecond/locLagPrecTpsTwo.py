
# NAME: 'locLagPrecTpsTwo.py'
#
# PURPOSE: Check effect of local Lagrange preconditioner on condition number
#
# DESCRIPTION: We compute the local Lagrange function preconditioner with 
# thin-plate spline interpolation on the sphere and 
# check its influence on the condition number of the kernel matrix.
# We show that GMRES solver roughly takes a constant number of iterations,
# even for increasing pointset sizes
#
# AUTHOR: NK, kraemer(at)ins.uni-bonn.de

import numpy as np
import matplotlib.pyplot as plt
import scipy.spatial
import scipy.sparse.linalg as spla

import sys
sys.path.insert(0,'../modules/')
from kernelFcts import tpsKernelSphere
from ptSetFcts import getPtsFibonacciSphere
from kernelMtrcs import buildKernelMtrxCond
from miscFcts import locLagPrecon, gmresCounter

def rhsFct(x,y,z):
	return np.exp(x)*(1-x)

print("\nHow many interpolation points? (e.g. 150)")
numPts = int(input("Enter: "))
print("\nWhich local radius? (e.g. 7.0)")
locRadius = float(input("Enter: "))
print("\nWhich GMRES tolerance? (e.g. 1e-10)")
gmresTol = float(input("Enter: "))
print("")

ptSet = getPtsFibonacciSphere(numPts)
kdTree = scipy.spatial.KDTree(ptSet)

kernelMtrx = buildKernelMtrxCond(ptSet, ptSet, tpsKernelSphere)
preconMtrx, numNeighb = locLagPrecon(ptSet, kdTree, locRadius, buildKernelMtrxCond, tpsKernelSphere, 4)
conditionedMtrx = kernelMtrx.dot(preconMtrx)
conditionedMtrx = conditionedMtrx[0:numPts, 0:numPts]

print('Number of neighbors for localisation:')
print('\tn =', numNeighb)

print('\nEffect of preconditioner:')
print('\tcond(K) =', np.linalg.cond(kernelMtrx))
print('\tcond(KP) =', np.linalg.cond(conditionedMtrx))

rhsVec = np.zeros(numPts)
for idx in range(numPts):
	rhsVec[idx] = rhsFct(ptSet[idx,0], ptSet[idx,1], ptSet[idx,2])

gmresCtr = gmresCounter()
solVec, info = spla.gmres(conditionedMtrx, rhsVec, tol = gmresTol, callback = gmresCtr)
print("\nNumber of iterations for GMRES: ")
print('\tnumIt =', gmresCtr.numIter)
print("")


