import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
pin_charge = 13
pin_test = 19

pin_led1 = 21
pin_led2 = 20
pin_led3= 16
pin_led4 = 26
pin_led5 = 12

GPIO.setup(pin_led1, GPIO.OUT)
GPIO.setup(pin_led2, GPIO.OUT)
GPIO.setup(pin_led3, GPIO.OUT)
GPIO.setup(pin_led4, GPIO.OUT)
GPIO.setup(pin_led5, GPIO.OUT)


def set_leds(val):
        GPIO.output(pin_led1, val <1.0)
        GPIO.output(pin_led2, val <2.0)
        GPIO.output(pin_led3, val <3.0)
        GPIO.output(pin_led4, val <4.0)
        GPIO.output(pin_led5, val <5.0)
    
def map_value(raw_val):
    MIN_INPUT = 400
    MAX_INPUT = 2600
    MIN_OUTPUT = 0
    MAX_OUTPUT = 5
    
    old_range = MAX_INPUT - MIN_INPUT
    new_range = MAX_OUTPUT - MIN_OUTPUT
    return (((raw_val - MIN_INPUT) * new_range) / old_range) + MIN_OUTPUT
    
    
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
        set_leds(map_value(count))

except KeyboardInterrupt:
    GPIO.cleanup()
