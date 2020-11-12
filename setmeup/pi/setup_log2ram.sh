#!/bin/bash

function setup_log2ram() {
    wget -qO - https://github.com/azlux/log2ram/archive/master.tar.gz | tar zxvf -
    cd log2ram-master
    chmod +x install.sh && sudo ./install.sh
    cd ..
    rm -r log2ram-master
}

setup_log2ram
