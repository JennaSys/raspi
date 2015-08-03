import os
import sys
from time import sleep
import logging

import pigpio

import MindBody
import wiegand_read

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger('rfid_checkin')
log.setLevel(logging.DEBUG)
# logging.getLogger('suds.client').setLevel(logging.DEBUG)


def main():

    mb = MindBody.MindBody()

    def validate(value):
        print("value={}".format(value))
        if value > 0:
            result = mb.AddArrival(str(value))
            if result.ArrivalAdded == True:
                w.beep_auth()
            elif result.ErrorCode == 301:  # ID not found
                w.beep_invalid()
            else:
                w.beep_noauth()


    try:
        if 'win' in sys.platform:
            WIN_GPIO_HOST = "rfidhost.local"
            os.environ["PIGPIO_ADDR"] = WIN_GPIO_HOST
            log.debug("PIGPIO_ADDR={}".format(os.environ["PIGPIO_ADDR"]))
            pi = pigpio.pi(WIN_GPIO_HOST)
        else:
            pi = pigpio.pi()

        w = wiegand_read.Weigand(pi, 14, 15, 23, 24, validate)

        while True:
            sleep(60)

    except KeyboardInterrupt:
        pass
    finally:
        w.cancel()
        pi.stop()


if __name__ == "__main__":
    main()

