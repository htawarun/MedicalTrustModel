#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 15:12:57 2018

@author: Cara
"""

import numpy as np
import os
import matplotlib.pyplot as plt
import sys
import math

def read_data(infile):
    with open(infile,"rt") as Infile:
        lines = Infile.readlines()
        width = len(lines[1].split(',')) - 1
        length = len(lines) - 1
        
        varnames = lines[0].split(",")
        data = np.zeros((length,width))
        timesteps = np.zeros(length)
        
        for i in range(1, len(lines)):
            linetokens = lines[i].split(',')
            timesteps[i-1] = linetokens[0]
            for n in range(1, len(linetokens)):
                data[i-1,n-1] = float(linetokens[n])
        return varnames, timesteps, data
    
allvarnames = []
alltimesteps = []
alldata = []
filenames = []

colours = ['b.-','g.-','r.-','k.-','y.-','m.-','c.-', 'ko-', 'ro-', 'bo-', 'go-', 'yo-', 'mo-']    
    
for i in range(1, len(sys.argv)):
    filename = sys.argv[i]
    filenames.append(filename)
    varnames, timesteps, data = read_data(filename)
    
    print(filename)
    
    allvarnames.append(varnames)
    alltimesteps.append(timesteps)
    alldata.append(data)

for i in range(0, np.ma.size(data, 1)):
    name = (varnames[i+1]).strip('\n')
    for j in range(0, len(filenames)):
        plt.plot(alltimesteps[j], alldata[j][:,i], colours[j], label = filenames[j])
    plt.title(name + " over time")
    plt.xlabel("Step number")
    plt.ylabel(name)
    plt.legend()
    plt.savefig(name + ".png")
    plt.clf()
    
