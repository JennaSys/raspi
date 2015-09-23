import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

portTrig = 23
portEcho = 24

GPIO.setup(portTrig, GPIO.OUT)
GPIO.setup(portEcho, GPIO.IN)

#reset Trigger and let settle
GPIO.output(portTrig, False)
time.sleep(0.5)

#Start ranging
try:
    while True:
        GPIO.output(portTrig, True)
        time.sleep(0.00001)
        GPIO.output(portTrig, False)

        pulse_start = time.time()
        while not GPIO.input(portEcho):
            pulse_start = time.time()
			
        pulse_end = pulse_start
        while GPIO.input(portEcho):
            pulse_end = time.time()
			
        pulse_duration = pulse_end - pulse_start

        if pulse_duration  < 0.023:  # otherwise timeout
            #distance = (duration / 2) * speed_of_sound
            #speed_of_sound = 343 m/s = 34300 cm/s = 1125 ft/s = 13504 in/s
            distance = (pulse_duration / 2) * 13504

            print "Distance: {:0.2f} ({})".format(distance, pulse_duration)
        time.sleep(0.1)
        
except KeyboardInterrupt:
    pass
    
finally:
    GPIO.cleanup()

