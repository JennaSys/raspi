#!/usr/bin/python

import RPi.GPIO as GPIO
from time import sleep
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)  #LED
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Alt btn
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Quit btn

cur_speed = 1.0

def cb_quit(channel):
	GPIO.cleanup()
	sys.exit()

def cb_alt(channel):
	global cur_speed
	
	if GPIO.input(channel):
		print "ON"
		cur_speed = 0.25
	else:
		print "off"
		cur_speed = 1.0
	
def blink():
	GPIO.output(17, True)
	sleep(cur_speed)
	GPIO.output(17, False)
	sleep(cur_speed)
	

GPIO.add_event_detect(24, GPIO.RISING, callback=cb_quit, bouncetime=50)	
GPIO.add_event_detect(23, GPIO.BOTH, callback=cb_alt, bouncetime=50)	

try:
	while True:
		blink()
		
except KeyboardInterrupt:
	print "\nQuitter!"
	sleep(2)
			
finally:
	GPIO.cleanup()
		
	
