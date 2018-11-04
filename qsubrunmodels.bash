#!/bin/bash

find . -name "Run*" -type d -print -exec rm -rf {} +

for d in */ ; do
    cd $d
    echo $d
    rm TrustModel.py
    cp ../TrustModel.py .
    rm singlesub
    cp ../singlesub .
    result=${PWD##*/} 
    echo $result
    sed -i "s/trust/trust$result/g" singlesub
    qsub singlesub
    cd ..
done
