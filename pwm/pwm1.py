#!/usr/bin/python

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)

p = GPIO.PWM(17, 50)
p.start(100)

try:
    while True:
        for dc in range(100, -1, -5):
            p.ChangeDutyCycle(dc)
            sleep(0.1)
        for dc in range(0, 101, 5):
            p.ChangeDutyCycle(dc)
            sleep(0.1)
 
except KeyboardInterrupt:
    pass

finally:
    p.stop()
    GPIO.cleanup()
    
