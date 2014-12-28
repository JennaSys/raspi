import RPi.GPIO as GPIO
import time

pPan = 24
pTilt = 23

freq = 200

center = 1.5 * freq / 10
left = 0.5 * freq / 10
right = 2.5 * freq / 10

GPIO.setmode(GPIO.BCM)
GPIO.setup(pPan, GPIO.OUT)
GPIO.setup(pTilt, GPIO.OUT)

sPan = GPIO.PWM(pPan, freq)
sTilt = GPIO.PWM(pTilt, freq)

sPan.start(center)
sTilt.start(center)

time.sleep(5)

sPan.stop()
sTilt.stop()

GPIO.cleanup()



