# MedicalTrustModel

Cara Lynch

Created October 2018, last modified 11/11/2018 17:26

## Overview
Simple model describing the evolution of trust in medicine, based on previous work by Graeme Ackland, incorporating two gossip modes.

## Models
- TrustModel.py: Standard model, with different gossip and trust modes.
- TrustModelFindGossip.py: Modified model, running simulations for one set of retailers and suppliers while iterating over gossip values. Aims to assess the effects of gossip on quality and price.

## Input files
- standard_input : input for TrustModel.py, see file for formatting
- findgossip_input : input for TrustModelFindGossip.py, see file for formatting

## Plotting Scripts
- QvsGplotter.py : plots Quality vs Gossip weight with data files produced by simplotter.py, requires file names as command line input
- allplotter.py : plots average Quality, Price and Quality/Price over time with data files produced by simplotter.py, requires file names as command line input
- findgossgrapher.py : plots Quality Improvement = Q(gossip weight)/Q(no gossip) and Price Improvement = P(gossip weight)/P(no gossip) vs gossip weight, for all TrustModelFindGossip.py runs in directory. Also plots Quality and Price vs Gossip Weight for each run.
- simplotter.py : plots quality, price and quality/price vs gossip weight for all runs and averaged over all runs
## Other scripts
- directories.py : makes directories with required input files
- qsubrungossmodels.bash : queues all jobs in directory to local cluster for a TrustModelFindGossip.py simulation. Requires subdirectories with input files, singlesub (appropriately modified), and TrustModelFindGossip.py in directory
- qsubrunmodels.bash : same as above, but for standard TrustModel.py jobs
- runmodels.bash : runs all jobs in directory on local machine
- singlesub : single submission to local cluste, must be in relevant subdirectory


