#!/bin/bash

function setup_vim() {
    sudo apt install vim

    mkdir -p ~/.vim/colors
    pushd ~/.vim/colors
    wget https://raw.githubusercontent.com/mihaigalos/molokai/master/colors/molokai.vim
    popd
    
    pushd ~
    wget https://raw.githubusercontent.com/mihaigalos/utils/master/setmeup/.vimrc
    popd
}

setup_vim
