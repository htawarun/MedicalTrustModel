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
		"""
		if len(subdirectory) == 13:
		    Gmode = "0"
		    Gweight = 0.0
		else:
		    Gmode = subdirectory[13]
		    Gweight = float(subdirectory[11:])
		    
		Pweight = float(subdirectory[1:3])
		Tweight = float(subdirectory[5:7])
		"""

		ptimesteps, patient_price = read_data(directory + "/" + subdirectory + "/PatientPrices.csv")
		ptimesteps, patient_quality = read_data(directory + "/" + subdirectory + "/PatientQualities.csv")
		
		prunlist = [ptimesteps, patient_price, patient_quality]
		
		rtimesteps, retailer_price = read_data(directory + "/" + subdirectory + "/RetailerPrices.csv")
		rtimesteps, retailer_quality = read_data(directory + "/" + subdirectory + "/RetailerQualities.csv")
		
		rrunlist = [rtimesteps, retailer_price, retailer_quality]
		
		stimesteps, supplier_price = read_data(directory + "/" + subdirectory + "/SupplierPrices.csv")
		stimesteps, supplier_quality = read_data(directory + "/" + subdirectory + "/SupplierQualities.csv")
		stimesteps, supplier_inventory = read_data(directory +  "/" + subdirectory + "/SupplierInventories.csv")
		
		srunlist = [stimesteps, supplier_price, supplier_quality, supplier_inventory]
		
		valsdata = [subdirectory, prunlist, rrunlist, srunlist]
		
		rungossdata.append(valsdata)
	    
    return rungossdata
		
def allruns():
    allrunsdata = []
    runs = []
    for directories in os.listdir("."):
	if os.path.isdir(directories) and directories != "PlotData":
	    rundat = individualruns(directories)
	    allrunsdata.append(rundat)
	    runs.append(directories)
	
    return allrunsdata, runs

def Qvstime(allrunsdata, runs):


    foundfirstP = False
    foundfirstT = False
    foundfirstGf = False
    foundfirstGp = False
    foundfirstGTf = False
    foundfirstGTp = False
    
    for i in range(0, len(allrunsdata)):
	rundata = allrunsdata[i]
	runname = runs[i]
	
	for gossvaldata in rundata:
	    name = gossvaldata[0]
	    
	    prunlist = gossvaldata[1]
	    
	    qualities = prunlist[2]
	    prices = prunlist[1]
	    ptimesteps = prunlist[0]
	    
	    meanQs = np.zeros(np.ma.size(qualities,0))
	    meanPs = np.zeros(np.ma.size(prices, 0))
	    
	    rrunlist = gossvaldata[2]
	    
	    rtimesteps = rrunlist[0]
	    rprices = rrunlist[1]
	    rqualities = rrunlist[2]
	    
	    rmeanQs = np.zeros(np.ma.size(rqualities,0))
	    rmeanPs = np.zeros(np.ma.size(rprices,0))
	    
	    srunlist = gossvaldata[3]
	    
	    stimesteps = srunlist[0]
	    sinventories = srunlist[3]
	    
	    for i in range(0,np.ma.size(meanQs)):
		meanQs[i] = np.mean(qualities[i,:])
		meanPs[i] = np.mean(prices[i,:])
	    
	    for j in range(0, np.ma.size(rmeanQs)):
		rmeanQs[j] = np.mean(rqualities[j,:])
		rmeanPs[j] = np.mean(rprices[j,:])
		
	    if name == "P0.0T0.0G10.0f":
		if not foundfirstGf:
		    fGQs = meanQs
		    fGPs = meanPs
		    
		    rfGQs = rmeanQs
		    rfGPs = rmeanPs
		    
		    allGfinvs = sinventories
		    foundfirstGf = True
		else:
		    fGQs = np.vstack((meanQs, fGQs))
		    fGPs = np.vstack((meanPs, fGPs))
		    
		    rfGQs = np.vstack((rmeanQs, rfGQs))
		    rfGPs = np.vstack((rmeanPs, rfGPs))
		    
		    allGfinvs += sinventories
		    
	    elif name == "P0.0T0.0G10.0p":
		if not foundfirstGp:
		    pGQs = meanQs
		    pGPs = meanPs
		    rpGQs = rmeanQs
		    rpGPs = rmeanPs
		    
		    allGpinvs = sinventories
		    
		    foundfirstGp = True
		else:
		    pGQs = np.vstack((meanQs, pGQs))
		    pGPs = np.vstack((meanPs, pGPs))
		    
		    rpGQs = np.vstack((rmeanQs, rpGQs))
		    rpGPs = np.vstack((rmeanPs, rpGPs))
		    
		    allGpinvs += sinventories
	    elif name == "P0.0T10.0G0.0":
		if not foundfirstT:
		    TQs = meanQs
		    TPs = meanPs
		    
		    rTQs = rmeanQs
		    rTPs = rmeanPs
		    
		    allTinvs = sinventories
		    
		    foundfirstT = True
		else:
		    TQs = np.vstack((meanQs, TQs))
		    TPs = np.vstack((meanPs, TPs))
		    rTQs = np.vstack((rmeanQs, rTQs))
		    rTPs = np.vstack((rmeanPs, rTPs))
		    
		    allTinvs += sinventories
		    		    
	    elif name == "P1.0T0.0G0.0":
		if not foundfirstP:
		    PQs = meanQs
		    PPs = meanPs
		    
		    rPQs = rmeanQs
		    rPPs = rmeanPs
		    
		    allPinvs = sinventories
		    
		    foundfirstP = True
		else:
		    PQs = np.vstack((meanQs, PQs))
		    PPs = np.vstack((meanPs, PPs))
		    
		    rPQs = np.vstack((rmeanQs, rPQs))
		    rPPs = np.vstack((rmeanPs, rPPs))
		    
		    allPinvs += sinventories
	    elif name == "P0.0T10.0G10.0f":
		if not foundfirstGTf:
		    fGTQs = meanQs
		    fGTPs = meanPs
		    
		    rfGTQs = rmeanQs
		    rfGTPs = rmeanPs
		    
		    allGTfinvs = sinventories
		    foundfirstGTf = True
		else:
		    fGTQs = np.vstack((meanQs, fGTQs))
		    fGTPs = np.vstack((meanPs, fGTPs))
		    
		    rfGTQs = np.vstack((rmeanQs, rfGTQs))
		    rfGTPs = np.vstack((rmeanPs, rfGTPs))
		    
		    allGTfinvs += sinventories
		    
	    elif name == "P0.0T10.0G10.0p":
		if not foundfirstGTp:
		    
		    pGTQs = meanQs
		    pGTPs = meanPs
		    rpGTQs = rmeanQs
		    rpGTPs = rmeanPs
		    
		    allGTpinvs = sinventories
		    
		    foundfirstGTp = True
		
		else:
		    pGTQs = np.vstack((meanQs, pGTQs))
		    pGTPs = np.vstack((meanPs, pGTPs))
		    
		    rpGTQs = np.vstack((rmeanQs, rpGTQs))
		    rpGTPs = np.vstack((rmeanPs, rpGTPs))
		    
		    allGTpinvs += sinventories
    
    # normalise supplier inventories
    allPinvs = allPinvs/len(allrunsdata)
    allTinvs = allTinvs/len(allrunsdata)
    allGfinvs = allGfinvs/len(allrunsdata)
    allGpinvs = allGpinvs/len(allrunsdata)
    allGTfinvs = allGTfinvs/len(allrunsdata)
    allGTpinvs = allGTpinvs/len(allrunsdata)
    
    #trust
    TmeanQs = np.empty(np.ma.size(ptimesteps))
    TerrorQs = np.empty(np.ma.size(ptimesteps))
    TmeanPs = np.empty(np.ma.size(ptimesteps))
    TerrorPs = np.empty(np.ma.size(ptimesteps))
    
    #price
    PmeanQs = np.empty(np.ma.size(ptimesteps))
    PerrorQs = np.empty(np.ma.size(ptimesteps))
    PmeanPs = np.empty(np.ma.size(ptimesteps))
    PerrorPs = np.empty(np.ma.size(ptimesteps))
    
    #gossip
    fGmeanQs = np.empty(np.ma.size(ptimesteps))
    fGerrorQs = np.empty(np.ma.size(ptimesteps))
    fGmeanPs = np.empty(np.ma.size(ptimesteps))
    fGerrorPs = np.empty(np.ma.size(ptimesteps))
    pGmeanQs = np.empty(np.ma.size(ptimesteps))
    pGerrorQs = np.empty(np.ma.size(ptimesteps))
    pGmeanPs = np.empty(np.ma.size(ptimesteps))
    pGerrorPs = np.empty(np.ma.size(ptimesteps))
    
    #gossip+trust
    fGTmeanQs = np.empty(np.ma.size(ptimesteps))
    fGTerrorQs = np.empty(np.ma.size(ptimesteps))
    fGTmeanPs = np.empty(np.ma.size(ptimesteps))
    fGTerrorPs = np.empty(np.ma.size(ptimesteps))
    pGTmeanQs = np.empty(np.ma.size(ptimesteps))
    pGTerrorQs = np.empty(np.ma.size(ptimesteps))
    pGTmeanPs = np.empty(np.ma.size(ptimesteps))
    pGTerrorPs = np.empty(np.ma.size(ptimesteps))    
    
    #rtrust
    rTmeanQs = np.empty(np.ma.size(rtimesteps))
    rTerrorQs = np.empty(np.ma.size(rtimesteps))
    rTmeanPs = np.empty(np.ma.size(rtimesteps))
    rTerrorPs = np.empty(np.ma.size(rtimesteps))
    
    #rprice
    rPmeanQs = np.empty(np.ma.size(rtimesteps))
    rPerrorQs = np.empty(np.ma.size(rtimesteps))
    rPmeanPs = np.empty(np.ma.size(rtimesteps))
    rPerrorPs = np.empty(np.ma.size(rtimesteps))
    
    #rgossip
    rfGmeanQs = np.empty(np.ma.size(rtimesteps))
    rfGerrorQs = np.empty(np.ma.size(rtimesteps))
    rfGmeanPs = np.empty(np.ma.size(rtimesteps))
    rfGerrorPs = np.empty(np.ma.size(rtimesteps))
    rpGmeanQs = np.empty(np.ma.size(rtimesteps))
    rpGerrorQs = np.empty(np.ma.size(rtimesteps))
    rpGmeanPs = np.empty(np.ma.size(rtimesteps))
    rpGerrorPs = np.empty(np.ma.size(rtimesteps))  
    
    #rgossip + trust
    rfGTmeanQs = np.empty(np.ma.size(rtimesteps))
    rfGTerrorQs = np.empty(np.ma.size(rtimesteps))
    rfGTmeanPs = np.empty(np.ma.size(rtimesteps))
    rfGTerrorPs = np.empty(np.ma.size(rtimesteps))
    rpGTmeanQs = np.empty(np.ma.size(rtimesteps))
    rpGTerrorQs = np.empty(np.ma.size(rtimesteps))
    rpGTmeanPs = np.empty(np.ma.size(rtimesteps))
    rpGTerrorPs = np.empty(np.ma.size(rtimesteps))   
    
    print(len(allrunsdata))
    
    for i in range(0,np.ma.size(ptimesteps)):
	TmeanQs[i] = np.mean(TQs[:,i])
	TerrorQs[i] = np.std(TQs[:,i])/math.sqrt(len(allrunsdata))
	TmeanPs[i] = np.mean(TPs[:,i])
	TerrorPs[i] = np.std(TPs[:,i])/math.sqrt(len(allrunsdata))
	
	PmeanQs[i] = np.mean(PQs[:,i])
	PerrorQs[i] = np.std(PQs[:,i])/math.sqrt(len(allrunsdata))
	PmeanPs[i] = np.mean(PPs[:,i])
	PerrorPs[i] = np.std(PPs[:,i])/math.sqrt(len(allrunsdata))
	
	fGmeanQs[i] = np.mean(fGQs[:,i])
	fGerrorQs[i] = np.std(fGQs[:,i])/math.sqrt(len(allrunsdata))
	fGmeanPs[i] = np.mean(fGPs[:,i])
	fGerrorPs[i] = np.std(fGPs[:,i])/math.sqrt(len(allrunsdata))
	pGmeanQs[i] = np.mean(pGQs[:,i])
	pGerrorQs[i] = np.std(pGQs[:,i])/math.sqrt(len(allrunsdata))
	pGmeanPs[i] = np.mean(pGPs[:,i])
	pGerrorPs[i] = np.std(pGPs[:,i])/math.sqrt(len(allrunsdata))
	
	fGTmeanQs[i] = np.mean(fGTQs[:,i])
	fGTerrorQs[i] = np.std(fGTQs[:,i])/math.sqrt(len(allrunsdata))
	fGTmeanPs[i] = np.mean(fGTPs[:,i])
	fGTerrorPs[i] = np.std(fGTPs[:,i])/math.sqrt(len(allrunsdata))
	pGTmeanQs[i] = np.mean(pGTQs[:,i])
	pGTerrorQs[i] = np.std(pGTQs[:,i])/math.sqrt(len(allrunsdata))
	pGTmeanPs[i] = np.mean(pGTPs[:,i])
	pGTerrorPs[i] = np.std(pGTPs[:,i])/math.sqrt(len(allrunsdata))	
	

    for j in range(0,np.ma.size(rtimesteps)):
	rTmeanQs[j] = np.mean(rTQs[:,j])
	rTerrorQs[j] = np.std(rTQs[:,j])/math.sqrt(len(allrunsdata))
	rTmeanPs[j] = np.mean(rTPs[:,j])
	rTerrorPs[j] = np.std(rTPs[:,j])/math.sqrt(len(allrunsdata))
	
	rPmeanQs[j] = np.mean(rPQs[:,j])
	rPerrorQs[j] = np.std(rPQs[:,j])/math.sqrt(len(allrunsdata))
	rPmeanPs[j] = np.mean(rPPs[:,j])
	rPerrorPs[j] = np.std(rPPs[:,j])/math.sqrt(len(allrunsdata))
	
	rfGmeanQs[j] = np.mean(rfGQs[:,j])
	rfGerrorQs[j] = np.std(rfGQs[:,j])/math.sqrt(len(allrunsdata))
	rfGmeanPs[j] = np.mean(rfGPs[:,j])
	rfGerrorPs[j] = np.std(rfGPs[:,j])/math.sqrt(len(allrunsdata))
	rpGmeanQs[j] = np.mean(rpGQs[:,j])
	rpGerrorQs[j] = np.std(rpGQs[:,j])/math.sqrt(len(allrunsdata))
	rpGmeanPs[j] = np.mean(rpGPs[:,j])
	rpGerrorPs[j] = np.std(rpGPs[:,j])/math.sqrt(len(allrunsdata))
	
	rfGTmeanQs[j] = np.mean(rfGTQs[:,j])
	rfGTerrorQs[j] = np.std(rfGTQs[:,j])/math.sqrt(len(allrunsdata))
	rfGTmeanPs[j] = np.mean(rfGTPs[:,j])
	rfGTerrorPs[j] = np.std(rfGTPs[:,j])/math.sqrt(len(allrunsdata))
	rpGTmeanQs[j] = np.mean(rpGTQs[:,j])
	rpGTerrorQs[j] = np.std(rpGTQs[:,j])/math.sqrt(len(allrunsdata))
	rpGTmeanPs[j] = np.mean(rpGTPs[:,j])
	rpGTerrorPs[j] = np.std(rpGTPs[:,j])/math.sqrt(len(allrunsdata))


    """
    os.mkdir("PlotData")
    
    plt.errorbar(ptimesteps, TmeanQs, yerr = TerrorQs, color = "#FF0000", marker = '.', linestyle = 'none', capsize = 2, label = "trust on")
    plt.errorbar(ptimesteps, PmeanQs, yerr = PerrorQs, color = "#000000", capsize = 2, marker = '.', linestyle = 'none', label = "price on")
    plt.errorbar(ptimesteps, fGmeanQs, yerr = fGerrorQs, color = "#002BFF", capsize = 2, linestyle = 'none', marker = '.', label = "friendly gossip on")
    plt.errorbar(ptimesteps, pGmeanQs, yerr = pGerrorQs, color = "#0F8934", capsize = 2, linestyle = 'none', marker = '.', label = "public gossip on") 
    plt.errorbar(ptimesteps, fGTmeanQs, yerr = fGTerrorQs, color = "#21DEED", capsize = 2,  linestyle = 'none', marker = '.',label = "friendly gossip and trust on")
    plt.errorbar(ptimesteps, pGTmeanQs, yerr = pGTerrorQs, color = "#03F703", capsize = 2, linestyle = 'none', marker = '.', label = "public gossip and trust on")  
    plt.title("Quality over time")
    plt.legend()
    plt.xlabel("Step number")
    plt.ylabel("Quality")
    #plt.yscale("log")
    plt.savefig("PlotData/Qvstime")
    plt.clf()
    
    plt.errorbar(ptimesteps, TmeanPs, yerr = TerrorPs, color = "#FF0000", linestyle = 'none', marker = '.', capsize = 2, label = "trust on")
    plt.errorbar(ptimesteps, PmeanPs, yerr = PerrorPs, color = "#000000", linestyle = 'none', marker = '.', capsize = 2, label = "price on")
    plt.errorbar(ptimesteps, fGmeanPs, yerr = fGerrorPs, color = "#002BFF", linestyle = 'none', marker = '.', capsize = 2, label = "friendly gossip on")
    plt.errorbar(ptimesteps, pGmeanPs, yerr = pGerrorPs, color = "#0F8934", linestyle = 'none', marker = '.', capsize = 2, label = "public gossip on") 
    plt.errorbar(ptimesteps, fGTmeanPs, yerr = fGTerrorPs, color = "#21DEED", linestyle = 'none', marker = '.', capsize = 2, label = "friendly gossip and trust on")
    plt.errorbar(ptimesteps, pGTmeanPs, yerr = pGTerrorPs, color = "#03F703", linestyle = 'none', marker = '.', capsize = 2, label = "public gossip and trust on")  
    plt.title("Price over time")
    plt.legend()
    plt.xlabel("Step number")
    plt.ylabel("Price")
    plt.savefig("PlotData/Pvstime")
    plt.clf()
    """
    
    plt.errorbar(ptimesteps, TmeanQs, yerr = TerrorQs, color = "#FF0000", marker = '.', linestyle = 'none', capsize = 2, label = "trust on")
    plt.errorbar(ptimesteps, fGmeanQs, yerr = fGerrorQs, color = "#002BFF", capsize = 2, linestyle = 'none', marker = '.', label = "friendly gossip on")
    plt.errorbar(ptimesteps, pGmeanQs, yerr = pGerrorQs, color = "#0F8934", capsize = 2, linestyle = 'none', marker = '.', label = "public gossip on") 
    plt.errorbar(ptimesteps, fGTmeanQs, yerr = fGTerrorQs, color = "#21DEED", capsize = 2,  linestyle = 'none', marker = '.',label = "friendly gossip and trust on")
    plt.errorbar(ptimesteps, pGTmeanQs, yerr = pGTerrorQs, color = "#03F703", capsize = 2, linestyle = 'none', marker = '.', label = "public gossip and trust on")     
    plt.title("Quality over time")
    plt.legend()
    plt.xlabel("Step number")
    plt.ylabel("Quality")
    #plt.yscale("log")
    plt.ylim(0.80,0.875)
    plt.xlim(198,402)
    plt.tight_layout()
    plt.savefig("PlotData/QEndvstime2")
    plt.clf()
    
    
    """
    plt.errorbar(ptimesteps, TmeanQs, yerr = TerrorQs, fmt = "b.", capsize = 2, label = "patients")
    plt.errorbar(rtimesteps, rTmeanQs, yerr = rTerrorQs, fmt = "r.", capsize = 2, label = "retailers")
    plt.title("Quality over time with trust on")
    plt.legend()
    plt.xlabel("Step number")
    plt.ylabel("Quality")
    plt.savefig("PlotData/QvsNT")
    plt.clf()
    
    plt.errorbar(ptimesteps, fGmeanQs, yerr = fGerrorQs, fmt = "b.", capsize = 2, label = "patients")
    plt.errorbar(rtimesteps, rfGmeanQs, yerr = rfGerrorQs, fmt = "r.", capsize = 2, label = "retailers")
    plt.title("Quality over time with friendly gossip on")
    plt.legend()
    plt.xlabel("Step number")
    plt.ylabel("Quality")
    plt.savefig("PlotData/QvsNfG")
    plt.clf()

    plt.errorbar(ptimesteps, pGmeanQs, yerr = pGerrorQs, fmt = "b.", capsize = 2, label = "patients")
    plt.errorbar(rtimesteps, rpGmeanQs, yerr = rpGerrorQs, fmt = "r.", capsize = 2, label = "retailers")
    plt.title("Quality over time with public gossip on")
    plt.legend()
    plt.xlabel("Step number")
    plt.ylabel("Quality")
    plt.savefig("PlotData/QvsNpG")
    plt.clf()

    plt.errorbar(ptimesteps, PmeanQs, yerr = PerrorQs, fmt = "b.", capsize = 2, label = "patients")
    plt.errorbar(rtimesteps, rPmeanQs, yerr = rPerrorQs, fmt = "r.", capsize = 2, label = "retailers")
    plt.title("Quality over time with price on")
    plt.legend()
    plt.xlabel("Step number")
    plt.ylabel("Quality")
    plt.savefig("PlotData/QvsNP")
    plt.clf()
    
    plt.errorbar(ptimesteps, pGTmeanQs, yerr = pGTerrorQs, fmt = "b.", capsize = 2, label = "patients")
    plt.errorbar(rtimesteps, rpGTmeanQs, yerr = rpGTerrorQs, fmt = "r.", capsize = 2, label = "retailers")
    plt.title("Quality over time with public gossip and trust on")
    plt.legend()
    plt.xlabel("Step number")
    plt.ylabel("Quality")
    plt.savefig("PlotData/QvsNpGT")
    plt.clf()
    
    plt.errorbar(ptimesteps, fGTmeanQs, yerr = fGTerrorQs, fmt = "b.", capsize = 2, label = "patients")
    plt.errorbar(rtimesteps, rfGTmeanQs, yerr = rfGTerrorQs, fmt = "r.", capsize = 2, label = "retailers")
    plt.title("Quality over time with friendly gossip and trust on")
    plt.legend()
    plt.xlabel("Step number")
    plt.ylabel("Quality")
    plt.savefig("PlotData/QvsNfGT")
    plt.clf()
    
    
    index = len(stimesteps) - 1
    plt.hist(allPinvs[index,:])
    plt.title("Supplier inventories at end of simulation with price on")
    plt.xlabel("Inventory")
    plt.ylabel("Number of suppliers")
    plt.savefig("PlotData/Pinvs")
    plt.clf()
    
    
    #Tmin = np.min(allTinvs[index,:])
    #Tmax = np.max(allTinvs[index,:])
    #plt.hist(allTinvs[index,:], bins = 10 ** np.linspace(np.log10(Tmin), np.log10(Tmax), 10))
    #plt.gca().set_xscale("log")
    plt.hist(allTinvs[index,:])
    plt.title("Supplier inventories at end of simulation with trust on")
    plt.xlabel("Inventory")
    plt.ylabel("Number of suppliers")
    plt.savefig("PlotData/Tinvs")
    plt.clf()
    

    plt.hist(allGpinvs[index,:])
    plt.title("Supplier inventories at end of simulation with public gossip on")
    plt.xlabel("Inventory")
    plt.ylabel("Number of suppliers")
    plt.savefig("PlotData/Gpinvs")
    plt.clf()
    
    plt.hist(allGfinvs[index,:])
    plt.title("Supplier inventories at end of simulation with friendly gossip on")
    plt.xlabel("Inventory")
    plt.ylabel("Number of suppliers")
    plt.savefig("PlotData/Gfinvs")
    plt.clf()
    
    plt.hist(allGTpinvs[index,:])
    plt.title("Supplier inventories at end of simulation with public gossip and trust on")
    plt.xlabel("Inventory")
    plt.ylabel("Number of suppliers")
    plt.savefig("PlotData/GTpinvs")
    plt.clf()
    
    plt.hist(allGTfinvs[index,:])
    plt.title("Supplier inventories at end of simulation with friendly gossip and trust on")
    plt.xlabel("Inventory")
    plt.ylabel("Number of suppliers")
    plt.savefig("PlotData/GTfinvs")
    plt.clf()    
    
    """

data, runs = allruns()
Qvstime(data, runs)


    				
				
			
