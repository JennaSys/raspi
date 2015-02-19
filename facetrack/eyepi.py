from RPIO import PWM
import RPIO
import time

class EyePi():
    def __init__(self):
        
        self.pPanL = 18
        self.pTiltL = 26
        self.pPanR = 23
        self.pTiltR = 24
        self.pPanicBtn = 17

        self.pan_minL = 120
        self.pan_maxL = 230
        self.tilt_minL = 80
        self.tilt_maxL = 210
        self.pan_minR = 80
        self.pan_maxR = 170
        self.tilt_minR = 70
        self.tilt_maxR = 230

        #pan_center = ((pan_max - pan_min) / 2) + pan_min
        #tilt_center = ((tilt_max - tilt_min) / 2) + tilt_min
        self.pan_centerL = 180
        self.tilt_centerL = 155
        self.pan_centerR = 126
        self.tilt_centerR = 160
        
        self.inPanic = False
        
        RPIO.setmode(RPIO.BCM)

    def cb_panic(self, channel, val):
        print "PANIC!!!"
        self.inPanic = True
        self.cross_eyed()
        time.sleep(4)
        self.inPanic = False
        
        
    def start(self):
        if not PWM.is_setup():
            PWM.setup()
        if not PWM.is_channel_initialized(0):
            PWM.init_channel(0)
        
        #same as look_forward() without clearing first
        PWM.add_channel_pulse(0, self.pPanL, 0, self.pan_centerL)
        PWM.add_channel_pulse(0, self.pTiltL, 0, self.tilt_centerL)
        PWM.add_channel_pulse(0, self.pPanR, 0, self.pan_centerR)
        PWM.add_channel_pulse(0, self.pTiltR, 0, self.tilt_centerR)
        
        RPIO.setup(self.pPanicBtn, RPIO.IN)
        RPIO.add_interrupt_callback(self.pPanicBtn, edge='falling', pull_up_down=RPIO.PUD_UP, callback=self.cb_panic, debounce_timeout_ms=200)
        RPIO.wait_for_interrupts(threaded=True)

    def stop(self):
        RPIO.del_interrupt_callback(self.pPanicBtn)
        PWM.clear_channel(0)
        PWM.cleanup()
        
    def __set_position(self, port, pulse_value):
        PWM.clear_channel_gpio(0, port)    
        PWM.add_channel_pulse(0, port, 0, pulse_value)

    def set_pan(self, pan_pct):
        if pan_pct < 0:  #Pan Left
            if pan_pct < -100:
                pan_pct = -100
            panL = int(((self.pan_centerL - self.pan_minL) * pan_pct) / 100) + self.pan_centerL
            panR = int(((self.pan_centerR - self.pan_minR) * pan_pct) / 100) + self.pan_centerR
        else:  #Pan Right
            if pan_pct > 100:
                pan_pct = 100
            panL = int(((self.pan_maxL - self.pan_centerL) * pan_pct) / 100) + self.pan_centerL
            panR = int(((self.pan_maxR - self.pan_centerR) * pan_pct) / 100) + self.pan_centerR
        
        print 'PAN=L:{0} ({1}/{2}/{3})  R:{4} ({5}/{6}/{7})'.format(panL, self.pan_minL, self.pan_centerL, self.pan_maxL, panR, self.pan_minR, self.pan_centerR, self.pan_maxR)
        PWM.clear_channel_gpio(0, self.pPanL)    
        PWM.add_channel_pulse(0, self.pPanL, 0, panL)
        PWM.clear_channel_gpio(0, self.pPanR)    
        PWM.add_channel_pulse(0, self.pPanR, 0, panR)
        
        

    def set_tilt(self, tilt_pct):
        if tilt_pct < 0:  #Tilt Down
            if tilt_pct < -100:
                tilt_pct = -100
            tiltL = int(((self.tilt_centerL - self.tilt_minL) * tilt_pct) / 100) + self.tilt_centerL
            tiltR = self.tilt_centerR - int(((self.tilt_maxR - self.tilt_centerR) * tilt_pct) / 100)
        else:  #Tilt Up
            if tilt_pct > 100:
                tilt_pct = 100
            tiltL = int(((self.tilt_maxL - self.tilt_centerL) * tilt_pct) / 100) + self.tilt_centerL
            tiltR = self.tilt_centerR - int(((self.tilt_centerR - self.tilt_minR) * tilt_pct) / 100)
            
        
        print 'TILT=L:{0} ({1}/{2}/{3})  R:{4} ({5}/{6}/{7})'.format(tiltL, self.tilt_minL, self.tilt_centerL, self.tilt_maxL, tiltR, self.tilt_minR, self.tilt_centerR, self.tilt_maxR)
        PWM.clear_channel_gpio(0, self.pTiltL)    
        PWM.add_channel_pulse(0, self.pTiltL, 0, tiltL)
        PWM.clear_channel_gpio(0, self.pTiltR)    
        PWM.add_channel_pulse(0, self.pTiltR, 0, tiltR)
        


    def look_forward(self):
        self.__set_position(self.pPanL, self.pan_centerL)
        self.__set_position(self.pTiltL, self.tilt_centerL)
        self.__set_position(self.pPanR, self.pan_centerR)
        self.__set_position(self.pTiltR, self.tilt_centerR)

    def cross_eyed(self):
        self.__set_position(self.pPanL, self.pan_minL)
        self.__set_position(self.pPanR, self.pan_maxR)
        self.__set_position(self.pTiltL, self.tilt_centerL)
        self.__set_position(self.pTiltR, self.tilt_centerR)


    def look_left(self):
        self.__set_position(self.pPanL, self.pan_minL)
        self.__set_position(self.pPanR, self.pan_minR)

    def look_right(self):
        self.__set_position(self.pPanL, self.pan_maxL)
        self.__set_position(self.pPanR, self.pan_maxR)

    def look_up(self):
        self.__set_position(self.pTiltL, self.tilt_minL)
        self.__set_position(self.pTiltR, self.tilt_maxR)

    def look_down(self):
        self.__set_position(self.pTiltL, self.tilt_maxL)
        self.__set_position(self.pTiltR, self.tilt_minR)
        
    
    
if __name__ == '__main__':
    eyes = EyePi()
    eyes.start()
    eyes.cross_eyed()
    time.sleep(3)
    eyes.look_forward()
    time.sleep(2)
    eyes.stop()

