#!/bin/bash

function setup_veracrypt() {
    sudo apt-get update
    sudo apt-get install -y libfuse-dev makeself libwxbase3.0-0v5
    mkdir -p veracryptfiles
    cd veracryptfiles
    
    wget -L -O veracrypt-1.21-raspbian-setup.tar.bz2 https://launchpad.net/veracrypt/trunk/1.21/+download/veracrypt-1.21-raspbian-setup.tar.bz2
    tar -xvf ./veracrypt-*-setup.tar.bz2
    chmod +x veracrypt-*-setup-*
    ./veracrypt-*-setup-console-armv7
    
    cd -
    rm -rf veracryptfiles
}

setup_veracrypt
