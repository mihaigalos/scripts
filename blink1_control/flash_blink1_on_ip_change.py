import os
from os.path import expanduser
from subprocess import Popen, PIPE

home = expanduser("~")
kCurrentIpFile = home+"/git/blink1_control/currentIp.txt"
kBlinkOneTool = home+"/git/blink1_control/blink1-tool"

def currentIp():
	get_ip_command = "curl -s icanhazip.com"
	p = Popen(get_ip_command.split(), stdout=PIPE)
	stdout = p.communicate()[0].strip()
	p.wait()
	return stdout

def writeCurrentIp(currentIp, currentIpFile=kCurrentIpFile):
	file = open(currentIpFile, "w")
	file.write(currentIp)
	file.close()

def getLastIp(currentIpFile=kCurrentIpFile):
	if os.path.isfile(kCurrentIpFile):
		file = open(currentIpFile, "r")
		return  file.readline()
	else:
		return "0"

currentIp = currentIp()
lastKnownIp = getLastIp()

if currentIp == lastKnownIp:
	pass
else:
	writeCurrentIp(currentIp)
	command = "sudo "+kBlinkOneTool+"  --magenta --millis=2000 --flash -1 --delay=2000 > /dev/null &"
	os.system(command)

