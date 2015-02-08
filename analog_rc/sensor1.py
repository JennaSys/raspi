#!/usr/bin/python

import RPi.GPIO as GPIO
from time import sleep

pin_charge = 22
pin_test= 23

GPIO.setmode(GPIO.BCM)

try:
    while True:
        #Discharge
        GPIO.setup(pin_charge, GPIO.IN)
        GPIO.setup(pin_test, GPIO.OUT)
        GPIO.output(pin_test, False)
        sleep(0.1)
        
        #Charge
        GPIO.setup(pin_charge, GPIO.OUT)
        GPIO.setup(pin_test, GPIO.IN)
        count = 0
        GPIO.output(pin_charge, True)
        while not GPIO.input(pin_test):
            count += 1
        print(count)
		
except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
    
