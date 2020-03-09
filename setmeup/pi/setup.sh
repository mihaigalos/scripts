#!/bin/bash

rasperry_pi_model_file="/proc/device-tree/model"

function run_files_with_setup_prefix() {
    for file in ./setup_*
    do
        bash -c $file
    done
}

if [ -f "$rasperry_pi_model_file" ]; then
    if grep -q Raspberry "$rasperry_pi_model_file"
    then
        run_files_with_setup_prefix
    fi
fi

