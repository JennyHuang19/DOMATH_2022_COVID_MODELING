"""
06/20/22
June Lee
"""

import math
import numpy as np
import random
import matplotlib.pyplot as plt
import PIL


"""
Individuals (Ind) Class
Class Attributes:
state: str, 'S', 'I', or 'R'
locX: int, x-coordinate location
locY: int, y-coordinate location
neigh: list of pointers to its neighbors within distance L
"""

class Individual:
    
    """
    Class Attributes:
    state: str, 'S', 'I', or 'R'
    locX: int, x-coordinate location
    locY: int, y-coordinate location
    """
    
    def __init__(self, locX, locY):
        # first placed on grid as S
        self.state = 'S'
        self.locX = locX
        self.locY = locY
        self.dist = 0.0

    
"""
long_range(N, L, beta, gamma, timestep, initInfected)
simulate spreading behavior
INPUTS: int N, int L, float beta, float gamma, int timestep, int initInfected
"""

def long_range(N, L, beta, gamma, initInfected, t):
    # initialize population
    # indexed s.t. pop[i][j] is individual with locX = i and locY = j
    pop = [[Individual(i,j) for i in range(N)] for j in range(N)]
    grid = PIL.Image.new(mode='RGB', size=(N,N), color=(0, 0, 0))
    pixels = grid.load()
    
    
    # preallocate lists
    # infected: list of pointers to infected individuals
    infected = []
    # numinfected: used to track # of infected at each timestep
    numInfected = []
    distance = []
    
    """
    # choose random starting infection site and # of initial infections
    for k in range(initInfected):
        xInit = random.randint(0, N-1)
        yInit = random.randint(0, N-1)
        pop[xInit][yInit].state = 'I'
        infected.append(pop[xInit][yInit])
        pixels[xInit, yInit] = (255,0,0)
    
    """
    # or pick a starting infection site
    xInit = N//2
    yInit = N//2
    pop[xInit][yInit].state = 'I'
    infected.append(pop[xInit][yInit])
    pixels[xInit, yInit] = (0,255,0)
    
    
    # set numInfected[0] as initInfected
    numInfected.append(1)
    grid.save('initGrid.jpg')
    
    # run spreading simulation for t timesteps
    # or run simulation until no more infected individuals remain
    timestep = 0
    distance.append(0)
    for t in range(t):
    #while len(infected) != 0:
        timestep = timestep + 1
        # for each timestep, track new infections and recoveries 
        # using list recovered newInfected
        recovered = []
        newInfected = []
        distNewInfected = []
        # for each infected individual
        for i in range(len(infected)):
            
            # infect or recover at given probabilities
            s = random.uniform(0, beta + gamma)
            
            # infect
            if s >= gamma:
                # allocate LxL
                xUB = infected[i].locX + L
                xLB = infected[i].locX - L
                yUB = infected[i].locY + L
                yLB = infected[i].locY - L
                
                # randomly choosing a neighbor in LxL
                xRand = random.randint(xLB, xUB)
                yRand = random.randint(yLB, yUB)
                
                # if infected individual himself chosen, redraw
                while xRand == 0 and yRand == 0:
                    xRand = random.randint(xLB, xUB)
                    yRand = random.randint(yLB, yUB)
                    
                # mod NxN (list indexed from 0 to N-1)
                if xRand > N-1:
                    tempX = xRand % (N-1)
                    xRand = tempX
                    
                if yRand > N-1:
                    tempY = yRand % (N-1)
                    yRand = tempY
                    
                if xRand < 0:
                    tempX = -xRand % (N-1)
                    xRand = -tempX
                    
                if yRand < 0:
                    tempY = -yRand % (N-1)
                    yRand = -tempY
                
                # if chosen neighbor is S, then infect and add to 
                # list of infected
                if pop[xRand][yRand].state == 'S':
                    pop[xRand][yRand].state = 'I'
                    newInfected.append(pop[xRand][yRand])
                    pop[xRand][yRand].dist = math.sqrt((xRand - xInit)**2 + (yRand - yInit)**2)
                    distNewInfected.append(pop[xRand][yRand].dist)
            
            
            # remove
            #elif s < gamma:
            #    infected[i].state = 'R'
            #    recovered.append(infected[i])
            
            
            # SIS model, return to S
            elif s < gamma:
                infected[i].state = 'S'
                recovered.append(infected[i])
                
        for i in recovered:
            pixels[i.locX, i.locY] = (0,0,0)
        # after infecting/removing
        updateInfected = []
        
        for j in range(len(infected)):
            if infected[j].state == 'I':
                updateInfected.append(infected[j])
                    
    
        # append new infections from timestep to list infected
        infected = updateInfected + newInfected
        for i in infected:
            pixels[i.locX, i.locY] = (0,255,0)
        
        # append total number of infecteds to numInfected
        numInfected.append(len(infected))
        if len(infected) == 0:
            raise ValueError('NumInfected == 0')
            
        print(len(infected))
        
        radius = 0.0
        distNewInfected.sort(reverse=True)
        for r in range((len(distNewInfected)//10) + 1):
            radius = radius + distNewInfected[r]
            
        avgRadius = radius/((len(distNewInfected)//10) + 1)
        
            
        distance.append(avgRadius)
        grid.save(f'N{N}_L{L}_B{beta}_t{timestep}.jpg')
        
    
    grid.save('finalGrid.jpg')
    
    plt.figure()
    fig, ax = plt.subplots()
    ax.plot(distance, label='d')
    ax.legend(loc='upper left')
    plt.title(f'Maximum Infected Distance from Initial per Time, N = {N}, L{L}, B = {beta}')
    plt.xlabel('Time')
    plt.ylabel('Distance from Initial Infected')
    plt.savefig(f'distance_N{N}_L{L}_B{beta}.png', bbox_inches='tight')
    plt.close('all')
        
    return (numInfected, distance)

    
if __name__ == "__main__":
    N = 225
    L = 15
    beta = [2, 3, 4]
    gamma = 1
    t = 100
    # if choosing a specific starting infection site, chose initInfected that
    # is a square; 9, 16, 25, etc.
    initInfected = 0
    
    plt.figure()
    fig, ax = plt.subplots()
    
    for i in range(len(beta)):
        (infections, distance) = long_range(N, L, beta[i], gamma, initInfected, t)
        ax.plot(infections, label=f'I, Beta = {beta[i]}')
    
    ax.legend(loc='upper right')
    plt.title(f'Long Range # Infected per Timestep,  N = {N}, L = {L}')
    plt.xlabel('Time')
    plt.ylabel('# of Infected Individuals')       
    plt.savefig('long_range.png', bbox_inches='tight')
    plt.close('all')
    
    
    
    
