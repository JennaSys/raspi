import serial
import time


# ---MFRC522 register ----
COMMAND_WAIT = 0x02
COMMAND_READBLOCK = 0x03
COMMAND_WRITEBLOCK = 0x04
MFRC522_HEADER = 0xAB

STATUS_ERROR = 0
STATUS_OK = 1

MIFARE_KEYA = 0x00
MIFARE_KEYB = 0x01


def readCardSerial(ser):
    return ser.read(ser.inWaiting())



if __name__ == '__main__':
    buffer = ''
    ser = serial.Serial('COM11', 9600)
    ser.write(int(COMMAND_WAIT))

    while True:
        if (ser.inWaiting()):
            # Detected card at the reader!
            print readCardSerial(ser)

            ser.write(int(COMMAND_WAIT))



