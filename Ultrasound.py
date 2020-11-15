#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 22:26:44 2020

@author: soonmi
"""

import numpy as np
import math as m
from scipy.io import loadmat
import matplotlib.pyplot as plt

usd = loadmat('ultrasounddata.mat')
Un = usd['Undata']

zeroCube = np.zeros((64,64,64), complex) #64x64x64 cube with zeros

UnCube = zeroCube
addCube = zeroCube
avgCube = zeroCube
gaussCube = zeroCube
marbleLoc = zeroCube

L = 15 #spatial domain
n = 64 #Fouriet modes
x2 = np.linspace(-L, L, n+1) #list from -15 to 15 with 64 evenly spaced numbers in between
x = x2[1:n+1] #first row, all the values
y = x
z = x
K = m.pi/L*x


#converting from space to frequency

for i in range(0,20):
    UnCube[:,:,:] = np.reshape(Un[i,:],(n,n,n)) 
    fftCube = np.fft.fftn(UnCube) #taking the freq of each sample
    addCube = addCube + fftCube #sum of all the fft cubes


#finding the prominent frequency in all the samples
    
avgCube = addCube/20 #avg of all the fft cubes

maxVal = np.max(avgCube) #max freq in all the cubes

print("The maximum amplitude is : " + str(maxVal))

for i in range(0,64):
    for j in range(0,64):
        for k in range(0,64):
            if avgCube[i,j,k]== maxVal:
                Kx = K[i]
                Ky = K[j]
                Kz = K[k]
                print("Kx: " + str(Kx) + ", Ky: " + str(Ky) + ", Kz: " + str(Kz))

#going back to space
                
LocX = np.zeros((1,20), float)
LocY = np.zeros((1,20), float)
LocZ = np.zeros((1,20), float)

for s in range(0,20): #for each sample

    UnCube[:,:,:] = np.reshape(Un[s,:],(n,n,n))
    fftCube = np.fft.fftn(UnCube) #taking the freq of each sample
    
    #filtering each point in the sample
    for i in range(0,64):
        for j in range(0,64):
            for k in range(0,64):
                gaussCube[i,j,k] = fftCube[i,j,k] * np.exp(-(K[i] - Kx)**2 - (K[j] - Ky)**2 - (K[k] - Kz)**2)
    
    #converting each point in the filtered sample back to space        
    spaceCube = np.fft.ifftn(gaussCube)
    marbleMax = np.max(spaceCube)
    
    print("The strength of the signal returned by the marble: " + str(marbleMax))
    #locating the marble in the sample 
    #print(marbleMax)
    
    for i in range(0,64):
        for j in range(0,64):
            for k in range(0,64):
                if spaceCube[i,j,k]== marbleMax:
                    LocX[0,s] = x[i]
                    LocY[0,s] = y[j]
                    LocZ[0,s] = z[k]
                    print("Location at Sample {}:\t{}" .format(s+1,[LocX[0,s], LocY[0,s], LocZ[0,s]]))

#plotting
                    
fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')

X, Y, Z = LocX, LocY, LocZ
ax.plot_wireframe(X,Y,Z)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

plt.show()                    
                    
                    
                    
         
