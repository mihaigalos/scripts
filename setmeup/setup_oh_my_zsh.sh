#!/bin/bash

function setup_oh_my_zsh() {
    
    sudo apt update
    sudo apt -y install zsh

    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

    cat << EOF >> ~/.zshrc
HISTFILE=~/.zsh_history
HISTSIZE=9999999
SAVEHIST=$HISTSIZE

export EDITOR=vim
export LC_ALL="en_US.UTF-8"

function cd {
    builtin cd "\$@" && l
}
EOF
}

setup_oh_my_zsh

