#!/usr/bin/python

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.OUT)
GPIO.setup(3,GPIO.OUT)
GPIO.setup(4,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
GPIO.setup(10,GPIO.OUT)
GPIO.setup(9,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)

segments = (2,3,4,17,27,22,10,9,11)
try:
    while True:
        for x in range(8):
            GPIO.output(segments[x],False)
            sleep(1.0)
            GPIO.output(segments[x],True)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
    
