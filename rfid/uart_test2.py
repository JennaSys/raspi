import serial
import time

def detectCard():
    sTag = "TAG detected    "
    sNotag = "No TAG detected "

    ser = serial.Serial('COM11', 9600, timeout=0)
    print sNotag


    # ser.write(chr((0x37<<1) & 0x7E))
    # ser.write(chr(0x02))

    # ser.write(chr(0x01))
    # ser.write(chr(0x26))
    # ser.write(chr(0x02))

    # ser.write(0x01)
    # ser.write(0x26)
    # ser.write(0x02)

    buf = chr(0x26)
    ser.write(buf)


    while True:
        # while ser.inWaiting():
        #     val = ser.read(1)
        #     print hex(ord(val))
        print ser.inWaiting()
        time.sleep(0.2)

        # while(ser.read(1) != 0x01):
        #     print sTag
        #     time.sleep(0.2)
        # while(ser.read(1) != 0xFE):
        #     print sNotag
        #     time.sleep(0.2)


if __name__ == '__main__':
    detectCard()