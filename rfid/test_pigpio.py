# Stub for running GPIO apps on Windows

OUTPUT = "out"
INPUT = "in"
PUD_UP = 'pullup'
PUD_DOWN = 'pulldown'
FALLING_EDGE = 'falling'
RISING_EDGE = 'rising'
EITHER_EDGE = 'either'
TIMEOUT = 2
 
def pi():
    print "INIT"
    gpio = GPIO()
    return gpio

class GPIO:
    def set_mode(self, pin, mode):
        print "SETUP(", pin, "):", mode

    def set_pull_up_down(self, pin, mode):
        print "SETUP(", pin, "):", mode

    def read(self, pin):
        print "READ(", pin, "):"

    def write(self, pin, value):
        print "WRITE(", pin, "):", value

    def stop(self):
        print "STOP"

    def callback(self, pin, mode, cb_method):
        print "EVENT(",pin, "):", mode, cb_method
