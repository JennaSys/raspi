import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

portLED = 17
portTrig = 18

GPIO.setup(portLED, GPIO.OUT)
GPIO.setup(portTrig, GPIO.IN)

try:
    while True:
        if GPIO.input(portTrig):
            GPIO.output(portLED, True)
        else:
            GPIO.output(portLED, False)

        time.sleep(0.5)
        
except KeyboardInterrupt:
    GPIO.cleanup()

    

