#!/bin/bash

for file in ./setup_*
do
    bash -c $file
done

pushd pi
./setup.sh
popd

