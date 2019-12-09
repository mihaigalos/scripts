#! /bin/bash

folder=$(realpath $1)
port=$2

#using tmux to keep server up after ssh close.

tmux new-session -d -s "httpServerSession" -- docker run --rm -it -p "$port":8000 -v "$folder":/share -w="/share" python_http_server
