#! /bin/sh

cat <<EOF >/etc/systemd/system/connect_to_hidden_wifi.service

[Unit]
Description=Manually connect to hidden WiFi

[Service]
ExecStart=nmcli c up id "Ye Olde Internet"
Type=oneshot
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target

EOF
