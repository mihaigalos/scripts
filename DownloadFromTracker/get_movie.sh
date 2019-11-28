#! /bin/bash
declare username=$1
declare password=$2
declare tracker=$3
declare movie="${@:4:99}"

movie=${movie// /+} # substitute spaces for plusses

echo curl --cookie-jar /tmp/tracker_cookies.txt --form username="$username" --form password="$password" "$tracker"
suggestions=$(curl -b /tmp/tracker_cookies.txt https://filelist.ro/browse.php?search=$movie&cat=0&searchin=1&sort=2)

torrent=$(echo $suggestions | sed -n 's/.*\(download.php?id=[0-9]*\).*/\1/p')
echo $torrent

