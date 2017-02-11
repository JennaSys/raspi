#!/usr/bin/python

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.OUT) #Segment A
GPIO.setup(3,GPIO.OUT) #Segment B
GPIO.setup(4,GPIO.OUT) #Segment C
GPIO.setup(17,GPIO.OUT) #Segment D
GPIO.setup(27,GPIO.OUT) #Segment E
GPIO.setup(22,GPIO.OUT) #Segment F
GPIO.setup(10,GPIO.OUT) #Segment G
GPIO.setup(9,GPIO.OUT) #Decimal Point

segments = (2,3,4,17,27,22,10,9)
try:
    while True:
        for x in range(8):
            GPIO.output(segments[x],False)
            sleep(1.0)
            GPIO.output(segments[x],True)

except KeyboardInterrupt:
    GPIO.cleanup()
    
