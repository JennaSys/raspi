#!/usr/bin/python
BOARD = "board"
BCM = "bcm"
OUT = "out"
IN = "in"

PUD_UP = 'pullup'
PUD_DOWN = 'pulldown'
FALLING = 'falling'
RISING = 'rising'
 
def setmode(mode):
    print "MODE: ", mode

def setup(pin, mode, **kwargs):
    print "SETUP(", pin, "):", mode, [kwargs[key] for key in kwargs]

def output(pin, value):
    print "OUTPUT(", pin, ":", value

def cleanup():
    print "clean-up"

def add_event_detect(pin, mode, **kwargs):
    print "EVENT(",pin, "):", mode, [kwargs[key] for key in kwargs]
