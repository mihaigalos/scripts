#! /bin/bash
declare username=$1
declare password=$2
declare tracker=$3
declare movie="${@:4:99}"

movie=${movie// /+} # substitute spaces for plusses

curl --silent --cookie-jar /tmp/tracker_cookies.txt --form username="$username" --form password="$password" "$tracker"/takelogin.php
suggestions=$(curl --silent -b /tmp/tracker_cookies.txt "$tracker"/browse.php?search=$movie&cat=0&searchin=1&sort=1)

torrent=$(echo $suggestions | sed -n 's/.*\(download.php?id=[0-9]*\).*/\1/p')
echo $torrent
curl --silent -b /tmp/tracker_cookies.txt "$tracker"/$torrent > /tmp/new_torrent.torrent

transmission-remote localhost:9091 -a /tmp/new_torrent.torrent 

