# -*- coding: utf-8 -*-
"""
Trust in Medecine model


Cara Lynch        26/09/2018
"""
import numpy as np
import random as r
import sys
import time as systime # to output how long simulation took


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
        trust += product_quality + r.rand() - 0.5 # want random to be centred on 0
        return trust
    elif trust_model_type == 'b':
        trust = (interaction_number*trust + product_quality + r.rand() - 0.5)/(interaction_number+1)
        return trust

def preferred_supplier(supplier_prices, supplier_inventory, retailer_cash, retailer_trust_in_suppliers, trust_weight):
    """
    Calculates the perceived value of each supplier for a retailer and finds their favourite one with medecine in stock.
    
    :param supplier_prices: (number_suppliers, 1) numpy array with all supplier prices
    :param supplier_inventory: (number_suppliers, 1) numpy array with all supplier inventories
    :param retailer_cash: float which is cash that retailer can spend (so stock they want to buy)
    :param retailer_trust_in_suppliers: (1, number_suppliers) numpy array with the trust this retailer has in all suppliers
    :param trust_weight: float representing the weight of trust
    :return preferred_supplier: int indicating index of preferred supplier
    """
    number_suppliers = np.ma.size(supplier_prices)
    supplier_values = np.zeros(number_suppliers)
    for k in range(0,number_suppliers):
        supplier_values[k] = -supplier_prices[k] + trust_weight*retailer_trust_in_suppliers[k]
    preferred_supplier = np.argmax(supplier_values)
    
    # if not enough inventory, go to next best supplier
    while supplier_inventory[preferred_supplier] < retailer_cash/supplier_prices[preferred_supplier]:
        supplier_values=np.delete(supplier_values, preferred_supplier)
        preferred_supplier = np.argmax(supplier_values)
    return preferred_supplier

def preferred_retailer(retailer_prices, retailer_inventory, patient_trust_in_retailers, trust_weight, patient_retailer_distances):
    """
    Calculates the perceived value of each retailer for a consumer and finds their favourite one with medicine in stock.
    
    :param retailer_prices: (number_retailers, 1) numpy array with all retailer prices
    :param retailer_inventory: (number_retailers, 1) numpy array with all retailer prices
    :param patient_trust_in_retailers: (1, number_retailers) numpy array with the trust this consumer has in all retailers
    :param trust_weight: float representing the weight of trust
    :param patient_retailer_distances: (1, number_retailers) numpy array with the distance from this consumer to all retailers
    :return preferred_retailer: int indicating index of preferred supplier
    """
    number_retailers = np.ma.size(retailer_prices)
    retailer_values = np.zeros(number_retailers)
    for j in range(0,number_retailers):
        retailer_values[j]=-retailer_prices[j] -patient_retailer_distances[j] + trust_weight*patient_trust_in_retailers[j]
    preferred_retailer = np.argmax(retailer_values)
    
    # if no inventory, go to next best retailer
    while retailer_inventory[preferred_retailer] < 1:
        retailer_values = np.delete(retailer_values, preferred_retailer)
        preferred_retailer = np.argmax(retailer_values)
    return preferred_retailer

def replace_supplier(supplier_index, retailer_supplier_trust, supplier_price, supplier_inventory, supplier_cash, supplier_quality):
    """
    Replaces a bankrupt supplier by setting all the values back to initial conditions
    
    :param retailer_index: integer
    :param retailer_supplier_trust: (number_retailers, number_suppliers) numpy array
    :param supplier_price: (number_retailers, 1) numpy array
    :param supplier_inventory: (number_retailers, 1) numpy array
    :param supplier_cash: (number_retailers, 1) numpy array
    :param supplier_quality: (number_retailers, 1) numpy array
    """
    retailer_supplier_trust[:,supplier_index].fill(0.5)
    supplier_inventory[supplier_index]=100
    supplier_cash[supplier_index] = 10+r.rand()
    supplier_price[supplier_index] = 1+r.rand()
    supplier_quality[supplier_index] = r.rand()
    
    return retailer_supplier_trust, supplier_price, supplier_inventory, supplier_cash, supplier_quality


# read input file name from command line
input_file_name = str(sys.argv[1])

# get time for overall time calculation later
systime.clock()

# open input file for reading
with open(input_file_name) as infile:
    lines = infile.readlines()
    trust_model_type = lines[0].split()[3] # c for cumulative, b for bounded
    trust_weight = float(lines[1].split()[2])
    gossip_mode = lines[2].split()[2]
    gossip_weight = float(lines[3].split()[2])
    total_runs = int(lines[4].split()[1])
    total_steps = int(lines[5].split()[1])
    number_patients = int(lines[6].split()[1])
    number_retailers = int(lines[7].split()[1])
    number_suppliers = int(lines[8].split()[1])
    standard_distance = float(lines[9].split()[2])
    retailer_overhead = int(lines[10].split()[2])
    supplier_overhead = int(lines[11].split()[2])

## Create lists of patient and retailer indices to be reshuffled at every
## timestep such that the order in which patients go to retailers and retailers
## go to suppliers is random

patient_list = range(0, number_patients)
retailer_list = range(0, number_retailers)
supplier_list = range(0, number_suppliers)

## Create arrays

# Trust arrays
patient_retailer_trust = np.zeros((number_patients,number_retailers))
retailer_supplier_trust = np.zeros((number_retailers,number_suppliers))

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


## Start runs
for run_number in range(1, total_runs+1):
    
    ## Initialise values
    
    # patients initially have neutral trust for each retailer
    patient_retailer_trust.fill(0.5)
    
    # retailers initially have neutral trust for each supplier
    retailer_supplier_trust.fill(0.5)
    
    # suppliers initial values
    supplier_inventory.fill(100) # all have 100 inventory
    for k in range(0,number_suppliers):
        supplier_cash[k] = 10 + r.rand() # cash
        supplier_quality[k] = r.rand() # quality
        supplier_price[k]=1+r.rand() # price
    
    
    # retailer initial values
    retailer_inventory.fill(number_patients/number_retailers + 1) # inventory
    retailer_cash.fill(10) # cash
    for j in range(0, number_retailers):
        retailer_quality[j] = r.rand() # quality
        retailer_price[j]=1+r.rand() # price
        
        # Set patient - retailer distances
        for i in range(0, number_patients):
            clockwise_separation = standard_distance*abs(i-j*number_patients/number_retailers)
            anticlockwise_separation = standard_distance*abs(number_patients - i + j*number_patients/number_retailers)
            patient_retailer_distance[i,j] = min(clockwise_separation, anticlockwise_separation)
    
    ## Start time loop
    for step_number in range(1, total_steps+1):
        
        # shuffle patient and retailer lists
        r.shuffle(patient_list)
        r.shuffle(retailer_list)
        
        # iterate over all patients
        for patient in patient_list:
            
            # find preferred retailer that has stock
            chosen_retailer = preferred_retailer(retailer_price, retailer_inventory, patient_retailer_trust[patient,:], trust_weight, patient_retailer_distance[patient,:])
            
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
                chosen_supplier = preferred_supplier(supplier_price, supplier_inventory, retailer_cash[retailer], retailer_supplier_trust[retailer,:], trust_weight)
                
                # buy stock from supplier and update own stock
                old_inventory = retailer_inventory[retailer]
                new_stock = int(retailer_cash[retailer]/supplier_price[chosen_supplier]) # stock must be an integer value
                retailer_cash[retailer] = 0 # all cash is put into inventory, what's left over is lost
                retailer_inventory[retailer] += new_stock
                new_quality = supplier_quality[chosen_supplier]
                
                # new quality is weighted average of old and new quality
                retailer_quality[retailer] = (retailer_quality[retailer]*old_inventory + new_stock*new_quality)/retailer_inventory[retailer]
                
                # update supplier stock and cash
                supplier_inventory[chosen_supplier] -= new_stock
                supplier_cash[chosen_supplier] += new_stock*supplier_price[chosen_supplier]
                
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
                retailer_price[retailer] = 1+r.rand()    
                retailer_quality[retailer] = r.rand()
                retailer_supplier_interaction_count[retailer,:].fill(0)
                patient_retailer_interaction_count[:,retailer].fill(0)
            
        for supplier in supplier_list:
            
            # buy stock if have cash
            if supplier_cash>0:
                old_inventory = supplier_inventory[supplier]
                new_stock = int(supplier_cash[supplier])
                supplier_inventory[supplier]+= new_stock
                supplier_cash = 0
                
                # quality is weighted average of new and old stock quality
                supplier_quality[supplier] = new_stock
            
            
            