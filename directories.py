#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 17:33:38 2018

@author: s1457132
"""

import os

os.mkdir(str(0.0))
stdinput = open(str(0.0)+"/standard_input", "w")

vals = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

fileline1 = "Trust model type: b \n"
fileline2 = "Trust weight: 0.0 \n"
fileline3 = "Gossip mode: 0 \n" 
fileline4 ="Gossip weight: 0.5 \n"
fileline5 = "Gossip range: 2 \n"
fileline6 = "Runs: 20 \nSteps: 400 \nPatients: 1000 \nRetailers: 100 \nSuppliers: 10 \n"
fileline7 = "Standard distance: 0.02 \nMinimum lifetime: 4 "

filelines = fileline1+fileline2+fileline3+fileline4+fileline5+fileline6

#fileline3f = "Gossip mode: f \n"
#fileline3p = "Gossip mode: p \n"

stdinput.write(filelines)
stdinput.close()

for i in vals:
    #os.mkdir(str(i)+"F")
    #os.mkdir(str(i)+"P")
    os.mkdir(str(i)+"noG")
    
    #fileline3 = "Gossip weight: " + str(i) + " \n"
    fileline2 = "Trust weight: " + str(i) + " \n" 
    
    #stdinputF = open(str(i)+"F/standard_input", "w")
    #stdinputP = open(str(i)+"P/standard_input", "w")
    stdinput = open(str(i)+"noG/standard_input", "w")
    
    #filelinesF = fileline1 + fileline2f + fileline3 + fileline4 + fileline5 + fileline6
    #filelinesP = fileline1 + fileline2p + fileline3 + fileline4 + fileline5 + fileline6
    filelines = fileline1+fileline2+fileline3+fileline4+fileline5+fileline6
    
    #stdinputF.write(filelinesF)
    #stdinputP.write(filelinesP)
    stdinput.write(filelines)
    
    #stdinputF.close()
    #stdinputP.close()
    stdinput.close()
    
