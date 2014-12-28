import spidev
import time

spi = spidev.SpiDev()
spi.open(0,0)

def ReadChannel(channel):
    adc = spi.xfer2([1, (8+channel)<<4, 0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data
    
try:    
    while True:
        light1 = ReadChannel(0)
        light2 = ReadChannel(1)
        
        print 'ch1={0}  ch2={1}'.format(light1, light2)
        time.sleep(1)

except KeyboardInterrupt:
    pass
    
finally:
    spi.close()
    
    
