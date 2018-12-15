# NAME: 'rileyAlgBasic.py'

# PURPOSE: Check the influence of the shifts 
# and accuracy onto Riley's Algorithm

# DESCRIPTION: I solve a system involving an exponential kernel matrix 
# and iteratively compute the approximations with Riley's algorithms
# (as in (2) on slide 42 on https://drna.padovauniversitypress.it/system/files/papers/Fasshauer-2008-Lecture3.pdf)

# AUTHOR: NK, kraemer(at)ins.uni-bonn.de

import numpy as np
from ptSetFcts import getPtsHalton
from kernelMtrcs import buildKernelMtrx, buildKernelMtrxShift
from kernelFcts import expKernel

import scipy.special

np.set_printoptions(precision = 1)

print "\nHow many points shall we work with? (e.g. 100)"
print "\tnumPts = ?"
numPts = input("Enter: ")

print "\nWhich spatial dimension? (e.g. 2)"
print "\tdim = ?"
dim = input("Enter: ")

print "\nWhich shift for Riley? (e.g. 0.001)"
print "\trileyShift = ?"
rileyShift = input("Enter: ")

print "\nWhich accuracy for Riley? (e.g. 1e-08)"
print "\trileyAcc = ?"
rileyAcc = input("Enter: ")

print "\nWhich maximal number of iterations? (e.g. 1000)"
print "\trileyNumMaxIt = ?"
rileyNumMaxIt = input("Enter: ")
print ""


ptSet = getPtsHalton(numPts,dim)


kernelMtrx = buildKernelMtrx(ptSet,ptSet, expKernel)
kernelMtrxShift = buildKernelMtrxShift(ptSet,ptSet, expKernel, rileyShift)

rhs = np.zeros(len(ptSet))
rhs[0] = 1

trueSol = np.linalg.solve(kernelMtrx,rhs)

print "\nIterations - relative errors:"
startVec = np.linalg.solve(kernelMtrxShift,rhs)
currIt = np.zeros(numPts)
counter = 0
currentRelError = 100.0
while currentRelError >= rileyAcc and counter <= rileyNumMaxIt:
	counter = counter + 1
	currIt = startVec + rileyShift * np.linalg.solve(kernelMtrxShift, currIt)
	currentRelError = np.linalg.norm(currIt - trueSol)/np.linalg.norm(trueSol)
	print counter, "-", '{:.5e}'.format(currentRelError)
print ""


