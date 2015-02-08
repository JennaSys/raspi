#!/usr/bin/python

import RPi.GPIO as GPIO
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN)  #Quit btn

print "Running..."
while True:
    status = GPIO.input(24)
    if status:
        print "\nQuitter!"
        break
GPIO.cleanup()
