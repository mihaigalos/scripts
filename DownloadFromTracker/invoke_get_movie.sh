#!/bin/bash

set -euxo pipefail

username=`sudo cat user`
password=`sudo cat pass`
tracker=`sudo cat tracker`

./get_movie.sh $username $password $tracker "$*"
