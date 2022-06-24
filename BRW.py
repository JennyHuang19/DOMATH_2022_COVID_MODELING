"""
06/24/22
June Lee
"""
from scipy.stats import pareto
import math
import numpy as np
import random
import matplotlib.pyplot as plt

def BRW(N, beta, gamma, a, t):
    #initial list of particles
    currGen = [0 for i in range(N+1)]
    #placeholder while updating
    
    left = 0
    right = 0
    #initial particle
    currGen[N//2 + 1] = 1
    
    # for each timestep
    for t in range(t):
        nextGen = [0 for i in range(N+1)]
        # for each location
        for x in range(N+1):
            # for each particle at given location
            births = np.random.binomial(currGen[x], beta/(beta + gamma)) # num births at site x
            nextGen[x] += births
            
            newLocs = pareto.rvs(a, size=births)
    
            for i in range(len(newLocs)):
                newLoc = round(newLocs[i])
                leftright = random.randint(0,1)
                
                if leftright == 0:
                    left += 1
                    if x - newLoc < 0:
                        tempX = -(x - newLoc) % N
                        nextGen[-tempX] += 1
                    else:
                        nextGen[x - newLoc] += 1
                else:
                    right += 1
                    if x + newLoc > N:
                        tempX = (x + newLoc) % N
                        nextGen[tempX] += 1
                    else:
                        nextGen[x + newLoc] += 1
                    
    currGen = nextGen
    
    return(currGen)


if __name__ == '__main__':
    N = 100
    beta = 4
    gamma = 1
    a = 0.1
    t = 15
    numTrials = 100
    
    total = [0 for i in range(N+1)]
    for i in range(numTrials):
        currGen = BRW(N, beta, gamma, a, t)
        for j in range(len(currGen)):
            total[j] += currGen[j]
    
    
    x = [i for i in range(-N//2, N//2 + 1)]
    
    plt.figure()
    fig, ax = plt.subplots()
    plt.bar(x, total)
    plt.title(f'BRW, Alpha = {a}')
    plt.xlabel('Location')
    plt.ylabel('# of Particles')       
    plt.savefig(f'BRW_alpha{a}.png', bbox_inches='tight')
    plt.close('all')
