#!/usr/bin/python

import numpy as np
import time
import matplotlib.pyplot as plt
import random

NUM = 30 

def gen_lattice(Lx,Ly,N=1024):
    X = np.linspace(0.0,Lx,N)
    Y = np.linspace(0.0,Ly,N)
    XX, YY = np.meshgrid(X, Y)
    dx = Lx/float(N-1)
    dy = Ly/float(N-1)
    return (XX,YY,dx,dy)

def update(arr,dt,dx,dy):
	arrRegular = calculateDeltaRegular(arr, dt, dx, dy)
	arrEdgeC = calculateDeltaEdge(arr,dt,dx,dy)
	return arr + arrRegular + arrEdgeC

def calculateDeltaEdge(arr, dt, dx, dy):
	tempArr = np.zeros((NUM,NUM))
	
	for i in range (NUM-1):
		tempArr[i][0] = (-0.5 * arr[i][1] + 0.5 * arr[i][2]) / dy
		tempArr[i][NUM-1] = (-0.5 * arr[i][NUM-2] + 0.5 * arr[i][NUM-3]) / dy
	
	for j in range (NUM-1):
		tempArr[0][j] = (-0.5 * arr[1][j] + 0.5 * arr[2][j]) / dx
		tempArr[NUM-1][j] = (-0.5 * arr[NUM-2][j] + 0.5 * arr[NUM-3][j]) / dx

	tempArr[0][0] = (-0.5 * arr[1][1] + 0.5 * arr[2][2]) / dx*1.4
	tempArr[NUM-1][0] = (-0.5 * arr[NUM-2][1] + 0.5 * arr[NUM-3][2]) / dx*1.4
	tempArr[0][NUM-1] = (-0.5 * arr[1][NUM-2] + 0.5 * arr[2][NUM-3]) / dx*1.4
	tempArr[NUM-1][NUM-1] = (-0.5 * arr[NUM-2][NUM-2] + 0.5 * arr[NUM-3][NUM-3]) / dx*1.4
		
	tempArr *= dt
	return tempArr

def calculateDeltaRegular(arr, dt, dx, dy):
	tempArr = np.zeros((NUM,NUM))
	
	for i in range (NUM):
		for j in range(NUM):
			if i > 0 and i < NUM - 1 and j > 0 and j < NUM - 1:
				tempArr[i][j] = (0.67 * (arr[i+1][j] + arr[i-1][j] + arr[i][j+1] + arr[i][j-1] - (4 * arr[i][j])) + 0.33 * (arr[i+1][j+1] + arr[i-1][j+1] + arr[i+1][j-1] + arr[i-1][j-1] - (4 * arr[i][j]))) / (dx * dy)
	tempArr *= dt
	return tempArr
	
	
if __name__ == '__main__':
    XX,YY,dx,dy = gen_lattice(1.0,1.0,NUM)
    vmin = 0.0
    vmax = 2.0

    #start = 2.0*np.exp(-10.0*(np.power(XX-0.5,2)+np.power(YY-0.5,2)))
    start = np.zeros((NUM,NUM))
	
    for j in range(2000):
		start[random.randrange(0,NUM-1,1)][random.randrange(0,NUM-1,1)] = random.random()+1
	
	
    fig, ax = plt.subplots()
    im = ax.imshow(start,origin='lower',vmin=vmin,vmax=vmax)
	
    step = start
    for i in range(600):
        step = update(step,0.0004,dx,dy) 
        
        ax.cla()
        im = ax.imshow(step,origin='lower',vmin=vmin,vmax=vmax)
        ax.set_title("frame {}".format(i))
        plt.pause(0.0001)