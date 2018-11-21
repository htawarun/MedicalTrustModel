# MedicalTrustModel

Cara Lynch

Created October 2018, last modified 21/11/2018 16:06

## Overview
Simple agent-based model (ABM) of a self-organising pharmaceutical supply chain with variable drug quality, based on previous work by Graeme Ackland. This model incorporates two gossip modes, public and friendly.

## Model scripts
- TrustModel.py: standard python script to run the ABM, requires an input file name as a command line argument. The input file must be in standard_input format.


- TrustModelFindGossip.py: modified model written to specifically assess the effects of gossip on the system. No input file required, this script runs simulations for one set of retailers and suppliers while changing gossip and trust values. To perform more than one run, qsubrungossmodels.bash and Gsinglesub are required.

## Input file
- standard_input : input for TrustModel.py, see file for formatting

## Plotting Script
- grapher.py : plots data from TrustModelFindGossip.py runs, designed to be in parent directory (where qsubrungossmodels.bash is, with Run1 as subdirectory).

## Other scripts
- qsubrungossmodels.bash : makes a directory for the number of runs specified (usually 100), copies TrustModelFindGossip.py and Gsinglesub into each directory and queues all jobs to the local cluster. Requires Gsinglesub and TrustModelFindGossip.py in directory.
- qsubrunmodels.bash : copies and queues all TrustModel.py jobs in subdirectories. Requires subdirectories and standard_input files in each subdirectory, as well as TrustModel.py in directory. Low number of runs in TrustModel.py is recommended to have time to finish, as each run will be running consecutively rather than me sent as different jobs to different cores.
- runmodels.bash : copies TrustModel.py into each subdirectory and launches in background on local machine. Requires TrustModel.py in directory and standard_input files in subdirectories
- singlesub and Gsinglesub: single submission scripts to local cluster, must be in relevant subdirectory. singlesub is for TrustModel.py jobs while Gsinglesub is for TrustModelFindGossip.py jobs.


