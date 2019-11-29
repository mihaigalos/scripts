#! /bin/bash
declare username=$1
declare password=$2
declare tracker=$3
declare movie="${@:4:99}"

movie=${movie// /+} # substitute spaces for plusses

curl --silent --cookie-jar /tmp/tracker_cookies.txt --form username="$username" --form password="$password" "$tracker"/takelogin.php
suggestions=$(curl --silent -b /tmp/tracker_cookies.txt "$tracker"/browse.php?search=$movie&cat=0&searchin=1&sort=1)

choice=`echo "$suggestions" \
| sed -e "s/href='details.php?/\n/g" \
| sed -e "s/<\/b><\/a>/\n/g" \
| grep -P "^id=[0-9]+'" \
| sed -e "s/id=//g" -e "s/'//g" -e "s/title=\(.*\)/\"\1\"/g" -e "s/><b>.*\"/\"/" \
| xargs dialog --stdout --clear --backtitle "Backtitle here" --title "Title here" --menu "Choose one of the following options:" 15 60 4`

torrent="$tracker/download.php?id=$choice"
curl --silent -b /tmp/tracker_cookies.txt "$torrent" > /tmp/new_torrent.torrent

transmission-remote localhost:9091 -a /tmp/new_torrent.torrent
