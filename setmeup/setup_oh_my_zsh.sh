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

unalias gp &>/dev/null || true
function gp() {
    declare branch origin param
    declare -a gp_opts=()
    while param="${1:-}"; [[ -n "$param" ]]; do
        [[ "$param" == -* ]] || break
        shift
        gp_opts+=("$param")
    done
    origin="${1:-$(git config --get branch.master.remote)}" || return 1
    branch="${2:-$(git rev-parse --abbrev-ref HEAD)}" || return 1
    if ! git rev-parse --abbrev-ref --symbolic-full-name '@{u}' &>/dev/null; then
        gp_opts+=(-u)
    fi
    gp_opts+=("$origin" "$branch")
    echo git push "${gp_opts[@]}"
    git push "${gp_opts[@]}"
    last_commit_message=$(git reflog -1 | sed 's/^.*: //')
    hub pull-request -F- <<<"WIP $last_commit_message"
}

EOF
}

setup_oh_my_zsh

