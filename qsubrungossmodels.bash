#!/bin/bash

for i in $(seq 1 100); do
    dir="Run$i"
    mkdir $dir
    cd $dir
    cp ../TrustModelFindGossip.py .
    cp ../Gsinglesub . 
    sed -i "s/trust/trust$i/g" Gsinglesub
    qsub Gsinglesub
    cd ..
done

