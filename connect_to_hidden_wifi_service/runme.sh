#! /bin/sh

set -xuoe

uid_of_wifi=$(nmcli connection show | head -2 | tail -1 | sed 's/   */:/g'| cut -d ":" -f2)
echo $uid_of_wifi | xargs nmcli connection modify -I {} wifi.hidden yes
sudo service network-manager restart
