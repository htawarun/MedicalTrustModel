# -*- coding: utf-8 -*-
"""
Trust in Medecine model


Cara Lynch        26/09/2018
"""
import numpy as np 
import random as r # to generate random numbers and shuffle lists
import sys # to get file name from command line
import time as systime # to output how long simulation took
import os

def trust_update(trust, product_quality, interaction_number, trust_model_type):
    """
    Updates retailer trust in supplier or patient trust in retailer according to the desired model.
    
    :param trust: float indicating trust between a retailer and supplier or patient and retailer
    :param product_quality: float which indicates quality of purchased medication
    :param interaction_number: number of interactions between entities considered
    :param trust_model_type: string
    :return trust: float with updated trust value
    """
    if trust_model_type == 'c':
        trust += product_quality + r.random() - 0.5 # want random to be centred on 0
        return trust
    elif trust_model_type == 'b':
        trust = (interaction_number*trust + product_quality + r.random() - 0.5)/(interaction_number+1)
        return trust


# read input file name from command line
input_file_name = str(sys.argv[1])

# get time for overall time calculation later
systime.clock()

# open input file for reading
with open(input_file_name) as infile:
    lines = infile.readlines()
    trust_model_type = lines[0].split()[3] # c for cumulative, b for bounded
    trust_weight = float(lines[1].split()[2])
    gossip_mode = lines[2].split()[2] # p for public, f for friend-based, 0 for off
    gossip_weight = float(lines[3].split()[2]) # if 0 then gossip is off
    gossip_range = int(lines[4].split()[2])
    total_runs = int(lines[5].split()[1])
    total_steps = int(lines[6].split()[1])
    number_patients = int(lines[7].split()[1])
    number_retailers = int(lines[8].split()[1])
    number_suppliers = int(lines[9].split()[1])
    standard_distance = float(lines[10].split()[2])
    retailer_overhead = int(lines[11].split()[2])
    supplier_overhead = int(lines[12].split()[2])

## Create lists of patient and retailer indices to be reshuffled at every
## timestep such that the order in which patients go to retailers and retailers
## go to suppliers is random

patient_list = list(range(0, number_patients))
retailer_list = list(range(0, number_retailers))
supplier_list = list(range(0, number_suppliers))

## Create arrays

# Trust arrays
patient_retailer_trust = np.zeros((number_patients,number_retailers))
retailer_supplier_trust = np.zeros((number_retailers,number_suppliers))

# Gossip trust arrays
if gossip_mode == "f":
    gossip_trust = np.zeros((number_patients,number_retailers))
elif gossip_mode == "p":
    gossip_trust = np.zeros(number_retailers)

# Interaction count arrays
patient_retailer_interaction_count = np.zeros((number_patients,number_retailers))
retailer_supplier_interaction_count = np.zeros((number_retailers,number_suppliers))

# Distance array
patient_retailer_distance=np.zeros((number_patients,number_retailers))

# retailer information
retailer_price = np.zeros((number_retailers,1))
retailer_inventory = np.zeros((number_retailers,1))
retailer_cash = np.zeros((number_retailers,1))
retailer_quality = np.zeros((number_retailers,1))

# supplier information
supplier_price = np.zeros((number_suppliers,1))
supplier_inventory = np.zeros((number_suppliers,1))
supplier_cash = np.zeros((number_suppliers,1))
supplier_quality = np.zeros((number_suppliers,1))

## Bankruptcy counts
retailers_bankrupt = 0
suppliers_bankrupt = 0

## Start runs
for run_number in range(1, total_runs+1):
    
    ## Make directory for output files
    os.mkdir("Run" + str(run_number))
    
    ## Open files for writing
    RetailerPrices = open("Run" + str(run_number) + "/RetailerPrices.csv","w")
    RetailerQualities = open("Run" + str(run_number) + "/Qualities.csv","w")
    SupplierPrices = open("Run" + str(run_number) + "/SupplierPrices.csv","w")
    SupplierQualities = open("Run" + str(run_number) + "/SupplierQualities.csv","w")
    
    
    ## Initialise values
    
    # patients initially have neutral trust for each retailer
    patient_retailer_trust.fill(0.5)
    
    # retailers initially have neutral trust for each supplier
    retailer_supplier_trust.fill(0.5)
    
    # suppliers initial values
    supplier_inventory.fill(100) # all have 100 inventory
    for k in range(0,number_suppliers):
        supplier_cash[k] = 10 + r.random() # cash
        supplier_quality[k] = r.random() # quality
        supplier_price[k]=1+r.random() # price
    
    
    # retailer initial values
    retailer_inventory.fill(number_patients/number_retailers + 1) # inventory
    retailer_cash.fill(10) # cash
    for j in range(0, number_retailers):
        retailer_quality[j] = r.random() # quality
        retailer_price[j]=1+r.random() # price
        
        # Set patient - retailer distances
        for i in range(0, number_patients):
            clockwise_separation = standard_distance*abs(i-j*number_patients/number_retailers)
            anticlockwise_separation = standard_distance*abs(number_patients - i + j*number_patients/number_retailers)
            patient_retailer_distance[i,j] = min(clockwise_separation, anticlockwise_separation)
            
    ## Write initial values into output files
    for retailer in range(0,number_retailers):
        RetailerPrices.write(str(retailer_price[retailer]) + ",")
        RetailerQualities.write(str(retailer_quality[retailer])+",")
    RetailerPrices.write("\n")
    RetailerQualities.write("\n")
    
    for supplier in range(0, number_suppliers):
        SupplierPrices.write(str(supplier_price[supplier]) + ",")
        SupplierQualities.write(str(supplier_quality[supplier]) +",")
    SupplierPrices.write("\n")
    SupplierQualities.write("\n")
    
    
    ## Start time loop
    for step_number in range(1, total_steps+1):
        
        # give percentage of this run's completion every 10%
        if step_number%(total_steps/10.0) == 0:
            print(str(systime.strftime("%H:%M:%S") + " - " + str(int(step_number*100/total_steps)) + "% of run " + str(run_number) + " of " + str(total_runs) +" complete"))

        
        # shuffle patient and retailer lists
        r.shuffle(patient_list)
        r.shuffle(retailer_list)
        
        
        # determine public gossip trust in each retailer
        if gossip_mode == "p":
            for retailer in retailer_list:
                average_trust = patient_retailer_trust[:,retailer].mean()
                gossip_trust[retailer]=average_trust
        
        # iterate over all patients
        for patient in patient_list:
            
            retailer_values = np.zeros(number_retailers)
            
            if gossip_mode == "f":
                

                
                for retailer in range(0, number_retailers):
                    communal_trust = []
                    
                    # determine gossip trust this patient has in each retailer
                    for i in range(1, gossip_range + 1):
                        if patient + i >= number_patients:
                            communal_trust.append(patient_retailer_trust[patient+i-number_patients, retailer])
                            communal_trust.append(patient_retailer_trust[patient-i,retailer])
                        elif patient-i<0:
                            communal_trust.append(patient_retailer_trust[patient-i+number_patients,retailer])
                            communal_trust.append(patient_retailer_trust[patient+i,retailer])
                        else:
                            communal_trust.append(patient_retailer_trust[patient+i,retailer])
                            communal_trust.append(patient_retailer_trust[patient-i,retailer])
                    average_trust = np.array(communal_trust).mean()
                    gossip_trust[patient, retailer] = average_trust
                    
                    # calculate retailer values
                    retailer_values[retailer] = -retailer_price[retailer] - patient_retailer_distance[patient,retailer] + trust_weight*patient_retailer_trust[patient,retailer] + gossip_weight*gossip_trust[patient, retailer]
                    
            elif gossip_mode == "p":
                
                for retailer in range(0,number_retailers):
                    
                    # calculate retailer values
                    retailer_values[retailer] = -retailer_price[retailer] - patient_retailer_distance[patient,retailer] + trust_weight*patient_retailer_trust[patient, retailer] + gossip_weight*gossip_trust[retailer]
                    
            else:
                
                for retailer in range(0, number_retailers):
                    
                    # calculate retailer values
                    retailer_values[retailer] = -retailer_price[retailer] - patient_retailer_distance[retailer] + trust_weight*patient_retailer_trust[patient, retailer]
                
            # find preferred retailer
            chosen_retailer = np.argmax(retailer_values)
            
            StockLeft = True
            
            # if no inventory, go to next best retailer
            while retailer_inventory[chosen_retailer] < 1:
                retailer_values = np.delete(retailer_values, chosen_retailer)
                try:
                    chosen_retailer = np.argmax(retailer_values)
                except ValueError:
                    print("None of the retailers have enough stock.")
                    print("Patient "+str(patient)+" can't buy from anyone.")
                    print(retailer_inventory)
                    StockLeft = False
                    break
            if StockLeft:
                # buy medicine from retailer
                retailer_inventory[chosen_retailer] -= 1
                retailer_cash[chosen_retailer] += retailer_price[chosen_retailer]
                medicine_quality = retailer_quality[chosen_retailer]
                patient_retailer_interaction_count[patient,chosen_retailer] +=1
                
                # change trust value according to whether the medicine worked or not
                patient_retailer_trust[patient,chosen_retailer] = trust_update(patient_retailer_trust[patient,chosen_retailer], medicine_quality,  patient_retailer_interaction_count[patient,chosen_retailer], trust_model_type)
            
        # iterate over all retailers
        for retailer in retailer_list:
            
            # only buy stock if cash is positive
            if retailer_cash[retailer]>0:
            
                # find preferred supplier that has enough stock
                supplier_values = np.zeros(number_suppliers)
                for supplier in range(0, number_suppliers):
                    supplier_values[supplier] = -supplier_price[supplier] + trust_weight*retailer_supplier_trust[retailer,supplier]
                
                chosen_supplier = np.argmax(supplier_values)

                # buy stock from supplier and update own stock
                old_inventory = retailer_inventory[retailer]
                new_stock = int(retailer_cash[retailer]/supplier_price[chosen_supplier]) # stock must be an integer value
                retailer_cash[retailer] = 0 # all cash is put into inventory, what's left over is lost
                retailer_inventory[retailer] += new_stock
                new_quality = supplier_quality[chosen_supplier]
                
                # new quality is weighted average of old and new quality
                retailer_quality[retailer] = (retailer_quality[retailer]*old_inventory + new_stock*new_quality)/retailer_inventory[retailer]
                
                # update supplier stock and cash
                # if supplier has stock, reduce stock 
                if supplier_inventory[chosen_supplier] >= new_stock:
                    supplier_inventory[chosen_supplier] -= new_stock
                    supplier_cash[chosen_supplier] += new_stock*supplier_price[chosen_supplier]
                # if not enough stock
                else:
                    # add only profit to supplier's cash (cost of medecine to supplier is 1)
                    supplier_cash[chosen_supplier] += new_stock*(supplier_price[chosen_supplier] - 1)
                    
                
                # update interaction count
                retailer_supplier_interaction_count[retailer,chosen_supplier] += 1
                
                # update retailer-supplier trust value
                retailer_supplier_trust[retailer,chosen_supplier] = trust_update(retailer_supplier_trust[retailer,chosen_supplier], new_quality, retailer_supplier_interaction_count[retailer,chosen_supplier], trust_model_type)
                
            # remove retailer overhead
            retailer_inventory[retailer] -= retailer_overhead
            
            # if retailer is bankrupt, replace (set everything back to initial values)
            if retailer_inventory[retailer] <= 0:
                patient_retailer_trust[:,retailer].fill(0.5)
                retailer_supplier_trust[retailer,:].fill(0.5)
                retailer_inventory[retailer]=number_patients/number_retailers + 1
                retailer_cash[retailer]=10
                retailer_price[retailer] = 1+r.random()    
                retailer_quality[retailer] = r.random()
                retailer_supplier_interaction_count[retailer,:].fill(0)
                patient_retailer_interaction_count[:,retailer].fill(0)
                retailers_bankrupt += 1
                
        for supplier in supplier_list:
            
            # buy stock if have cash
            if supplier_cash[supplier]>0:
                supplier_inventory[supplier]+= int(supplier_cash[supplier])
                supplier_cash[supplier] = 0
            
            # remove supplier overhead
            supplier_inventory[supplier] -= supplier_overhead
            
            # replace supplier if bankrupt
            if supplier_inventory[supplier] <= 0:
                retailer_supplier_trust[:,supplier].fill(0.5)
                supplier_inventory[supplier]=100
                supplier_cash[supplier] = 10+r.random()
                supplier_price[supplier] = 1+r.random()
                supplier_quality[supplier] = r.random()
                suppliers_bankrupt+=1
                
            # supplier list not rearranged so can write directly to file
            SupplierPrices.write(str(supplier_price[supplier]) + ",")
            SupplierQualities.write(str(supplier_quality[supplier]) +",")
        
        SupplierPrices.write("\n")
        SupplierQualities.write("\n")
        
        # write values to files (need to do another retailer loop as retailers are rearranged)
        
        for retailer in range(0,number_retailers):
            RetailerPrices.write(str(retailer_price[retailer]) + ",")
            RetailerQualities.write(str(retailer_quality[retailer])+",")
        RetailerPrices.write("\n")
        RetailerQualities.write("\n")
       
    ## Close output files
    RetailerPrices.close()
    RetailerQualities.close()
    SupplierPrices.close()
    SupplierQualities.close()
            
