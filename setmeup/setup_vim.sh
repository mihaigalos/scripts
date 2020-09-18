#!/bin/bash

function setup_vim_go_to_linenumber() {
    # allows for syntax: vim file.log:123

    git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim

    cat <<EOF >> ~/.vimrc

""""""""""""""""""""""""""""Vundle Config""""""""""""""""""""""""""""
set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
"Plugin 'VundleVim/Vundle.vim'
Plugin 'wsdjeg/vim-fetch'

Plugin 'tpope/vim-fugitive'
Plugin 'git://git.wincent.com/command-t.git'
Plugin 'rstacruz/sparkup', {'rtp': 'vim/'}

" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required
" To ignore plugin indent changes, instead use:
"filetype plugin on
"
" Brief help
" :PluginList       - lists configured plugins
" :PluginInstall    - installs plugins; append `!` to update or just :PluginUpdate
" :PluginSearch foo - searches for foo; append `!` to refresh local cache
" :PluginClean      - confirms removal of unused plugins; append `!` to auto-approve removal
"
" see :h vundle for more details or wiki for FAQ
" Put your non-Plugin stuff after this line

""""""""""""""""""""""""""""End of Vundle Config""""""""""""""""""""""""""""
EOF

    vim +PluginInstall +qall
}

function setup_vim() {
    sudo apt install vim

    mkdir -p ~/.vim/colors
    pushd ~/.vim/colors
    wget https://raw.githubusercontent.com/mihaigalos/onedark.vim/master/colors/onedark.vim
    popd

    mkdir -p ~/.vim/autoload
    pushd ~/.vim/autoload
    wget https://raw.githubusercontent.com/mihaigalos/onedark.vim/master/autoload/onedark.vim
    popd
    
    pushd ~
    wget https://raw.githubusercontent.com/mihaigalos/utils/master/setmeup/.vimrc
    popd

    setup_vim_go_to_linenumber
}

setup_vim
