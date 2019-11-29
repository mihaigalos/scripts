#!/bin/bash

set -euxo pipefail

script_path=$(dirname $(readlink -f `which invoke_get_movie.sh`))
username=`sudo cat "$script_path/user"`
password=`sudo cat "$script_path/pass"`
tracker=`sudo cat "$script_path/tracker"`

"$script_path"/get_movie.sh $username $password $tracker "$*"
