#!/bin/bash

find . -name "Run*" -type d -print -exec rm -rf {} +
find . -name "standard_input" -type f -print -exec sed -i '/Gossip weight/c\Gossip weight: 0.5' {} \; -exec sed -i '/Trust weight/c\Trust weight: 0.5' {} \; -exec sed -i '/Supplier overhead/c\Supplier overhead: 5' {} \; 

for d in */ ; do
    cd $d
    rm TrustModel.py
    echo "TrustModel removed"
    cp ../TrustModel.py .
    nohup python TrustModel.py standard_input &
    cd ..
done
