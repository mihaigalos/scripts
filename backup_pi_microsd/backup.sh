#! /bin/bash
set -e
set -u
set -x

# Get pishrink as prerequisite
wget -nc https://raw.githubusercontent.com/Drewsif/PiShrink/master/pishrink.sh
sudo chmod a+x pishrink.sh

date_suffix=$(date +%y%m%d) 
output_filename=pi_$date_suffix.img

echo "Dumping microSD contents.."
sudo dd if=/dev/sdc | pv | dd of=pi_backup.img

echo "Shrinking and producing final image.."
sudo ./pishrink.sh -s pi_backup.img $output_filename

echo "Removing initial image dump.."
rm pi_backup.img

echo "Done. Written file: $output_filename"
