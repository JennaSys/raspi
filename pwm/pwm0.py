#!/usr/bin/python

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)

p = GPIO.PWM(17, 50)
p.start(100)

while True:
	
    try:
        dc = raw_input('Enter a number between 0 and 100: ')
        val = float(dc)
        if val < 0:
            break
        p.ChangeDutyCycle(val)
 
    except ValueError:
        print 'Bad number: "' + dc + '"'

p.stop()
GPIO.cleanup()
