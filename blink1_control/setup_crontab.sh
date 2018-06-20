#!/usr/bin/bash

(crontab -l 2>/dev/null; echo "*/10 * * * * python ~/git/blink1_control/flash_blink1_on_ip_change.py >/dev/null 2>&1")| crontab - 