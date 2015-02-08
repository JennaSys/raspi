#!/usr/bin/python

import RPi.GPIO as GPIO
from time import sleep
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Quit btn

def cb_quit(channel):
	GPIO.cleanup()
	print "All Done!"
	sys.exit()

GPIO.add_event_detect(24, GPIO.RISING, callback=cb_quit, bouncetime=50)	
print "Running..."

try:
    while True:
        GPIO.output(17,True)
        sleep(1.0)
        GPIO.output(17,False)
        sleep(1.0)
        
except KeyboardInterrupt:
	print "\nQuitter!"
	sleep(2)
			
finally:
	GPIO.cleanup()
    
    
