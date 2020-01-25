#!/bin/bash

(crontab -l 2>/dev/null; echo "*/5 * * * * python ~/git/utils/blink1_control/flash_blink1_on_ip_change.py >/dev/null 2>&1") | crontab -
(crontab -l 2>/dev/null; echo "*/5 * * * * python ~/git/utils/blink1_control/no_vpn.py >/dev/null 2>&1") | crontab -
(crontab -l 2>/dev/null; echo "*/1 * * * * python ~/git/utils/blink1_control/downloading.py >/dev/null 2>&1") | crontab -
