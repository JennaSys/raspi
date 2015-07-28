#!/usr/bin/env python

import pigpio
import logging
   
logging.basicConfig(level=logging.DEBUG)


class weigand:

    BYTE_LEN = 8
    CODE_BYTES = 4  #  Wiegand 26=3, Wiegand34=4

    def __init__(self, pi, gpio_0, gpio_1, callback, bit_timeout=10):

        """
        Instantiate with the pi, gpio for 0 (green wire), the gpio for 1
        (white wire), the callback function, and the bit timeout in
        milliseconds which indicates the end of a code.

        The callback is passed the code length in bits and the value.
        """

        self.pi = pi
        self.gpio_0 = gpio_0
        self.gpio_1 = gpio_1

        self.callback = callback
        self.bit_timeout = bit_timeout

        self.in_code = False

        self.pi.set_mode(gpio_0, pigpio.INPUT)
        self.pi.set_mode(gpio_1, pigpio.INPUT)

        self.pi.set_pull_up_down(gpio_0, pigpio.PUD_UP)
        self.pi.set_pull_up_down(gpio_1, pigpio.PUD_UP)

        self.cb_0 = self.pi.callback(gpio_0, pigpio.FALLING_EDGE, self._cb)
        self.cb_1 = self.pi.callback(gpio_1, pigpio.FALLING_EDGE, self._cb)


    def _cb(self, gpio, level, tick):

        """
        Accumulate bits until both gpios 0 and 1 timeout.
        """

        # TODO: very first bit read is skipped for some reason

        if level < pigpio.TIMEOUT:

            if self.in_code == False:
                self.bits = 1
                self.num = 0
                self.parity_even = 0 if gpio == self.gpio_0 else 1
                self.parity_odd = -1
                self.data = []

                self.in_code = True
                self.code_timeout = 0
                self.pi.set_watchdog(self.gpio_0, self.bit_timeout)
                self.pi.set_watchdog(self.gpio_1, self.bit_timeout)
                logging.debug("START")
            else:
                if (self.bits - 1) % 8 == 0 and self.bits > 1:
                    self.data.append(self.num)
                    self.num = 0
                    logging.debug("BITS={}".format(self.bits))
                else:
                    self.num = self.num << 1
                    
                self.bits += 1

            if gpio == self.gpio_0:
                logging.debug("{} BIT:0".format(self.bits))
                self.code_timeout = self.code_timeout & 2 # clear gpio 0 timeout
            else:
                logging.debug("{} BIT:1".format(self.bits))
                self.code_timeout = self.code_timeout & 1 # clear gpio 1 timeout
                if self.bits > 1:   # skip 1st parity bit
                    self.num = self.num | 1

        else:

            if self.in_code:

                if gpio == self.gpio_0:
                    self.code_timeout = self.code_timeout | 1 # timeout gpio 0
                else:
                    self.code_timeout = self.code_timeout | 2 # timeout gpio 1

                if self.code_timeout == 3: # both gpios timed out
                    self.pi.set_watchdog(self.gpio_0, 0)
                    self.pi.set_watchdog(self.gpio_1, 0)
                    self.in_code = False
                    self.parity_odd = self.num   # should only have one bit at this point
                    logging.debug("PE={}  PO={}".format(self.parity_even, self.parity_odd)) 
                    if self.parity(self.data[:2],0) == self.parity_even and self.parity(self.data[2:],1) == self.parity_odd:
                        self.callback(self.bits, self.data[::-1])
                    else:
                        self.callback(self.bits, [])
                    

    def cancel(self):

        """
        Cancel the Wiegand decoder.
        """

        self.cb_0.cancel()
        self.cb_1.cancel()

    def parity(self, data, evenodd):
        p = 0
        for value in data:
            p += bin(value).count('1')
        return ((p % 2) + evenodd) % 2
        

    def total(self, values):
        t = 0
        for n in values:
            t = (t << 8) + n
        return t
            
        
if __name__ == "__main__":

    import time


    def validate_id(bits, value):
        print("bits={} bytes={} value={}".format(bits, [hex(n) for n in value], w.total(value)))

    pi = pigpio.pi()

    w = weigand(pi, 14, 15, validate_id)

    time.sleep(300)

    w.cancel()

    pi.stop()

