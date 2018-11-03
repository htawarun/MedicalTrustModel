#!/bin/bash

find . -name "Run*" -type d -print -exec rm -rf {} +

for d in */ ; do
    cd $d
    rm TrustModel.py
    echo "TrustModel removed"
    cp ../TrustModel.py .
    cp ../singlesub .
    sed -i "s/trust/trust$d/g" singlesub
    qsub singlesub
    cd ..
done
