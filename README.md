# MedicalTrustModel

Cara Lynch

Created October 2018, last modified 24/11/2018 18:40

## Overview
Simple agent-based model (ABM) of a self-organising pharmaceutical supply chain with variable drug quality, based on previous work by Graeme Ackland. This model incorporates two gossip modes, public and friendly.

## Model scripts
- TrustModel.py: standard python script to run the ABM, requires an input file name as a command line argument. The input file must be in standard_input format.


- TrustModelFindGossip.py: modified model written to specifically assess the effects of gossip on the system. No input file required, this script runs simulations for one set of retailers and suppliers while changing gossip and trust values. To perform more than one run, qsubrungossmodels.bash and Gsinglesub are required.

## Input file
- standard_input : input for TrustModel.py, see file for formatting

## Plotting scripts
- grapher.py : plots data from TrustModelFindGossip.py runs, designed to be in parent directory (where qsubrungossmodels.bash is, with Run1 as subdirectory).
- simplotter.py: plots data from TrustModel.py, designed to be in directory where TrustModel.py ran.

## Other scripts
- qsubrungossmodels.bash : makes a directory for the number of runs specified (usually 100), copies TrustModelFindGossip.py and Gsinglesub into each directory and queues all jobs to the local cluster. Requires Gsinglesub and TrustModelFindGossip.py in directory.
- qsubrunmodels.bash : copies and queues all TrustModel.py jobs in subdirectories. Requires subdirectories and standard_input files in each subdirectory, as well as TrustModel.py in directory. Low number of runs in TrustModel.py is recommended to have time to finish, as each run will be running consecutively rather than me sent as different jobs to different cores.
- runmodels.bash : copies TrustModel.py into each subdirectory and launches in background on local machine. Requires TrustModel.py in directory and standard_input files in subdirectories
- singlesub and Gsinglesub: single submission scripts to local cluster, must be in relevant subdirectory. singlesub is for TrustModel.py jobs while Gsinglesub is for TrustModelFindGossip.py jobs.

## plots directory
Contains plots produced by grapher.py from TrustModelFindGossip.py runs.

Different modes:
- Gf or Gp: friendly (f) or public (p) gossip on with gossip weight 10.0, patient trust weight 0.0, retailer trust weight 0.0, price off
- T: trust on with trust weight 10.0 (for patients and retailers), gossip weight 0.0, price off
- P: only price, with trust and gossip off
- GTf or GTp: trust and gossip on in friend (f) or public (p) mode, with trust and gossip weights 10.0 while price is off


Different graphs:
- Bankruptcies.png: plot of average number of bankruptcies over 100 runs over step number.
- Minvs.png: final supplier inventories for mode M, where M is one of the modes above, averaged over 200 runs.
- MQvsN.png: Average quality of medicine (averaged over all patients or retailers) over 200 runs, for patients in blue and retailers in red, for mode M.
- Qvstime.png: Average quality of medicine bought by patients over 200 runs, with all modes shown.
- QEndvstime2.png: The above plot without the price mode, only over the last 200 timesteps.
- Qvstimefit.png: An attempt to fit Qvstime for T, Gf and Gp, with a fit A-Bexp(x/C) with A, B and C fitted parameters.
- Qdiff.png: graph of Qmax-Q over time with Qmax set as the maximum average value of quality of medicine bought by patients (the value at timestep 400) and Q the average value of quality of medicine.
- Qdifffits.png: attempt to fit the above graph with A-Bexp(x/C).
- Qdifflog.png: Qdiff.png plot with a log scale on the y axis.
- Qdiffzoom.png: Qdiff.png plot over the last 200 timesteps.
- Pvstime.png: Average price of medicine bought by patients over 200 runs, with all modes shown.