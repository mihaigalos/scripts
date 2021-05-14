#! /bin/sh

cat <<EOF >/lib/systemd/system/connect_to_hidden_wifi.service

[Unit]
Description=Manually connect to hidden WiFi
Before=network.target
After=dbus.service

[Service]
ExecStart=nmcli c up id "Ye Olde Internet"
Type=oneshot
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target

EOF

systemctl enable connect_to_hidden_wifi.service
