#!/bin/bash

find . -name "RetailerData" -type d -print -exec rm -rf {} +
find . -name "SupplierData" -type d -print -exec rm -rf {} +
find . -name "AllRuns*" -type f  -print -exec rm -rf {} +

for d in */ ; do
    cd $d
    rm simplotter.py
    echo "simplotter removed"
    cp ../simplotter.py .
    nohup python simplotter.py 0 &
    cd ..
done
