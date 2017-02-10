#!/usr/bin/python

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(24, GPIO.IN)

try:
    while True:
        status = GPIO.input(24)
        if status:
            GPIO.output(17,True)
            sleep(0.2)
            GPIO.output(17,False)
            sleep(0.2)
        else:
            GPIO.output(17,True)
            sleep(1.0)
            GPIO.output(17,False)
            sleep(1.0)
            
except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
