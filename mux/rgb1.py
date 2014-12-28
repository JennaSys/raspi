import RPi.GPIO as GPIO
import time

pRed = 4
pGreen = 17
pBlue = 22

pLed1 = 18
pLed2 = 23
pLed3 = 24
pLed4 = 25


GPIO.setmode(GPIO.BCM)

GPIO.setup(pRed, GPIO.OUT, initial=True)
GPIO.setup(pGreen, GPIO.OUT, initial=True)
GPIO.setup(pBlue, GPIO.OUT, initial=True)

leds=[pLed1, pLed2, pLed3, pLed4]
for led in range(4):
    GPIO.setup(leds[led], GPIO.OUT,  initial=False)

colors = [[0,0,1],[0,1,0],[0,1,1],[1,0,0],[1,0,1],[1,1,0],[1,1,1]]

def setLed(port, color):
    if sum(color) == 0:
        GPIO.output(port, False)
    else:
        GPIO.output(port, True)
        
    GPIO.output(pRed, color[0])
    GPIO.output(pGreen, color[1])
    GPIO.output(pBlue, color[2])


def simple():
    speed = 0.5
    for led in range(4):
        setLed(leds[led], [1,0,0])
        time.sleep(speed)
        setLed(leds[led], [0,1,0])
        time.sleep(speed)
        setLed(leds[led], [0,0,1])
        time.sleep(speed)
        setLed(leds[led],[0,0,0])
        time.sleep(speed)
        
def setLeds(red, green, blue):
    for led in range(4):
        setLed(leds[led], [red, green, blue])


def display_frame(frame, duration, dwelltime):
    start = time.time()
    while (time.time() - start) < duration:
        for led in range(4):
            setLed(leds[led], frame[led])
            time.sleep(dwelltime/1000.0)
            setLed(leds[led], [0,0,0])
    
    
def cycle():
    x=0
    while True:
        display_frame([colors[x],colors[(x+1)%7],colors[(x+2)%7],colors[(x+3)%7]], 1, 3)
        x += 1
        if x > 6:
            x = 0
    
    
try: 
    #simple()
    #display_frame([colors[3],colors[1],colors[0],colors[6]], 5, 3)
    cycle()
    #while True:
    #    setLeds(1,1,1)
    
except KeyboardInterrupt:
    pass
    
finally:
    GPIO.cleanup()
