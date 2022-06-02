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
    cases = pd.read_csv('casesNC.csv')
    var = pd.read_csv('varNC.csv')
    
    # specify columns, convert to numpy
    casesDates = pd.DataFrame(cases, columns=['date'])
    dailyCases = pd.DataFrame(cases, columns=['nc_case_day'])
    casesDates = pd.DataFrame.to_numpy(casesDates, dtype=str)
    cases = pd.DataFrame.to_numpy(dailyCases, dtype=int)
    
    percAlpha = pd.DataFrame(var, columns=['percAlpha'])
    percOther = pd.DataFrame(var, columns=['percOthers'])
    percDelta = pd.DataFrame(var, columns=['percDelta'])
    percB11529 = pd.DataFrame(var, columns=['percB.1.1.529'])
    percBA11 = pd.DataFrame(var, columns=['percBA.1.1'])
    percBA2 = pd.DataFrame(var, columns=['percBA.2'])
    percBA2121 = pd.DataFrame(var, columns=['percBA.2.12.1'])
    
    alpha = pd.DataFrame.to_numpy(percAlpha, dtype=float)
    other = pd.DataFrame.to_numpy(percOther, dtype=float)
    delta = pd.DataFrame.to_numpy(percDelta, dtype=float)
    B11529 = pd.DataFrame.to_numpy(percB11529, dtype=float)
    BA11 = pd.DataFrame.to_numpy(percBA11, dtype=float)
    BA2 = pd.DataFrame.to_numpy(percBA2, dtype=float)
    BA2121 = pd.DataFrame.to_numpy(percBA2121, dtype=float)
    
    

    # to create new list of weekly NC cases
    n = None
    for i in range(len(casesDates)):
        if casesDates[i,0] == '2021-07-03':
            n = i

    weeklyCases = []
    week = 0
    # 34 weeks
    for i in range(44):
        # aggregating cases from each day of the week
        for j in range(7):
            week = week + cases[n - j, 0]
            
        weeklyCases.append(week)
        week = 0
        n = n + 7
        
    # calc # of cases by variant
    
    numAlpha = []
    numOther = []
    numDelta = []
    numB11529 = []
    numBA11 = []
    numBA2 = []
    numBA2121 = []
    
    
    for i in range(len(alpha)):
        
        alphaEntry = alpha[i,0]*weeklyCases[i]
        numAlpha.append(alphaEntry)
        
        otherEntry = other[i,0]*weeklyCases[i]
        numOther.append(otherEntry)
        
        deltaEntry = delta[i,0]*weeklyCases[i]
        numDelta.append(deltaEntry)
        
        B11529Entry = B11529[i,0]*weeklyCases[i]
        numB11529.append(B11529Entry)
        
        BA11Entry = BA11[i,0]*weeklyCases[i]
        numBA11.append(BA11Entry)
        
        BA2Entry = BA2[i,0]*weeklyCases[i]
        numBA2.append(BA2Entry)
        
        BA2121Entry = BA2121[i,0]*weeklyCases[i]
        numBA2121.append(BA2121Entry)
        
        
    
    plt.figure()
    fig, ax = plt.subplots()
    ax.plot(numAlpha, label='Alpha')
    ax.plot(numDelta, label='Delta')
    ax.plot(numB11529, label='B.1.1.529')
    ax.plot(numBA11, label='BA.1.1')
    ax.plot(numBA2, label='BA.2')
    ax.plot(numBA2121, label='BA.2.12.1')
    ax.plot(numOther, label='Other')
    ax.legend(loc='upper left')
    plt.title('Cases by Variant, NC')
    plt.xlabel('Time (Weekly)')
    plt.ylabel('# of Cases')       
    plt.savefig('casesByVarNC.png', bbox_inches='tight')
    plt.close('all')
    
    
    
    plt.figure()
    fig, ax = plt.subplots()
    ax.plot(alpha[:,0], label='Alpha')
    ax.plot(other[:,0], label='Other')
    ax.plot(delta[:,0], label='Delta')
    ax.plot(B11529[:,0], label='BA.1.1.529')
    ax.plot(BA11[:,0], label='BA.1.1')
    ax.plot(BA2[:,0], label='BA.2')
    ax.plot(BA2121[:,0], label='BA.2.12.1')
    ax.legend(loc='upper left')
    plt.title('Variant Percentages, NC')
    plt.xlabel('Time (Weekly)')
    plt.ylabel('% of Cases')       
    plt.savefig('varPercNC.png', bbox_inches='tight')
    plt.close('all')
    
    
   
    return
    
    
    
if __name__ == '__main__':
    calcCasesByVariant()
