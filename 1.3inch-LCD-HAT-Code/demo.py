# -*- coding:utf-8 -*-

from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.core import lib

from luma.oled.device import sh1106
import RPi.GPIO as GPIO

import time
import subprocess

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def getFredDiskUsage(drive):
	cmd =  "ssh osmc@192.168.0.101 'df -h' | grep " + drive
        command_result = subprocess.check_output(cmd, shell = True )
	elements=command_result.split()

	total_size=elements[1]
	used_size=elements[2]
	used_percentage=elements[4]
	path=elements[5][elements[5].find("/", 1)+1:]
	path=path[-1:]

	return path +": "+str(used_size)+"/"+str(total_size)+" "+str(used_percentage)


# Load default font.
font = ImageFont.load_default()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = 128
height = 64
image = Image.new('1', (width, height))

# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

RST = 25
CS = 8
DC = 24

USER_I2C = 0

if  USER_I2C == 1:
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(RST,GPIO.OUT)
	GPIO.output(RST,GPIO.HIGH)

	serial = i2c(port=1, address=0x3c)
else:
	serial = spi(device=0, port=0, bus_speed_hz = 8000000, transfer_size = 4096, gpio_DC = 24, gpio_RST = 25)

device = sh1106(serial, rotate=2) #sh1106

try:
	while True:
		with canvas(device) as draw:

			#draw.rectangle(device.bounding_box, outline="black", fill="black")
			#draw.text((30, 40), "Hello World", fill="white")
			# Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
			#cmd = "hostname -I | cut -d\' \' -f1"
			#IP = subprocess.check_output(cmd, shell = True )
			cmd =  "top -bn2 | grep '%Cpu' | tail -1 | grep -Poh '([0-9.]*) us' | head -c 4"

			CPU = subprocess.check_output(cmd, shell = True )
			CPU = "CPU Load: " +str(CPU).strip()+"%"
			cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
			MemUsage = subprocess.check_output(cmd, shell = True )
			cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
			Disk = subprocess.check_output(cmd, shell = True )

			cmd = "python /home/mihai/scripts/mvg/getMVGInfo_Petuelring_U3.py"
			MvgInfo=subprocess.check_output(cmd, shell = True )

			# Write two lines of text.
			draw.text((x, top),    str(MvgInfo),  font=font, fill=255)

			cmd = "python /home/mihai/scripts/mvg/getMVGInfo_Milbertshofen_U2.py"
			MvgInfo_U2=subprocess.check_output(cmd, shell = True )

			cmd = "python /home/mihai/scripts/google/getTimeToWork.py"
			time_to_work=subprocess.check_output(cmd, shell = True )

			draw.text((x+6*8, top),    str(MvgInfo_U2),  font=font, fill=255)
			draw.text((x, top+8),    str("Mins to work: ")+str(time_to_work)+".",  font=font, fill=255)

			#draw.text((x, top),       "IP: " + str(IP),  font=font, fill=255)
			draw.text((x, top+16),     str(CPU), font=font, fill=255)
			draw.text((x, top+25),    str(MemUsage),  font=font, fill=255)
			draw.text((x, top+33),    str(Disk),  font=font, fill=255)
			#draw.text((x, top+33),    str(MvgInfo),  font=font, fill=255)
			draw.text((x, top+41),    getFredDiskUsage("SeagateA"),  font=font, fill=255)
			draw.text((x, top+49),    getFredDiskUsage("SeagateB"),  font=font, fill=255)
			time.sleep(30)
except Exception as e:
	print(e)
GPIO.cleanup()
