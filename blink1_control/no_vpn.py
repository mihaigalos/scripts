import re
import os
from os.path import expanduser
from subprocess import Popen, PIPE

home = expanduser("~")
kBlinkOneTool = home+"/git/blink1_control/blink1-tool"

def is_vpn_active():
        vpn_status_command = "windscribe status"
        p = Popen(vpn_status_command.split(), stdout=PIPE)
        stdout = p.communicate()[0].strip()
        p.wait()
	
	last_line = stdout.splitlines()[-1]
	m = re.search('^CONNECTED', last_line)
	status = False	
	
	if m is not None:
		status = True
	
	return status

if is_vpn_active():
	pass
else:
	command = "sudo "+kBlinkOneTool+" --led=1 --blue --millis=2000 --flash -1 --led=1 --delay=2000 > /dev/null &"
	os.system(command)

