#! /bin/bash

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 folder port user pass"
    exit 1
fi

folder=$(realpath $1)
port=$2
user=$3
pass=$4
#using tmux to keep server up after ssh close.

tmux new-session -d -s "httpServerSession" -- docker run --rm -it -p "$port":8000 -v "$folder":/share -w="/share" python_https_server /bin/bash -c 'python3 /https_server.py $(realpath .) 8000 /server_certificate.pem '"$user:$pass"
