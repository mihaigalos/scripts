#!/bin/bash

function setup_log2ram() {
    curl -Lo log2ram.tar.gz https://github.com/azlux/log2ram/archive/master.tar.gz
    tar xf log2ram.tar.gz
    cd log2ram-master
    chmod +x install.sh && sudo ./install.sh
    cd ..
    rm -r log2ram-master
}

setup_log2ram
