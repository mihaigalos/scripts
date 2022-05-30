#!/bin/sh

github_page_of_user=$1

curl -s ${github_page_of_user} | grep -- '<title>' | sed -e "s|.*<.*>\(.*\)</.*>|\1|" -e "s/[()]//g" | cut -d' ' -f1-3 | awk '{print  $1 " # " $2 " " $3}'
