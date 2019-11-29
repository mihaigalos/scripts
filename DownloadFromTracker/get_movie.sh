#! /bin/bash

username=$1
password=$2
tracker=$3
movie="${@:4:99}"

temp_folder="/mnt/Vera_SeagateC/incomplete" # no use of mktemp since not encrypted

movie=${movie// /+} # substitute spaces for plusses

curl --silent --cookie-jar "$temp_folder/tracker_cookies.txt" --form username="$username" --form password="$password" "$tracker"/takelogin.php
suggestions=$(curl --silent -b "$temp_folder/tracker_cookies.txt" "$tracker"/browse.php?search=$movie&cat=0&searchin=1&sort=1)

choice=`echo "$suggestions" \
| sed -e "s/href='details.php?/\n/g" \
| sed -e "s/<\/b><\/a>/\n/g" \
| grep -P "^id=[0-9]+'" \
| sed -e "s/id=//g" -e "s/'//g" -e "s/title=\(.*\)/\"\1\"/g" -e "s/><b>.*\"/\"/" \
| xargs dialog --stdout --clear --backtitle "Backtitle here" --title "Get movie" --menu "Choose one of the following options:" 15 60 10`

torrent="$tracker/download.php?id=$choice"
curl --silent -b "$temp_folder/tracker_cookies.txt" "$torrent" > "$temp_folder"/new_torrent.torrent

transmission-remote localhost:9091 -a "$temp_folder"/new_torrent.torrent
