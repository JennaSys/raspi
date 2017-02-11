import RPi.GPIO as GPIO
from time import sleep
import web

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)

urls = ('/(.*)', 'snap')
led_state = False
app = web.application(urls, globals())

class snap:
    def GET(self, status):
        global led_state
        response = '?'
        if not status: 
            led_state = not led_state
            response = 'LED toggled!'
        else:
            if status == "on":
                led_state = True
                response = "LED turned ON!"
            elif status == "off":
                led_state = False
                response = "LED turned OFF!"
            else:
                response = 'Unknown command: ' + status + '!\n'	    
        GPIO.output(17,led_state)
        return response

if __name__ == "__main__":
    app.run()
