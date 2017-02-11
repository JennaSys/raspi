#!/usr/bin/python

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(24,GPIO.OUT)
GPIO.output(24, False)

status = False

try:
    while True:
        GPIO.output(24, status)
        raw_input('Press [Enter] to toggle relay ' + ('Off' if status else 'On'))
        status = not status

except KeyboardInterrupt:
    GPIO.cleanup()

