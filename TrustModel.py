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
    else:
        trust = float((interaction_number*trust + product_quality + r.random() - 0.5)/(interaction_number+1))
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
    min_lifetime = int(lines[11].split()[2]) # lifetime if no sales
    
## Calculate retailer and supplier overhead according to what the
## expected average number of units sold would be per round
retailer_overhead = int((number_patients/number_retailers)/min_lifetime)
supplier_overhead = int((number_patients/number_suppliers)/min_lifetime)

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

# Set patient - retailer distances
for j in range(0, number_retailers):
    for i in range(0, number_patients):
        clockwise_separation = standard_distance*abs(i-j*number_patients/number_retailers)
        anticlockwise_separation = standard_distance*abs(number_patients - i + j*number_patients/number_retailers)
        patient_retailer_distance[i,j] = min(clockwise_separation, anticlockwise_separation)

## Start runs
for run_number in range(1, total_runs+1):
    
    # patient information
    patient_quality = np.zeros((number_patients,1)) # qualitiesof medicine bought by patients
    patient_prices = np.zeros((number_patients,1)) # prices of medicine bought by patients
    
    ## Make directory for output files
    os.mkdir("Run" + str(run_number))
    
    ## Open files for writing
    # Patients
    PatientQualities = open("Run" + str(run_number) + "/PatientQualities.csv","w")
    PatientPrices = open("Run" + str(run_number) + "/PatientPrices.csv","w")
    
    # Retailers
    RetailerPrices = open("Run" + str(run_number) + "/RetailerPrices.csv","w")
    RetailerQualities = open("Run" + str(run_number) + "/RetailerQualities.csv","w")
    RetailerInventories = open("Run" + str(run_number) + "/RetailerInventories.csv","w")
    TrustInRetailers = open("Run" + str(run_number) + "/TrustInRetailers.csv","w")
    RetailerBankruptcy = open("Run" + str(run_number) + "/RetailerBankruptcy.csv","w")
    P_R_interactions = open("Run" + str(run_number) + "/PRInteractionCounts.csv","w")
        
    # Suppliers
    SupplierPrices = open("Run" + str(run_number) + "/SupplierPrices.csv","w")
    SupplierQualities = open("Run" + str(run_number) + "/SupplierQualities.csv","w")
    SupplierInventories = open("Run" + str(run_number) + "/SupplierInventories.csv","w")
    SupplierBankruptcy = open("Run" + str(run_number) + "/SupplierBankruptcy.csv","w")
    TrustInSuppliers = open("Run" + str(run_number) + "/TrustInSuppliers.csv","w")
    R_S_interactions = open("Run" +  str(run_number) + "/RSInteractionCounts.csv","w")
    
    
    # Create strings to write to files
    P_prices = "Timestep\Patient"
    P_quals = "Timestep\Patient"
    
    R_prices = "Timestep\Retailer"
    R_qualities = "Timestep\Retailer"
    R_invs = "Timestep\Retailer"
    R_trusts = "Timestep\Retailer"
    
    S_prices = "Timestep\Supplier"
    S_qualities = "Timestep\Supplier"
    S_invs = "Timestep\Supplier"
    R_S_ints = "Timestep\Supplier"
    S_trusts = "Timestep\Supplier"
    
    # lists to store strings
    patient_strings = [P_prices, P_qualities]
    retailer_strings = [R_prices, R_qualities, R_invs, P_R_ints, R_trusts]
    supplier_strings = [S_prices, S_qualities, S_invs, R_S_ints, S_trusts]

    # add retailer indices to strings
    for j in range(0, number_retailers):
        for n in retailer_strings:
            n += "," + str(j)

    for k in range(0, number_suppliers):
        for m in supplier_strings:
            m += "," + str(k)
    
    for i in range(0, number_patients):
        for l in patient_strings:
            l += "," + str(i)
    
    for n in retailer_strings:
        n += "\n 0"
    
    for m in supplier_strings:
        m += "\n 0"
        
    
    
    RetailerPrices.write("\n 0")
    RetailerQualities.write("\n 0")
    RetailerInventories.write("\n 0")
    TrustInRetailers.write("\n 0")
    if gossip_mode == "f":
        RetailerGossipTrust.write("\n 0")  
    SupplierPrices.write("\n 0")
    SupplierQualities.write("\n 0")
    SupplierInventories.write("\n 0")
    TrustInSuppliers.write("\n 0")
    P_R_interactions.write("\n")
    R_S_interactions.write("\n")
    PatientPrices.write("\n ")
    PatientQualities.write("\n ")
        
    ## Initialise values
    
    
    # patients initially have neutral trust for each retailer
    patient_retailer_trust.fill(0.5)

    
    # retailers initially have neutral trust for each supplier
    retailer_supplier_trust.fill(0.5)
    
    # suppliers initial values
    supplier_inventory.fill(int(number_patients/number_suppliers))
    for k in range(0,number_suppliers):
        supplier_cash[k] = 10 + r.random() # cash
        supplier_quality[k] = r.random() # quality
        supplier_price[k]=1+r.random() # price
    
    
    # retailer initial values
    retailer_inventory.fill(number_patients/number_retailers + 1) # inventory
    retailer_cash.fill(10) # cash
    for j in range(0, number_retailers):
        retailer_quality[j] = r.random() # quality
        retailer_price[j]=1+2*r.random() # price
        

    
    # supplier and retailer bankruptcy counters
    suppliers_bankrupt = 0
    retailers_bankrupt = 0
    
    # patients affected by 0 stock
    no_stock = np.zeros(total_steps)
            
    ## Write initial values into output files
    for retailer in range(0,number_retailers):
        RetailerPrices.write("," + str(float(retailer_price[retailer])))
        RetailerQualities.write("," + str(float(retailer_quality[retailer])))
        RetailerInventories.write("," + str(int(retailer_inventory[retailer])))
        TrustInRetailers.write("," + str(float(np.mean(patient_retailer_trust[:,retailer]))))
        P_R_interactions.write("," + str(0))
        
        if gossip_mode == "f":
            RetailerGossipTrust.write("," + str(float(np.mean(gossip_trust[:,retailer]))))
    RetailerPrices.write("\n")
    RetailerQualities.write("\n")
    RetailerInventories.write("\n")
    TrustInRetailers.write("\n")
    if gossip_mode == "f":
        RetailerGossipTrust.write("\n")
    RetailerBankruptcy.write("Step number, Retailers \n")
    
    for supplier in range(0, number_suppliers):
        SupplierPrices.write("," + str(float(supplier_price[supplier])))
        SupplierQualities.write("," + str(float(supplier_quality[supplier])))
        SupplierInventories.write("," + str(int(supplier_inventory[supplier])))
        TrustInSuppliers.write("," + str(float(np.mean(retailer_supplier_trust[:,supplier]))))
        R_S_interactions.write("," + str(0))

    SupplierPrices.write("\n")
    SupplierQualities.write("\n")
    SupplierInventories.write("\n")
    SupplierBankruptcy.write("Step number, Retailers \n") 
    TrustInSuppliers.write("\n")
    P_R_interactions.write("\n")
    R_S_interactions.write("\n")
    
    
    ## Start time loop
    for step_number in range(1, total_steps+1):
        
        # write step number to files if one of the 40 data points
        if step_number%(total_steps/40.0) == 0:
            RetailerPrices.write(str(step_number))
            RetailerQualities.write(str(step_number))
            RetailerInventories.write(str(step_number))
            TrustInRetailers.write(str(step_number))
            if gossip_mode == "f":
                RetailerGossipTrust.write(str(step_number))  
            SupplierPrices.write(str(step_number))
            SupplierQualities.write(str(step_number))
            SupplierInventories.write(str(step_number))
            TrustInSuppliers.write(str(step_number))
            R_S_interactions.write(str(step_number))
            P_R_interactions.write(str(step_number))
            PatientPrices.write(str(step_number))
            PatientQualities.write(str(step_number))
        
        # shuffle patient and retailer lists
        r.shuffle(patient_list)
        r.shuffle(retailer_list)
        
        
        # determine public gossip trust in each retailer
        if gossip_mode == "p":
            for retailer in retailer_list:
                PR_tested_trust = patient_retailer_trust[:,retailer][patient_retailer_trust[:,retailer] != 0.5]
                if np.ma.size(PR_tested_trust)<1:
                    gossip_trust[retailer]= np.mean(patient_retailer_trust[:,retailer])
                else:    
                    gossip_trust[retailer]= np.mean(PR_tested_trust)

        
        # iterate over all patients
        for patient in patient_list:
            
            # create array with retailer indices and values
            retailer_values = np.zeros((number_retailers,2))
            retailer_values[:,0] = np.array(range(0, number_retailers))
            
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
                            communal_trust.append(patient_retailer_trust[patient+i, retailer])
                            communal_trust.append(patient_retailer_trust[patient-i,retailer])
                    average_trust = np.array(communal_trust).mean()
                    gossip_trust[patient, retailer] = average_trust
                    
                    # calculate retailer values
                    retailer_values[retailer,1] = -retailer_price[retailer] - patient_retailer_distance[patient,retailer] + trust_weight*patient_retailer_trust[patient,retailer] + gossip_weight*gossip_trust[patient, retailer]
                    
            elif gossip_mode == "p":
                
                for retailer in range(0,number_retailers):
                    
                    # calculate retailer values
                    retailer_values[retailer,1] = -retailer_price[retailer] - patient_retailer_distance[patient,retailer] + trust_weight*patient_retailer_trust[patient, retailer] + gossip_weight*gossip_trust[retailer]
                    
            else:
                
                for retailer in range(0, number_retailers):
                    
                    # calculate retailer values
                    retailer_values[retailer,1] = -retailer_price[retailer] - patient_retailer_distance[patient,retailer] + trust_weight*patient_retailer_trust[patient, retailer]
                
            # find preferred retailer
            chosen_retailer_row = np.argmax(retailer_values[:,1])
            chosen_retailer = int(retailer_values[chosen_retailer_row,0])

            
            StockLeft = True
            
            # if no inventory, go to next best retailer
            while retailer_inventory[chosen_retailer] < 1:
                retailer_values = np.delete(retailer_values, chosen_retailer_row,0)
                try:
                    chosen_retailer_row = np.argmax(retailer_values[:,1])
                    chosen_retailer = int(retailer_values[chosen_retailer_row,0])
                except ValueError:
                    print("None of the retailers have enough stock.")
                    print("Patient "+str(patient)+" can't buy from anyone.")
                    StockLeft = False
                    
                    # no stock left so add nans to patient prices and quality and add to no stock counter
                    patient_prices[patient,0] = np.nan
                    patient_quality[patient,0] = np.nan
                    
                    break
            if StockLeft:
                # buy medicine from retailer
                retailer_inventory[chosen_retailer] -= 1
                retailer_cash[chosen_retailer] += retailer_price[chosen_retailer]
                medicine_quality = retailer_quality[chosen_retailer]
                patient_retailer_interaction_count[patient,chosen_retailer] +=1
                
                # change trust value according to whether the medicine worked or not
                patient_retailer_trust[patient,chosen_retailer] = trust_update(patient_retailer_trust[patient,chosen_retailer], medicine_quality,  patient_retailer_interaction_count[patient,chosen_retailer], trust_model_type)
                
                # add patient price and quality to arrays
                patient_prices[patient,0] = retailer_price[chosen_retailer]
                patient_quality[patient,0] = medicine_quality
                
                
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
                new_price = supplier_price[chosen_supplier] + r.random() # random profit margin between 0 and 1 for retailers
                retailer_cash[retailer] = 0 # all cash is put into inventory, what's left over is lost
                retailer_inventory[retailer] += new_stock
                new_quality = supplier_quality[chosen_supplier]
                
                # new quality and price is weighted average of quality and price of old and new stock if new stock purchased
                if new_stock > 0:
                    retailer_quality[retailer] = (retailer_quality[retailer]*old_inventory + new_stock*new_quality)/(old_inventory+new_stock)
                    retailer_price[retailer] = (retailer_price[retailer]*old_inventory + new_stock*new_price)/(old_inventory + new_stock)
                
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
                RetailerBankruptcy.write(str(step_number) + "," + str(int(retailer)) + ", \n")
                
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
                SupplierBankruptcy.write(str(step_number) + "," + str(int(supplier)) + ", \n")
            
            if step_number%(total_steps/40.0) == 0:    
                # supplier list not rearranged so can write directly to file
                SupplierPrices.write("," + str(float(supplier_price[supplier])) )
                SupplierQualities.write("," + str(float(supplier_quality[supplier])) )
                SupplierInventories.write("," + str(int(supplier_inventory[supplier])))
                TrustInSuppliers.write("," + str(float(np.mean(retailer_supplier_trust[:,supplier]))))
                R_S_interactions.write("," + str(np.sum(retailer_supplier_interaction_count[:,supplier])))
                
        
        if step_number%(total_steps/40.0) == 0:
            SupplierPrices.write("\n")
            SupplierQualities.write("\n")
            SupplierInventories.write("\n")
            TrustInSuppliers.write("\n")
            R_S_interactions.write("\n")
            
            # write values to files (need to do another retailer loop as retailers are rearranged)
            
            for retailer in range(0,number_retailers):
                RetailerPrices.write("," + str(float(retailer_price[retailer])))
                RetailerQualities.write("," + str(float(retailer_quality[retailer])))
                RetailerInventories.write("," + str(int(retailer_inventory[retailer])))
                TrustInRetailers.write("," + str(float(np.mean(patient_retailer_trust[:,retailer]))))
                P_R_interactions.write("," + str(np.sum(patient_retailer_interaction_count[:,retailer])))
                if gossip_mode == "f":
                    RetailerGossipTrust.write("," + str(float(np.mean(gossip_trust[:,retailer]))))
            RetailerPrices.write("\n")
            RetailerQualities.write("\n")
            RetailerInventories.write("\n")
            TrustInRetailers.write("\n")
            if gossip_mode == "f":
                RetailerGossipTrust.write("\n")
            P_R_interactions.write("\n")
            
            # write supplier prices and qualities for this step to file
            for patient in range(0, number_patients):
                PatientPrices.write("," + str(patient_prices[patient,0]))
                PatientQualities.write("," + str(patient_quality[patient,0]))
                
            PatientPrices.write("\n")
            PatientQualities.write("\n")

        # give percentage of this run's completion every 10%
        if step_number%(total_steps/10.0) == 0:
            print(str(systime.strftime("%H:%M:%S") + " - " + str(int(step_number*100/total_steps)) + "% of run " + str(run_number) + " of " + str(total_runs) +" complete"))
    
    # Print number of bankrupt retailers and suppliers over run
    SupplierBankruptcy.write("Total bankruptcies: " + str(suppliers_bankrupt))
    RetailerBankruptcy.write("Total bankruptcies: " + str(retailers_bankrupt))
    
    ## Close output files
    RetailerPrices.close()
    RetailerQualities.close()
    RetailerInventories.close()
    SupplierPrices.close()
    SupplierQualities.close()
    SupplierInventories.close()
    TrustInRetailers.close()
    if gossip_mode == "f":
        RetailerGossipTrust.close()
    RetailerBankruptcy.close()
    SupplierBankruptcy.close()
    TrustInSuppliers.close()

# Indicate simulation time    
print("Time taken: " + str(systime.clock()) + "s")
            
