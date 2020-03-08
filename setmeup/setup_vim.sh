#!/bin/bash

function setup_vim() {
    mkdir -p ~/.vim/colors
    pushd ~/.vim/colors
    https://raw.githubusercontent.com/mihaigalos/molokai/master/colors/molokai.vim
    popd
    
    pushd ~
    wget https://raw.githubusercontent.com/mihaigalos/utils/master/setmeup/.vimrc
    popd
}

setup_vim
