#!/bin/bash

for i in $(seq 21 50); do
    dir="Run$i"
    mkdir $dir
    cd $dir
    cp ../TrustModelFindGossip.py .
    cp ../singlesub . 
    cp ../findgossip_input . 
    sed -i "s/trust/trust$i/g" singlesub
    qsub singlesub
    cd ..
done

