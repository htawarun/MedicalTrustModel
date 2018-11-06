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
    

fQdata = []
fQerrdat = []
fQPdata = []
fQPerrdat = []
pQdata = []
pQerrdat = []
pQPdata = []
pQPerrdat = []
filenames = []
pgossvals = []
fgossvals = []

colours = ['b.-','g.-','r.-','k.-','y.-','m.-','c.-', 'ko-', 'ro-', 'bo-', 'go-', 'yo-', 'mo-']    

#friend = int(sys.argv[1])

#public = int(sys.argv[2])

# get data from files and put into lists
    
for i in range(1, len(sys.argv), 2):
#for i in range(3, len(sys.argv),2):    
    filename = sys.argv[i]
    filenames.append(filename)
    
    gossval = float(sys.argv[i+1])

    
    varnames, timesteps, data = read_data(filename)
    
    print(filename)
    
    halfindex = int(np.ma.size(data[:,1])/2) -1
    lastindex = np.ma.size(data[:,1]) -1
    endQs = data[:,1][halfindex:lastindex]
    endQPs = data[:,2][halfindex:lastindex]    
    
    if i < (len(sys.argv)+1)/2:
    #if i<3+2*friend:
        fgossvals.append(gossval)
        
        fQdata.append(np.mean(endQs))
        fQerrdat.append(np.std(endQs)/math.sqrt(np.ma.size(endQs)))
        
        fQPdata.append(np.mean(endQPs))
        fQPerrdat.append(np.std(endQPs)/math.sqrt(np.ma.size(endQPs)))
    else:
        pgossvals.append(gossval)
        
        pQdata.append(np.mean(endQs))
        pQerrdat.append(np.std(endQs)/math.sqrt(np.ma.size(endQs)))
        
        pQPdata.append(np.mean(endQPs))
        pQPerrdat.append(np.std(endQPs)/math.sqrt(np.ma.size(endQPs)))

# plot qualities over gossip weights
plt.errorbar(fgossvals, fQPdata, yerr = fQPerrdat, fmt = 'b-', capsize = 2, label = "friendly")
plt.errorbar(pgossvals, pQPdata, yerr = pQPerrdat, fmt = 'g-', capsize = 2, label = "public")
plt.title("Quality-price vs Gossip Weight")
plt.legend()
plt.xlabel("Gossip Weight")
plt.ylabel("Q-P")
plt.savefig("QPvsG")
plt.clf()

plt.errorbar(fgossvals, fQdata, yerr = fQerrdat, fmt = 'b-', capsize = 2, label = "friendly")
plt.errorbar(pgossvals, pQdata, yerr = pQerrdat, fmt = 'g-', capsize = 2, label = "public")
plt.title("Quality vs Gossip Weight")
plt.legend()
plt.xlabel("Gossip Weight")
plt.ylabel("Q")
plt.savefig("QvsG")
plt.clf()

    
