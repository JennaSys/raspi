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
digits = [(0,1,2,3,4,5),
          (1,2),
          (0,1,3,4,6),
          (0,1,2,3,6),
          (1,2,5,6),
          (0,2,3,5,6),
          (0,2,3,4,5,6),
          (0,1,2),
          (0,1,2,3,4,5,6),
          (0,1,2,3,5,6)]

def clear_digit():
    #turn off all segments
    for segment in segments:
        GPIO.output(segments,True)

try:
    clear_digit()
    while True:
        for digit in digits:
            for segment in digit:
                GPIO.output(segments[segment],False)
            sleep(1.0)
            clear_digit()

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
    
