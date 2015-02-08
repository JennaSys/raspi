#!/usr/bin/python

import RPi.GPIO as GPIO
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Quit btn

while True:
    status = GPIO.input(24)
    if status:
        print "\nQuitter!"
        GPIO.cleanup()
        sys.exit()

