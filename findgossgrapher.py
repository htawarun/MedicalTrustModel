#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created Sat Nov 10 15:56 2018

@author: s1457132

"""

import numpy as np
import os
import matplotlib.pyplot as plt
import sys
import math

        
def read_data(infile):
    """
    Reads files and puts data into arrays.
    The files would have the timesteps in the first column and the retailer indices in the first row
    
    :param infile: string name of file to read
    :return timesteps: numpy array of timesteps 
    :return data: numpy array of data
    """
    with open(infile, "rt") as Infile:
        
        lines = Infile.readlines()
        width = len(lines[1].split(',')) - 1
        length = len(lines) - 1
        
        data = np.zeros((length,width))
        timesteps = np.zeros(length)
        
        for i in range(1, length+1):
            linetokens = lines[i].split(',')
            timesteps[i-1] = linetokens[0]
            for n in range(1, len(linetokens)):
                data[i-1,n-1] = float(linetokens[n])
        return timesteps, data
def individualruns(directory):
    rungossdata = []
    for subdirectory in os.listdir(directory):
	if os.path.isdir(directory + "/" + subdirectory):
	    if os.path.exists(directory + "/" + subdirectory + "/PatientQualities.csv"):
		if len(subdirectory) == 3:
		    Gmode = "0"
		    Gweight = 0.0
		else:
		    Gmode = subdirectory[0]
		    Gweight = float(subdirectory[1:])

		ptimesteps, patient_price = read_data(directory + "/" + subdirectory + "/PatientPrices.csv")
		ptimesteps, patient_quality = read_data(directory + "/" + subdirectory + "/PatientQualities.csv")
		
		prunlist = [ptimesteps, patient_price, patient_quality]
		
		rtimesteps, retailer_price = read_data(directory + "/" + subdirectory + "/RetailerPrices.csv")
		rtimesteps, retailer_quality = read_data(directory + "/" + subdirectory + "/RetailerQualities.csv")
		
		rrunlist = [rtimesteps, retailer_price, retailer_quality]
		
		stimesteps, supplier_price = read_data(directory + "/" + subdirectory + "/SupplierPrices.csv")
		stimesteps, supplier_quality = read_data(directory + "/" + subdirectory + "/SupplierQualities.csv")
		
		srunlist = [stimesteps, supplier_price, supplier_quality]
		
		gossvaldata = [Gmode, Gweight, prunlist, rrunlist, srunlist]
		
		rungossdata.append(gossvaldata)
	    
    return rungossdata
		
def allruns():
    allrunsdata = []
    runs = []
    for directories in os.listdir("."):
	if os.path.isdir(directories):
	    rundat = individualruns(directories)
	    allrunsdata.append(rundat)
	    runs.append(directories)
	
    return allrunsdata, runs

def QvsG(allrunsdata, runs):
    os.mkdir("PlotData")
    # plot for each run
    foundfirst = False
    for i in range(0, len(allrunsdata)):
	rundata = allrunsdata[i]
	runname = runs[i]
	runfGweights = []
	runpGweights = []	
	runfPs = []
	runfQs = []
	runpPs = []
	runpQs = []
	
	for gossvaldata in rundata:
	    gmode = gossvaldata[0]
	    gweight = gossvaldata[1]
	    prunlist = gossvaldata[2]
	    
	    qualities = prunlist[2]
	    prices = prunlist[1]
	    
	    stepnumber = np.ma.size(qualities, 0)
	    laststepsstart = stepnumber - int(stepnumber/5)
	    
	    lastQs = qualities[laststepsstart:]
	    lastPs = prices[laststepsstart:]
	    
	    meanQs = np.zeros(np.ma.size(lastQs,0))
	    meanPs = np.zeros(np.ma.size(lastPs, 0))
	    
	    for i in range(0,np.ma.size(meanQs)):
		meanQs[i] = np.mean(lastQs)
		meanPs[i] = np.mean(lastPs)
	    
	    Q = np.mean(meanQs)
	    P = np.mean(meanPs)
	    
	    if gmode == "f" or gmode == "0":
		
		runfGweights.append(gweight)
		runfPs.append(P)
		runfQs.append(Q)
	    
	    if gmode == "p" or gmode == "0":
		runpGweights.append(gweight)
		runpPs.append(P)
		runpQs.append(Q)
		
	    if gweight == 0.0:
		nogossQ = Q
		nogossP = P
	
	sortedfQs = [x for _,x in sorted(zip(runfGweights,runfQs))]
	sortedfGweights = sorted(runfGweights)
	
	sortedpQs = [x for _,x in sorted(zip(runpGweights,runpQs))]
	sortedpGweights = sorted(runpGweights)
	

	
	plt.plot(sortedfGweights, sortedfQs, "b-", label = "friendly")
	plt.plot(sortedpGweights, sortedpQs, "g-", label = "public")
	plt.title("Quality vs Gossip Weight")
	plt.legend()
	plt.xlabel("Gossip Weight")
	plt.ylabel("Quality")
	plt.savefig("PlotData/" + runname + "QvsG.png")
	plt.clf()
	
	sortedfPs = [x for _,x in sorted(zip(runfGweights,runfPs))]
	sortedpPs = [x for _,x in sorted(zip(runpGweights,runpPs))]
	plt.plot(sortedfGweights, sortedfPs, "b-", label = "friendly")
	plt.plot(sortedpGweights, sortedpPs, "g-", label = "public")
	plt.title("Price vs Gossip Weight")
	plt.legend()
	plt.xlabel("Gossip Weight")
	plt.ylabel("Price")
	plt.savefig("PlotData/" + runname + "PvsG.png")
	plt.clf()
	
	fP = np.array(sortedfPs)
	pP = np.array(sortedpPs)
	fQ = np.array(sortedfQs)
	pQ = np.array(sortedpQs)
	fW = np.array(sortedfGweights)
	pW = np.array(sortedpGweights)
	
	fQP = np.divide(fQ, fP)
	pQP = np.divide(pQ, pP)
	
	fI = fQ/nogossQ
	pI = pQ/nogossQ
	
	fPI = fP/nogossP
	pPI = pP/nogossP
	
	if not foundfirst:
	    fIdata = fI
	    pIdata = pI
	    
	    pPIdata = pPI
	    fPIdata = fPI
	    foundfirst = True
	else:

	    fIdata = np.vstack((fI, fIdata))
	    pIdata = np.vstack((pI, pIdata))
	    
	    pPIdata = np.vstack((pPI, pPIdata))
	    fPIdata = np.vstack((fPI, fPIdata))
	
    meanfI = np.empty(np.ma.size(fIdata,1))
    errfI = np.empty(np.ma.size(fIdata,1))
    meanpI = np.empty(np.ma.size(pIdata,1))
    errpI = np.empty(np.ma.size(pIdata,1))
    
    meanfPI = np.empty(np.ma.size(fPIdata,1))
    errfPI = np.empty(np.ma.size(fPIdata,1))
    meanpPI = np.empty(np.ma.size(pPIdata,1))
    errpPI = np.empty(np.ma.size(pPIdata,1))
    
    for i in range(0,np.ma.size(fIdata,1)):
	meanfI[i] = np.mean(fIdata[:,i])
	errfI[i] = np.std(fIdata[:,i])/math.sqrt(np.ma.size(fIdata,0))
	meanpI[i] =np.mean(pIdata[:,i])
	errpI[i] = np.std(pIdata[:,i])/math.sqrt(np.ma.size(pIdata,0))
	
	meanfPI[i] = np.mean(fPIdata[:,i])
	errfPI[i] = np.std(fPIdata[:,i])/math.sqrt(np.ma.size(fPIdata,0))
	meanpPI[i] =np.mean(pPIdata[:,i])
	errpPI[i] = np.std(pPIdata[:,i])/math.sqrt(np.ma.size(pPIdata,0))

    
    plt.errorbar(fW, meanfI, yerr = errfI, fmt = "b.", capsize = 2, label = "friendly")
    plt.errorbar(pW, meanpI, yerr = errpI, fmt = "g.", capsize = 2, label = "public")
    plt.title("Quality Improvement vs Gossip Weight")
    plt.legend()
    plt.xlabel("Gossip Weight")
    plt.ylabel("Improvement")
    plt.savefig("PlotData/IvsG")
    plt.clf()
    
    
    plt.errorbar(fW, meanfPI, yerr = errfPI, fmt = "b.", capsize = 2, label = "friendly")
    plt.errorbar(pW, meanpPI, yerr = errpPI, fmt = "g.", capsize = 2, label = "public")
    plt.title("Price Improvement vs Gossip Weight")
    plt.legend()
    plt.xlabel("Gossip Weight")
    plt.ylabel("Price Improvement")
    plt.savefig("PlotData/PIvsG")
    plt.clf()
    
    
	    

data, runs = allruns()
QvsG(data, runs)


    				
				
			
