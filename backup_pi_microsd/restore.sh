 #! /bin/bash
set -e
set -u
set -x

argc=$#
if [ "$#" -ne 2 ]; then
    echo "usage: ./restore.sh input_file output_device"
    exit 1
fi

input_file=$1
output_device=$2

echo Reading from $input_file and outputting to $output_device..

sudo dd if=$input_file | sudo pv | sudo dd of=$output_device
