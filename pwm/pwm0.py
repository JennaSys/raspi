#!/usr/bin/python

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(24,GPIO.OUT)

pwm = GPIO.PWM(24, 100)
pwm.start(0)

while True:
	
    try:
        dc = raw_input('Enter a number between 0 and 100 (-1 to end): ')
        val = float(dc)
        if val < 0:
            break
        pwm.ChangeDutyCycle(val)
 
    except ValueError:
        print 'Bad number: "' + dc + '"'

pwm.stop()
GPIO.cleanup()
