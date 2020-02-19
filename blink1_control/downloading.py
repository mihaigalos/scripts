import re
import os
from os.path import expanduser
import subprocess

home = expanduser("~")
kBlinkOneTool = home+"/git/utils/blink1_control/blink1-tool"


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

def blink_14_times_a_4_seconds():
    command = "sudo "+kBlinkOneTool + \
        " --led=2 --green --blink 20 --delay 1500 --millis 1500 > /dev/null"
    os.system(command)

if TranmissionProvider().is_active_download():
    blink_14_times_a_4_seconds()
