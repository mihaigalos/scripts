#!/bin/bash

folder=$(pwd)

(crontab -l 2>/dev/null; echo "*/5 * * * * python ${folder}/flash_blink1_on_ip_change.py >/dev/null 2>&1") | crontab -
(crontab -l 2>/dev/null; echo "*/5 * * * * python ${folder}/no_vpn.py >/dev/null 2>&1") | crontab -
(crontab -l 2>/dev/null; echo "*/1 * * * * python ${folder}/downloading.py >/dev/null 2>&1") | crontab -
