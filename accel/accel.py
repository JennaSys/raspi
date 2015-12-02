import RPi.GPIO as GPIO
from adxl345 import ADXL345
from time import sleep
  
adxl345 = ADXL345()

GPIO.setmode(GPIO.BCM)

pX_up = 22
pX_dn = 27
pY_up = 6
pY_dn = 5
pZ_up = 21
pZ_dn = 20

GPIO.setup(pX_up, GPIO.OUT)
GPIO.setup(pX_dn, GPIO.OUT)
GPIO.setup(pY_up, GPIO.OUT)
GPIO.setup(pY_dn, GPIO.OUT)
GPIO.setup(pZ_up, GPIO.OUT)
GPIO.setup(pZ_dn, GPIO.OUT)

def set_leds(x,y,z):
    GPIO.output(pX_up, x>=0)
    GPIO.output(pX_dn, x<0)
    GPIO.output(pY_up, y>=0)
    GPIO.output(pY_dn, y<0)
    GPIO.output(pZ_up, z>=0)
    GPIO.output(pZ_dn, z<0)
    
try:
    
    while True:    
        axes = adxl345.getAxes(True)
        print "ADXL345 on address 0x{:02X}".format(adxl345.address)
        print "   x = {:0.3f}G".format(axes['x'])
        print "   y = {:0.3f}G".format(axes['y'])
        print "   z = {:0.3f}G".format(axes['z'])
        
        set_leds(axes['x'], axes['y'], axes['z'])
        sleep(0.5)
            
except KeyboardInterrupt:
    pass
    
finally:
    GPIO.cleanup()

