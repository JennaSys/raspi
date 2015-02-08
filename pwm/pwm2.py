import wiringpi2 as wiringpi
from time import sleep

wiringpi.wiringPiSetupGpio()  #setup for BCM mode
wiringpi.pinMode(18, 2)       #enable PWM on GPIO18
wiringpi.pwmWrite(18, 0)      #set duty cycle to 0 (range is 0-1024)

delay_time = 0.002

try:
    while True:
        for dc in range(0, 1025):
            wiringpi.pwmWrite(18, dc)
            sleep(delay_time)
        for dc in range(1024, -1, -1):
            wiringpi.pwmWrite(18, dc)
            sleep(delay_time)
 
except KeyboardInterrupt:
    pass

finally:
    wiringpi.pwmWrite(18, 0) #turn off PWM mode
    wiringpi.pinMode(18, 0)  #reset GPIO18 to input
