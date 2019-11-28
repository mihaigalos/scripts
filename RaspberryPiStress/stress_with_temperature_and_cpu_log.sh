#!/bin/bash

homedir=~
eval homedir=$homedir
log_folder=$homedir"/logs" 

echo "Stresstest for Raspberry Pi, 20 minutes."
echo "Starting to record the temperature"
timestamp=`date +%F_%H-%M-%S`
echo "Writing into $log_folder/temperature_log_$timestamp.txt"
echo "Temperature and CPU Log - $(date)" > $log_folder/temperature_log_$timestamp.txt

stress-ng -c 4 --metrics --timeout 1200s & #20 minutes

for i in {1..40}
do
    temp=$(paste <(cat /sys/class/thermal/thermal_zone*/type) <(cat /sys/class/thermal/thermal_zone*/temp) | column -s $'\t' -t | sed 's/\(.\)..$/.\1°C/')
    cpu=$(cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq)
    echo  $temp >>~/logs/temperature_log_$timestamp.txt
    echo "CPU: $cpu" >> ~/logs/temperature_log_$timestamp.txt
    echo "" >>~/logs/temperature_log_$timestamp.txt
    echo "Current temperature: #$i: $temp"
    echo "CPU: $cpu"
    echo ""
    sleep 30
done
