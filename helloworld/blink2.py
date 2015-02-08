#!/usr/bin/python

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)

try:
    while True:
        GPIO.output(17,False)
        sleep(1.0)
        GPIO.output(17,True)
        sleep(1.0)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
    
