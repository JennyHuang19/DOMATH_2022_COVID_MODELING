"""
06/24/22
June Lee
"""
from scipy.stats import pareto
import math
import numpy as np
import random
import matplotlib.pyplot as plt

def BRW(N, m, beta, gamma, a, t):
    #initial list of particles
    currGen = [0 for i in range(N+1)]
    #placeholder while updating
    
    
    #initial particle
    currGen[N//2 + 1] = 1
    
    # for each timestep
    for t in range(t):
        nextGen = [0 for i in range(N+1)]
        # for each location
        for x in range(len(currGen)):
            # for each particle at given location
            births = np.random.binomial(currGen[x], beta/(beta + gamma)) # num births at site x
            nextGen[x] += births
            if births == 0:
                break
            
            newLocs = pareto.rvs(a, size=births)
    
            for i in newLocs:
                newLocs[i] = math.ceil(newLocs[i])
                leftright = random.randit(0,1)
                if leftright == 0:
                    if x - newLocs[i] < 0:
                        tempX = -(x - newLocs[i]) % N
                        nextGen[tempX] += 1
                    else:
                        nextGen[x - newLocs[i]] += 1
                else:
                    if x + newLocs[i] > N:
                        tempX = (x + newLocs[i]) % N
                        nextGen[tempX] += 1
                    else:
                        nextGen[x + newLocs[i]] += 1
                    
            
                    
        currGen = nextGen
    
    return (currGen)


if __name__ == '__main__':
    N = 100
    m = 5
    beta = 6
    gamma = 1
    a = 1/2
    t = 10
    currGen = BRW(N, m, beta, gamma, a, t)
    
    plt.figure()
    fig, ax = plt.subplots()
    ax.plot(currGen, label='# of particles')
    ax.legend(loc='upper right')
    plt.title('BRW')
    plt.xlabel('Location')
    plt.ylabel('# of particles at Location')       
    plt.savefig('BRW.png', bbox_inches='tight')
    plt.close('all')