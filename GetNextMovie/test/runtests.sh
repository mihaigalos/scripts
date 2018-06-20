#!/usr/bin/bash

pushd ../
echo
python -m unittest discover -v
find . -name "*.pyc" -exec rm -f {} \;
popd
echo 
