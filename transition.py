"""
5/25/22
June Lee, Sofie Hletko
"""

import math
import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt

"""
calcCasesByVariant()
INPUTS: specify csv files.
OUTPUTS: x = list, percentage of variant 1 among infected.
         y = list, percentage of vairant 2 among infected.
         biweeklyCases = list, total number of cases
         numDelta = list, # of cases Delta
         numOmicron = list, # of cases Omicron
"""

def calcCasesByVariant():
    # access csv files, change file name as necessary
    casesData = pd.read_csv('CDC052322.csv', skiprows=(0,1))
    varData = pd.read_csv('CovidPropsJ.csv')

    # specify columns, convert to numpy
    dates = pd.DataFrame(casesData, columns=['Date'])
    avgCases = pd.DataFrame(casesData, columns=['7-Day Moving Avg'])
    dates = pd.DataFrame.to_numpy(dates, dtype=str)
    avgCases = pd.DataFrame.to_numpy(avgCases, dtype=int)
    
    percentDelta = pd.DataFrame(varData, columns=['perc_deltas'])
    percentOmicron = pd.DataFrame(varData, columns=['perc_omicrons'])
    percentDelta = pd.DataFrame.to_numpy(percentDelta, dtype=float)
    percentOmicron = pd.DataFrame.to_numpy(percentOmicron, dtype=float)
    
    # preallocate empty lists for biweekly dates and cases
    biweeklyDates = []
    biweeklyCases = []
    n = None

    #fill in biweekly dates/cases based on starting date (Jan 11 2021)
    for i in range(len(dates[:,0])):
        j = len(dates[:,0]) - 1 - i
        if dates[j,0] == 'Jan 11 2021':
            biweeklyDates.append(dates[j,0])
            biweeklyCases.append(avgCases[j,0])
            n = j
            break
    
    for i in range(34):
        n = n - 14
        biweeklyDates.append(dates[n,0])
        biweeklyCases.append(avgCases[n,0])
    

    numDelta = []
    numOmicron = []
    for i in range(len(biweeklyDates)):
        delta = percentDelta[i,0]*biweeklyCases[i]
        numDelta.append(delta)
        omicron = percentOmicron[i,0]*biweeklyCases[i]
        numOmicron.append(omicron)
    
    
    # x = i1/ (i1 + i2)
    # y = i2/ (i1 + i2)
    x = []
    y = []
    for i in range(len(biweeklyDates)):
        entryX = numDelta[i]/biweeklyCases[i]
        x.append(entryX)
        entryY = numOmicron[i]/biweeklyCases[i]
        y.append(entryY)
        
    
    
    
    return(x, y, biweeklyCases)

"""
transition(S, I_1, I_2, R, beta_1, beta_2, gamma, theta)
INPUTS: 
initial conditions: S, I_1, I_2, R_1, R
                    float beta's, gamma, and theta 
                    (assume gamma_1 == gamma_2; beta_3 = theta*beta_2)
                    fixed pop size N
OUTPUTS: simulated transition from variant 1 to variant 2 using advnaced SIR
"""

def transition(S, I_1, I_2, R_1, R, beta_1, beta_2, gamma, theta):
    # divide by N
    s = S/N
    i_1 = I_1/N
    i_2 = I_2/N
    r_1 = R_1/N
    r = R/N
    
    # preallocate empty lists to track
    sList = []
    i_1List = []
    i_2List = []
    r_1List = []
    rList = []
    
    # append initial conditions
    sList.append(s)
    i_1List.append(i_1)
    i_2List.append(i_2)
    r_1List.append(r_1)
    rList.append(r)
    
    # incorporate ODE's and track changes in lists above
    # run 99 iterations so that final lists are length 100, can be changed in future
    for i in range(99):
        # ODE's
        ds = -s*( beta_1*i_1 + beta_2*i_2 )
        di_1 = (s*beta_1*i_1) - (gamma*i_1)
        di_2 = (s*beta_2*i_2) + (r_1*beta_2*theta*i_2) - (gamma*i_2)
        dr_1 = (gamma*i_1) - (r_1*beta_2*theta*i_2)
        dr = gamma*i_2
        
        # Tracking
        s = s + ds
        i_1 = i_1 + di_1
        i_2 = i_2 + di_2
        r_1 = r_1 + dr_1
        r = r + dr
        
        sList.append(s)
        i_1List.append(i_1)
        i_2List.append(i_2)
        r_1List.append(r_1)
        rList.append(r)
        
    
    return [sList, i_1List, i_2List, r_1List, rList]
    
    
if __name__ == "__main__":
    # let variant 1 be Delta and variant 2 be Omicron
    # input initial conditions, edit as needed
    
    N = 329000000
    I_1 = 100000
    I_2 = 1
    R_1 = 0
    R = 0
    S = N - (I_1 + I_2 + R_1 + R)
    # beta values from 0.1 to 2
    #beta_1 = [ round(0.1*i, 1) for i in range(1,21) ]
    #beta_2 = [ round(0.1*j, 1) for j in range(1,21) ]
    beta_1 = 0.5
    beta_2 = 0.9
    gamma = 0.2
    # theta values from 0 to 1
    # 0 ==> individuals in R_1 cannot be reinfected by variant 2; 
    # 1 ==> R_1 just as susceptible as S
    #theta = [ round(0.1*n, 1) for n in range(11) ]
    theta = 0.9
    
    #simResult = []
    # all beta_1 values
    #for i in range(20):
        # all beta_2 values
    #    for j in range(20):
            #all theta values
     #       for k in range(10):
     #           simResult.append(transition(S, I_1, I_2, R_1,
      #                     R, beta_1[i], beta_2[j], gamma, theta[k]))
                
    (s, i_1, i_2, r_1, r) = transition(S, I_1, I_2, 
                                       R_1, R, beta_1, beta_2, gamma, theta)
            
    
    plt.figure()
    fig, ax = plt.subplots()
    ax.plot(s, label='s')
    ax.plot(i_1, label='i_1')
    ax.plot(i_2, label='i_2')
    ax.plot(r_1, label='r_1')
    ax.plot(r, label='r')
    ax.legend(loc='upper left')
    plt.title('Reinfection Simulation')
    plt.xlabel('Time')
    plt.ylabel('% of Total Population')       
    plt.savefig('reinfectionSim.png', bbox_inches='tight')
    plt.close('all')
    
    
    
    
    
    
    
    
