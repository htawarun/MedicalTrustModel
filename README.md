# MedicalTrustModel

Cara Lynch

October 2018

## Overview
Simple model trying to describe the evolution of trust in medecine, based on previous work by Graeme Ackland. This model aims to incorporate gossip.

## Input files

The input file must be in the following format:

Trust model type: [string] # c for cumulative, b for bounded

Trust weight: [float] # float between 0 and 1

Gossip mode: [string] # p for public, f for friend based

Gossip weight: [float] # float between 0 and 1

Runs: [int] # integer number of simulation runs

Steps: [int] # integer number of timesteps

Patients: [int] # integer number of patients

Retailers: [int] # integer number of retailers

Suppliers: [int] # integer number of suppliers

Standard distance: [float] # float, smallest possible distance between patient and retailer

Retailer overhead: [int] # integer, inventory removed from retailer at the end of a round

Supplier overhead: [int] # integer, inventory removed from supplier at the end of a round

## 
