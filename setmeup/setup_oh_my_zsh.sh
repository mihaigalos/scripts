#!/bin/bash

function setup_oh_my_zsh() {
    
    sudo apt update
    sudo apt -y install zsh

    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
    sed -i -e "s/ZSH_THEME.*//" ~/.zshrc
    wget https://gist.githubusercontent.com/mihaigalos/bde132c03ba2ae6a5f4d5c0cfedbcd61/raw/3fe5d6461005981bd529e124f728a88e5949063c/af-magic-time.zsh-theme -o ~/.oh-my-zsh/themes/af-magic-time.zsh-theme

    cat << EOF >> ~/.zshrc
ZSH_THEME="af-magic-time"
HISTFILE=~/.zsh_history
HISTSIZE=9999999
SAVEHIST=$HISTSIZE

export EDITOR=vim
export LC_ALL="en_US.UTF-8"

[ -x "\$(command -v exa)" ] && alias l='exa -all'

function cd {
    builtin cd "\$@" && l
}
EOF
}

setup_oh_my_zsh

