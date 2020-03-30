import re
import os
from os.path import expanduser
import subprocess

home = expanduser("~")
kBlinkOneTool = home+"/git/utils/blink1_control/blink1-tool"

class SystemProvider():
    def get_speed(self):
        bashCommand = "sudo /usr/sbin/iftop -B -t -s 1 2>/dev/null | grep Total\ receive\ rate: | awk '{print $4}'"
        output, error = subprocess.Popen(
                bashCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            ).communicate()
        return self.to_bytes(output)

    def to_bytes(self, input):
        units = {"B": 1, "KB": 2**10, "MB": 2**20, "GB": 2**30, "TB": 2**40}
        input = input.upper()
        if not re.match(r' ', input):
            input = re.sub(r'([KMGT]?B)', r' \1', input)
        number, unit = [string.strip() for string in input.split()]
        return int(float(number)*units[unit])


class TranmissionProvider():
    def get(self):
        for status in ["Downloading"]:
            bashCommand = "transmission-remote  192.168.0.101:9091 -l | head -n -1 | grep " + \
                status + " | wc -l"

            output, error = subprocess.Popen(
                bashCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            ).communicate()

            count = int(output)

        return count

    def is_active_download(self):
        downloads = self.get()
        if downloads > 0:
            return True
        return False

def flash_led(times, delay, color):
    command = "sudo "+kBlinkOneTool + \
        " --led=2 --"+color+" --blink "+str(times)+" --delay "+str(delay)+" --millis 1500 > /dev/null"
    os.system(command)

def get_color_for_speed(speed):
    speed=int(speed)
    if speed<500000:
        return "red"
    elif speed < 1500000:
        return "yellow"
    else:
        return "green"

speed_bytes_per_second=SystemProvider().get_speed()
color=get_color_for_speed(speed_bytes_per_second)

if TranmissionProvider().is_active_download():
    flash_led(times=20, delay=1500, color=color)

