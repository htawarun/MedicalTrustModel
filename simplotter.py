# -*- coding: utf-8 -*-
"""
Plot data produced during Trust Model simulations

Created on Sat Oct 13 18:33 2018

@author: Cara Lynch
"""

import numpy as np
import os
import matplotlib.pyplot as plt
import sys
import math

def read_olddata(infile):
    """
    Reads files and puts data into arrays
    
    :param infile: string, name of file to read
    :return array: numpy array of all data from file
    """
    with open(infile, "rt") as file:
        
        lines = file.readlines()
        width = len(lines[0].split(','))
        length = len(lines)
        
        array = np.zeros((length,width))
        
        for i in range(0, len(lines)):
            linetokens = lines[i].split(',')
            for n in range(0, len(linetokens)):
                array[i,n] = float(linetokens[n])
        return array
        
def read_newdata(infile):
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

## get data for all runs

def get_data(gossip_mode):
    """
    Gets data from  files for all runs in directory
    
    :param gossip_mode: string indicating which gossip mode is used
    :param new_or_old: string indicating whether the output files are in new or old format
    :return retailer_data: list of lists, each run is one element, each element is a list of
    numpy arrays (directory, timesteps, inventory, price, quality, trust in retailer, quality/price and gossip trust if friendly mode)
    :return supplier_data: list of lists, each run is an element, each element a list of numpy arrays
    (directory, timesteps, inventory, quality, quality/price and trust if applicable)
    :return retailer_mean_data: list of lists, each run is an element, each element a list of numpy arrays
    (directory, timesteps, mean prices and errors, mean quality and errors, mean trust and errors, mean q/p and errors, mean gossip trust and errors)
    :param supplier_mean_data: list of lists, each run is an element, each element a list of numpy array
    (directory, timesteps, mean prices and errors, mean quality and errors, mean q/p and errors, mean trust and errors)
    """
    
    ## create empty lists for data from each run
    retailer_data = []
    retailer_mean_data = []
    supplier_data = []
    supplier_mean_data = []
    patient_data = []
    patient_mean_data = []
    
    for directory in os.listdir("."):
        if os.path.isdir(directory):
            if os.path.exists(directory + "/RetailerInventories.csv"):

                    
                timesteps, retailer_inventory = read_newdata(directory+"/RetailerInventories.csv")
                timesteps, retailer_price = read_newdata(directory+"/RetailerPrices.csv")
                timesteps, retailer_quality = read_newdata(directory + "/RetailerQualities.csv")
                
                timesteps,supplier_inventory = read_newdata(directory+"/SupplierInventories.csv")
                timesteps,supplier_price = read_newdata(directory+"/SupplierPrices.csv")
                timesteps,supplier_quality = read_newdata(directory + "/SupplierQualities.csv")
                
                timesteps, retailer_trust = read_newdata(directory + "/TrustInRetailers.csv")
                timesteps, supplier_trust = read_newdata(directory + "/TrustInSuppliers.csv")
                
                if gossip_mode == "f":
                    timesteps, gossip_trust = read_newdata(directory + "/GossipTrust.csv")
                        
                # lol mixup        
                ptimesteps, patient_price = read_newdata(directory+"/PatientQualities.csv")
                ptimesteps, patient_quality = read_newdata(directory + "/PatientPrices.csv")
                        
                # interesting calculations
                retailer_quality_price = np.divide(retailer_quality, retailer_price)
                supplier_quality_price = np.divide(supplier_quality, supplier_price)
                patient_quality_price = np.divide(patient_quality, patient_price)
                
                # add data to list for this run
                retailer_run_list = [directory, timesteps, retailer_inventory, retailer_price, retailer_quality, retailer_trust, retailer_quality_price]
                if gossip_mode == "f":
                    retailer_run_list.append(gossip_trust)
                supplier_run_list = [directory, timesteps, supplier_inventory, supplier_price, supplier_quality, supplier_quality_price]
                supplier_run_list.append(supplier_trust)
                patient_run_list = [directory, ptimesteps, patient_price, patient_quality, patient_quality_price]
                
                # get mean values and standard deviations over all retailers and suppliers
                retailer_price_mean = np.zeros((np.ma.size(timesteps),1))
                retailer_quality_mean = np.zeros((np.ma.size(timesteps),1))
                retailer_trust_mean = np.zeros((np.ma.size(timesteps),1))
                if gossip_mode == "f":
                    gossip_trust_mean = np.zeros((np.ma.size(timesteps),1))

                supplier_price_mean = np.zeros((np.ma.size(timesteps),1))
                supplier_quality_mean = np.zeros((np.ma.size(timesteps),1))
                
                retailer_q_p_mean = np.zeros((np.ma.size(timesteps),1))
                supplier_q_p_mean = np.zeros((np.ma.size(timesteps),1))
                
                supplier_trust_mean = np.zeros((np.ma.size(timesteps),1))
                
                patient_q_mean = np.zeros((np.ma.size(ptimesteps), 1))
                patient_p_mean = np.zeros((np.ma.size(ptimesteps), 1))
                patient_q_p_mean = np.zeros((np.ma.size(ptimesteps), 1))
                
                for n in range(0, np.ma.size(ptimesteps)):
                    patient_q_mean[n,0] = np.mean(patient_quality[n,:])
                    patient_p_mean[n,0] = np.mean(patient_price[n,:])
                    patient_q_p_mean[n,0] = np.mean(patient_quality_price[n,:])
                
                for i in range(0,np.ma.size(timesteps)):
                    
                    retailer_price_mean[i,0] = np.mean(retailer_price[i,:])
                    retailer_quality_mean[i,0] = np.mean(retailer_quality[i,:])
                    retailer_trust_mean[i,0] = np.mean(retailer_trust[i,:])
                    if gossip_mode == "f":
                        gossip_trust_mean[i,0] = np.mean(gossip_trust[i,:])
                    
                    retailer_q_p_mean[i,0] = np.mean(retailer_quality_price[i,:])

                    supplier_price_mean[i,0] = np.mean(supplier_price[i,:])
                    supplier_quality_mean[i,0] = np.mean(supplier_quality[i,:])

                    supplier_trust_mean[i,0] = np.mean(supplier_trust[i,:])
                    
                    supplier_q_p_mean[i,0] = np.mean(supplier_quality_price[i,:])
                
                # add mean and stdev data to list for this run
                retailer_run_mean_list = [directory, timesteps, retailer_price_mean, retailer_quality_mean, retailer_trust_mean, retailer_q_p_mean]
                if gossip_mode == "f":
                    retailer_run_mean_list.append(gossip_trust_mean)
                supplier_run_mean_list = [directory, timesteps, supplier_price_mean, supplier_quality_mean, supplier_q_p_mean]

                supplier_run_mean_list.append(supplier_trust_mean)
                
                patient_run_mean_list = [directory, ptimesteps, patient_p_mean, patient_q_mean, patient_q_p_mean]
                
                patient_data.append(patient_run_list)
                patient_mean_data.append(patient_run_mean_list)
                retailer_data.append(retailer_run_list)
                retailer_mean_data.append(retailer_run_mean_list)
                supplier_data.append(supplier_run_list)
                supplier_mean_data.append(supplier_run_mean_list)
                    
    return  retailer_data, retailer_mean_data, supplier_data, supplier_mean_data, patient_data, patient_mean_data
            

## make supplier histograms
def supplier_inv_histograms(supplier_data):
    """
    Makes histograms of the initial, midway and final supplier inventories
    """
    try:
        os.mkdir("SupplierData")
    except OSError:
        print("Data file already exists")
        
    k = 0
    
    for run in supplier_data:
        name = run[0]
        timesteps = run[1]
        inventory = run[2]
        
        # for plotting histograms over all runs
        if k == 0:
            allinventories = inventory
        else:
            allinventories += inventory  
        """
        # plot initial values
        plt.hist(inventory[0,:])
        plt.title(name + " inventory at t=" + str(int(timesteps[0])))
        plt.xlabel("Inventory")
        plt.ylabel("Number of suppliers")
        plt.savefig("SupplierData/" + name + "Inventory" + str(int(timesteps[0]))+".png")
        plt.clf()
        
        # plot midway values
        index = int((len(timesteps)+1)/2)
        plt.hist(inventory[index,:])
        plt.title(name+ " inventory at t=" + str(timesteps[index]))
        plt.xlabel("Inventory")
        plt.ylabel("Number of suppliers")
        plt.savefig("SupplierData/" + name + "Inventory" + str(timesteps[index])+".png")
        plt.clf()
        """
        # plot end values
        index = len(timesteps) - 1
        plt.hist(inventory[index,:])
        plt.title(name+ " inventory at t=" + str(timesteps[index]))
        plt.xlabel("Inventory")
        plt.ylabel("Number of suppliers")
        plt.savefig("SupplierData/" + name + "Inventory" + str(timesteps[index])+".png")
        plt.clf()
        
        k += 1
    """    
    print(k)
    averageinventory = allinventories/k
    
    ## plot histogram of average inventory
    # plot initial values
    plt.hist(averageinventory[0,:])
    plt.title("Average inventory at t=" + str(int(timesteps[0])))
    plt.xlabel("Inventory")
    plt.ylabel("Number of suppliers")
    plt.savefig("SupplierData/AverageInventory" + str(int(timesteps[0]))+".png")
    plt.clf()
    
    # plot midway values
    index = int((len(timesteps)+1)/2)
    plt.hist(averageinventory[index,:])
    plt.title("Average inventory at t=" + str(timesteps[index]))
    plt.xlabel("Inventory")
    plt.ylabel("Number of suppliers")
    plt.savefig("SupplierData/AverageInventory" + str(timesteps[index])+".png")
    plt.clf()
    
    # plot end values
    index = len(timesteps) - 1
    plt.hist(inventory[index,:])
    plt.title("Average inventory at t=" + str(timesteps[index]))
    plt.xlabel("Inventory")
    plt.ylabel("Number of suppliers")
    plt.savefig("SupplierData/AverageInventory" + str(timesteps[index])+".png")
    plt.clf()  
    """               
        

        
def retailer_inv_histograms(retailer_data):
    """
    Makes histograms of the initial, midway and final retailer inventories
    """
    try:
        os.mkdir("RetailerData")
    except OSError:
        print("Data file already exists")
     
    k = 0
        
    for run in retailer_data:
        name = run[0]
        timesteps = run[1]
        inventory = run[2]
        
        # for plotting histograms over all runs
        if k == 0:
            allinventories = inventory
        else:
            allinventories += inventory
        """
        # plot initial values
        plt.hist(inventory[0,:])
        plt.title(name + " inventory at t=" + str(int(timesteps[0])))
        plt.xlabel("Inventory")
        plt.ylabel("Number of retailers")
        plt.savefig("RetailerData/" + name + "Inventory" + str(int(timesteps[0]))+".png")
        plt.clf()
        
        # plot midway values
        index = int((len(timesteps)+1)/2)
        plt.hist(inventory[index,:])
        plt.title(name+ " inventory at t=" + str(timesteps[index]))
        plt.xlabel("Inventory")
        plt.ylabel("Number of retailers")
        plt.savefig("RetailerData/" + name + "Inventory" + str(timesteps[index])+".png")
        plt.clf()
        """
        # plot end values
        index = len(timesteps) - 1
        plt.hist(inventory[index,:])
        plt.title(name+ " inventory at t=" + str(timesteps[index]))
        plt.xlabel("Inventory")
        plt.ylabel("Number of retailers")
        plt.savefig("RetailerData/" + name + "Inventory" + str(timesteps[index])+".png")
        plt.clf()
        
        k += 1
    """
    print(k)
    averageinventory = allinventories/k
    
    ## plot histogram of average inventory
    # plot initial values
    plt.hist(averageinventory[0,:])
    plt.title("Average inventory at t=" + str(int(timesteps[0])))
    plt.xlabel("Inventory")
    plt.ylabel("Number of retailers")
    plt.savefig("RetailerData/AverageInventory" + str(int(timesteps[0]))+".png")
    plt.clf()
    
    # plot midway values
    index = int((len(timesteps)+1)/2)
    plt.hist(averageinventory[index,:])
    plt.title("Average inventory at t=" + str(timesteps[index]))
    plt.xlabel("Inventory")
    plt.ylabel("Number of retailers")
    plt.savefig("RetailerData/AverageInventory" + str(timesteps[index])+".png")
    plt.clf()
    
    # plot end values
    index = len(timesteps) - 1
    plt.hist(inventory[index,:])
    plt.title("Average inventory at t=" + str(timesteps[index]))
    plt.xlabel("Inventory")
    plt.ylabel("Number of retailers")
    plt.savefig("RetailerData/AverageInventory" + str(timesteps[index])+".png")
    plt.clf()    
    """
    
    
    
def patient_mean_plotter(patient_mean_data):
    try:
        os.mkdir("PatientData")
    except OSError:
        print("Patient data file already exists")
    
    timesteps = patient_mean_data[0][1]
    
    # create arrays to have the mean quality/price and error over time for each run
    means_QP = np.zeros((len(patient_mean_data),len(timesteps)))
    
    # mean price and error arrays
    means_price = np.zeros((len(patient_mean_data),len(timesteps)))
    
    # mean quality and error arrays
    means_quality = np.zeros((len(patient_mean_data),len(timesteps)))
    
    k = 0
    
    for run in patient_mean_data:
        name = run[0]
        timesteps = run[1]
        price = run[2]
        quality = run[3]
        QP = run[4]
        
        # add mean values over time
        for i in range(0, len(timesteps)):
            means_QP[k,i] = QP[i,0]
            means_price[k,i] = price[i,0]
            means_quality[k,i] = quality[i,0]
        k+=1
        
    mean_QP_allruns = np.zeros(np.ma.size(means_QP,1))
    error_QP_allruns =np.zeros(np.ma.size(means_QP,1)) 
    mean_price_allruns = np.zeros(np.ma.size(means_price,1))
    error_price_allruns = np.zeros(np.ma.size(means_price,1))
    mean_quality_allruns = np.zeros(np.ma.size(means_quality,1))
    error_quality_allruns = np.zeros(np.ma.size(means_quality,1))
    
    
    # open output file to write mean values into
    dirpath = os.getcwd()
    foldername = os.path.basename(dirpath)
    meanfile = open("PatientData/" + foldername, "w")
    errorsfile = open("PatientData/AllRunsErrors","w")
    meanfile.write("timestep,mean price,mean quality,mean QP\n")
    errorsfile.write("timestep, error price, error quality, error QP \n")
    
    # calculate means and errors over all runs
    for i in range(0, np.ma.size(means_QP,1)):
        mean_QP_allruns[i] = np.mean(means_QP[:,i])
        error_QP_allruns[i] = np.std(means_QP[:,i])/math.sqrt(len(patient_mean_data))
        mean_price_allruns[i] = np.mean(means_price[:,i])
        error_price_allruns[i] =  np.std(means_price[:,i])/math.sqrt(len(patient_mean_data))
        mean_quality_allruns[i] = np.mean(means_quality[:,i])
        error_quality_allruns[i] =  np.std(means_quality[:,i])/math.sqrt(len(patient_mean_data))
        
        # write to file
        meanfile.write(str(timesteps[i]) + "," + str(mean_price_allruns[i])  + "," + str(mean_quality_allruns[i]) + "," + str(mean_QP_allruns[i]) + "\n")
        errorsfile.write(str(timesteps[i]) + "," + str(error_price_allruns[i])  + "," + str(error_quality_allruns[i]) + "," + str(error_QP_allruns[i]) + "\n")
    
    # graph QP for all runs
    plt.errorbar(timesteps, mean_QP_allruns, yerr = error_QP_allruns, fmt= 'k.', capsize=2)
    plt.title("Mean Quality/Price over time")
    plt.xlabel("Step number")
    plt.ylabel("Quality/Price")
    plt.savefig("PatientData/Overall_Quality_Price.png")
    plt.clf()

    
    # graph quality for all runs
    plt.errorbar(timesteps, mean_quality_allruns, yerr = error_quality_allruns, fmt= 'k.', capsize=2)
    plt.title("Mean Quality over time")
    plt.xlabel("Step number")
    plt.ylabel("Quality")
    plt.savefig("PatientData/Overall_Quality.png")
    plt.clf()    
    
    # graph price for all runs
    plt.errorbar(timesteps, mean_price_allruns, yerr = error_price_allruns, fmt= 'k.', capsize=2)
    plt.title("Mean Price over time")
    plt.xlabel("Step number")
    plt.ylabel("Price")
    plt.savefig("PatientData/Overall_Price.png")
    plt.clf()

def retailer_mean_plotter(retailer_mean_data):
    """
    Makes a Q/P plot over time for retailers
    """
    try:
        os.mkdir("RetailerData")
    except OSError:
        print("Data file already exists")
    
    timesteps = retailer_mean_data[0][1]
    
    # create arrays to have the mean quality/price and error over time for each run
    means_QP = np.zeros((len(retailer_mean_data),len(timesteps)))

    
    # create arrays to have mean trust and error over time for each run
    means_trust = np.zeros((len(retailer_mean_data),len(timesteps)))

    
    # mean price and error arrays
    means_price = np.zeros((len(retailer_mean_data),len(timesteps)))

    
    # mean quality and error arrays
    means_quality = np.zeros((len(retailer_mean_data),len(timesteps)))

    
    k = 0
    
    for run in retailer_mean_data:
        name = run[0]
        timesteps = run[1]
        price = run[2]
        quality = run[3]
        QP = run[5]
        trust = run[4]
        
        # add mean values over time
        for i in range(0, len(timesteps)):
            means_QP[k,i] = QP[i,0]
            means_trust[k,i] = trust[i,0]
            means_price[k,i] = price[i,0]
            means_quality[k,i] = quality[i,0]
        k+=1
        
        
        """
        # graph quality over price
        plt.errorbar(timesteps, QP[:,0], yerr=QP[:,1], fmt='k.', capsize=2)
        plt.title(name + " Quality/Price over time")
        plt.xlabel("Step number")
        plt.ylabel("Quality/Price")
        plt.savefig("RetailerData/" + name + "Quality_Price.png")
        plt.clf()
        
        # graph trust
        plt.errorbar(timesteps, trust[:,0], yerr = trust[:,1], fmt = 'k.', capsize=2)
        plt.title(name + " trust in retailers over time")
        plt.xlabel("Step number")
        plt.ylabel("Trust")
        plt.savefig("RetailerData/" + name + "Trust.png")
        plt.clf()
        
        # graph price
        plt.errorbar(timesteps, price[:,0], yerr = price[:,1], fmt='k.', capsize = 2)
        plt.title(name + " price over time")
        plt.xlabel("Step number")
        plt.ylabel("Price")
        plt.savefig("RetailerData/" + name + "Price.png")
        plt.clf()
        
        # graph quality 
        plt.errorbar(timesteps, quality[:,0], yerr = quality[:,1], fmt='k.', capsize = 2)
        plt.title(name + " quality over time")
        plt.xlabel("Step number")
        plt.ylabel("Quality")
        plt.savefig("RetailerData/" + name + "Quality.png")
        plt.clf()
        """    
    mean_QP_allruns = np.zeros(np.ma.size(means_QP,1))
    error_QP_allruns =np.zeros(np.ma.size(means_QP,1)) 
    mean_trust_allruns= np.zeros(np.ma.size(means_trust,1))
    error_trust_allruns= np.zeros(np.ma.size(means_trust,1))
    mean_price_allruns = np.zeros(np.ma.size(means_price,1))
    error_price_allruns = np.zeros(np.ma.size(means_price,1))
    mean_quality_allruns = np.zeros(np.ma.size(means_quality,1))
    error_quality_allruns = np.zeros(np.ma.size(means_quality,1))
    
    
    # open output file to write mean values into
    dirpath = os.getcwd()
    foldername = os.path.basename(dirpath)
    meanfile = open("RetailerData/" + foldername, "w")
    errorsfile = open("RetailerData/AllRunsErrors","w")
    meanfile.write("timestep, mean price, mean quality, mean QP, mean trust \n")
    errorsfile.write("timestep, error price, error quality, error QP, error trust \n")
    
    # calculate means and errors over all runs
    for i in range(0, np.ma.size(means_QP,1)):
        mean_QP_allruns[i] = np.mean(means_QP[:,i])
        error_QP_allruns[i] = np.std(means_QP[:,i])/math.sqrt(len(retailer_mean_data))
        mean_trust_allruns[i] = np.mean(means_trust[:,i])
        error_trust_allruns[i] = np.std(means_trust[:,i])/math.sqrt(len(retailer_mean_data))
        mean_price_allruns[i] = np.mean(means_price[:,i])
        error_price_allruns[i] = np.std(means_price[:,i])/math.sqrt(len(retailer_mean_data))
        mean_quality_allruns[i] = np.mean(means_quality[:,i])
        error_quality_allruns[i] = np.std(means_quality[:,i])/math.sqrt(len(retailer_mean_data))
        
        # write to file
        meanfile.write(str(timesteps[i]) + "," + str(mean_price_allruns[i])  + "," + str(mean_quality_allruns[i]) + "," + str(mean_QP_allruns[i]) + "," + str(mean_trust_allruns[i]) + "\n")
        errorsfile.write(str(timesteps[i]) + "," + str(error_price_allruns[i])  + "," + str(error_quality_allruns[i]) + "," + str(error_QP_allruns[i]) + "," + str(error_trust_allruns[i]) + "\n")
    
    # graph QP for all runs
    plt.errorbar(timesteps, mean_QP_allruns, yerr = error_QP_allruns, fmt= 'k.', capsize=2)
    plt.title("Mean Quality/Price over time")
    plt.xlabel("Step number")
    plt.ylabel("Quality/Price")
    plt.savefig("RetailerData/Overall_Quality_Price.png")
    plt.clf()

    
    # graph trust for all runs
    plt.errorbar(timesteps, mean_trust_allruns, yerr = error_trust_allruns, fmt= 'k.', capsize=2)
    plt.title("Mean trust over time")
    plt.xlabel("Step number")
    plt.ylabel("Trust")
    plt.savefig("RetailerData/Overall_Trust.png")
    plt.clf()
    
    # graph quality for all runs
    plt.errorbar(timesteps, mean_quality_allruns, yerr = error_quality_allruns, fmt= 'k.', capsize=2)
    plt.title("Mean Quality over time")
    plt.xlabel("Step number")
    plt.ylabel("Quality")
    plt.savefig("RetailerData/Overall_Quality.png")
    plt.clf()    
    
    # graph price for all runs
    plt.errorbar(timesteps, mean_price_allruns, yerr = error_price_allruns, fmt= 'k.', capsize=2)
    plt.title("Mean Price over time")
    plt.xlabel("Step number")
    plt.ylabel("Price")
    plt.savefig("RetailerData/Overall_Price.png")
    plt.clf()
    

## read command line
gossip_mode = sys.argv[1] # f friendly, p public, 0 off

retailer_data, retailer_mean_data, supplier_data, supplier_mean_data, patient_data, patient_mean_data = get_data(gossip_mode)

#supplier_inv_histograms(supplier_data)
#retailer_inv_histograms(retailer_data)
retailer_mean_plotter(retailer_mean_data)
patient_mean_plotter(patient_mean_data)
