#!/bin/sh

user=$1
endpoint=https://github.com

curl -s ${endpoint}/${user} | grep -- '<title>' | sed -e "s|.*<.*>\(.*\)</.*>|\1|" -e "s/[()]//g" | cut -d' ' -f1-3 | awk '{print  $1 " # " $2 " " $3}'
