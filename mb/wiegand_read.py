#!/usr/bin/env python

import logging
import sys
import os
from time import sleep
import pigpio


if 'win' in sys.platform:
    WIN_GPIO_HOST = "rfidhost.local"
    os.environ["PIGPIO_ADDR"] = WIN_GPIO_HOST

logging.basicConfig(format='%(asctime)s %(levelname)s:  %(message)s')
log = logging.getLogger('Wiegand')
log.setLevel(logging.DEBUG)

class Weigand:

    BYTE_LEN = 8
    CODE_BYTES = 4   # Wiegand26=3, Wiegand34=4

    def __init__(self, pi, gpio_0, gpio_1, gpio_beep, gpio_led, callback, reverse_bytes=False, bit_timeout=10):

        """
        Instantiate with the pi, gpio for 0 (green wire), the gpio for 1
        (white wire), the gpio for the buzzer, the gpio for the LED, 
        the callback function, and the bit timeout in
        milliseconds which indicates the end of a code.

        The callback is passed the code length in bits and the value.
        """

        self.pi = pi
        self.gpio_0 = gpio_0    # Data 0
        self.gpio_1 = gpio_1    # Data 1
        self.gpio_beep = gpio_beep  # Buzzer
        self.gpio_led = gpio_led    # LED

        self.callback = callback
        self.bit_timeout = bit_timeout
        self.reverse_bytes = reverse_bytes

        self.in_code = False

        self.pi.set_mode(gpio_0, pigpio.INPUT)
        self.pi.set_mode(gpio_1, pigpio.INPUT)
        self.pi.set_mode(gpio_beep, pigpio.OUTPUT)
        self.pi.set_mode(gpio_led, pigpio.OUTPUT)

        self.pi.set_pull_up_down(gpio_0, pigpio.PUD_UP)
        self.pi.set_pull_up_down(gpio_1, pigpio.PUD_UP)

        self.cb_0 = self.pi.callback(gpio_0, pigpio.FALLING_EDGE, self._cb)
        self.cb_1 = self.pi.callback(gpio_1, pigpio.FALLING_EDGE, self._cb)
        
        self.pi.write(gpio_beep, 1)    # Turn off buzzer
        self.pi.write(gpio_led, 1)    # Turn off Green LED

    def _cb(self, gpio, level, tick):

        """
        Accumulate bits until both gpios 0 and 1 timeout.
        """

        # TODO: very first bit read is skipped for some reason

        if level < pigpio.TIMEOUT:

            if not self.in_code:
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
                    # TODO: Fix parity check if using Wiegand26 with 3 bytes
                    if self._get_parity(self.data[:2],0) == self.parity_even and self._get_parity(self.data[2:],1) == self.parity_odd:
                        self.callback(self.total(self.data))
                    else:
                        self.callback(0)

    def cancel(self):
        """
        Cancel the Wiegand decoder.
        """
        self.cb_0.cancel()
        self.cb_1.cancel()

    def _get_parity(self, data, evenodd):
        """
        data = [list of bytes to parity check]
        evenodd = 0 if even parity or 1 if odd parity
        """
        p = 0
        for value in data:
            p += bin(value).count('1')
        return ((p % 2) + evenodd) % 2

    def total(self, byte_list):
        total_value = 0
        for value in byte_list:
            total_value = (total_value << 8) + value
        return total_value
        
    def beep_auth(self):
        self.pi.write(self.gpio_led, 0)
        self.pi.write(self.gpio_beep, 0)
        sleep(0.17)
        self.pi.write(self.gpio_beep, 1)
        sleep(0.02)
        self.pi.write(self.gpio_beep, 0)
        sleep(0.17)
        self.pi.write(self.gpio_beep, 1)
        self.pi.write(self.gpio_led, 1)

    def beep_noauth(self):
        self.pi.write(self.gpio_beep, 0)
        sleep(1.0)
        self.pi.write(self.gpio_beep, 1)

    def beep_invalid(self):
        self.pi.write(self.gpio_beep, 0)
        sleep(1.0)
        self.pi.write(self.gpio_beep, 1)
        sleep(0.1)
        self.pi.write(self.gpio_beep, 0)
        sleep(1.0)
        self.pi.write(self.gpio_beep, 1)

            
        
if __name__ == "__main__":

    def validate_id(value):
        print("value={}".format(value))
        if value > 0:
            sleep(0.5)
            w.beep_auth()

    try:
        if 'win' in sys.platform:
            log.debug("PIGPIO_ADDR={}".format(os.environ["PIGPIO_ADDR"]))
            pi = pigpio.pi(WIN_GPIO_HOST)
        else:
            pi = pigpio.pi()

        w = Weigand(pi, 14, 15, 23, 24, validate_id)
        while True:
            sleep(60)
            
    except KeyboardInterrupt:
        pass
    finally:
        w.cancel()
        pi.stop()

