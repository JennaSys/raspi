import serial
import time

def detectCard():
    sTag = "TAG detected    "
    sNotag = "No TAG detected "

    ser = serial.Serial('COM11', 115200, timeout=2)
    print sNotag

    # Test Mode
    # ser.write(chr(0x02))

    # Normal Mode
    ser.write(chr(0x01))

    #Read ID
    #  Card Type
    # ser.write(chr(0x7f))
    # ser.write(chr(0x03))
    # ser.write(chr(0x52))
    # ser.write(chr(0xf7))
    # ser.write("\x7f\x03\x52\xf7")
    ser.write(''.join(map(chr,[0x7f,0x03,0x52,0xf7])))
    time.sleep(0.2)

    #  Series Number
    ser.write(chr(0x7f))
    ser.write(chr(0x04))
    ser.write(chr(0xf7))
    time.sleep(0.2)

    #  Halt
    ser.write(chr(0x7f))
    ser.write(chr(0x0b))
    ser.write(chr(0xf7))
    time.sleep(0.2)

    try:
        while True:
            while ser.inWaiting():
                val = ser.read(1)
                print hex(ord(val))
            # print ser.inWaiting()
            # time.sleep(0.2)

            # while(ser.read(1) != 0x01):
            #     print sTag
            #     time.sleep(0.2)
            # while(ser.read(1) != 0xFE):
            #     print sNotag
            #     time.sleep(0.2)

    except KeyboardInterrupt:
        ser.write(chr(0x0c))
        print "halt"



if __name__ == '__main__':
    detectCard()