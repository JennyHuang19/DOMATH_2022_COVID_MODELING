"""
5/23/22
June Lee
"""

import math
import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt

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
    percentBA45 = pd.DataFrame(varData, columns=['perc_ba45'])
    percentDelta = pd.DataFrame.to_numpy(percentDelta, dtype=float)
    percentOmicron = pd.DataFrame.to_numpy(percentOmicron, dtype=float)
    percentBA45 = pd.DataFrame.to_numpy(percentBA45, dtype=float)
    
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
    numBA45 = []
    for i in range(len(biweeklyDates)):
        delta = percentDelta[i,0]*biweeklyCases[i]
        numDelta.append(delta)
        omicron = percentOmicron[i,0]*biweeklyCases[i]
        numOmicron.append(omicron)
        BA45 = percentBA45[i,0]*biweeklyCases[i]
        numBA45.append(BA45)
        
        
    finalTable = [['Dates', '# of Delta', '# of Omicron', '# of Total Cases']]
    
    
    # x = i1/ (i1 + i2 + i3)
    # y = i2/ (i1 + i2 + i3)
    # z = i3/ (i1 + i2 + i3)
    
    x = []
    y = []
    z = []
    for i in range(len(biweeklyDates)):
        entryX = numDelta[i]/biweeklyCases[i]
        x.append(entryX)
        entryY = numOmicron[i]/biweeklyCases[i]
        y.append(entryY)
        entryZ = numBA45[i]/biweeklyCases[i]
        z.append(entryZ)
        
    
    
    
    return(x, y, z, biweeklyCases, numDelta, numOmicron, numBA45)

if __name__ == '__main__':
    (x, y, z, biweeklyCases, numDelta, numOmicron, numBA45) = calcCasesByVariant()

    plt.figure()
    fig, ax = plt.subplots()
    ax.plot(x, label='Delta')
    ax.plot(y, label='Omicron')
    ax.plot(z, label='BA45')
    ax.legend(loc='upper left')
    plt.title('Delta to Omicron to BA45 Transition')
    plt.xlabel('Time (Biweekly)')
    plt.ylabel('% of Cases')       
    plt.savefig('DeltaOmicronBA45percentage.png', bbox_inches='tight')
    plt.close('all')
    
