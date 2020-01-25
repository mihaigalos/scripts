import re
import os
from os.path import expanduser
import subprocess

home = expanduser("~")
kBlinkOneTool = home+"/git/blink1_control/blink1-tool"


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


if TranmissionProvider().is_active_download():
    command = "sudo "+kBlinkOneTool + \
        " --led=2 --green --blink 1 --delay 2000 --millis 5000 > /dev/null &"
    os.system(command)
