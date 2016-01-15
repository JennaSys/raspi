import spidev
import time

VREF = 3.3

spi = spidev.SpiDev()
spi.open(0,0)

def ReadChannel(channel):
    adc = spi.xfer2([1, (8+channel)<<4, 0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data
    
try:    
    while True:
        raw_data = ReadChannel(0)
        millivolts = (raw_data * (VREF * 1000)) / 1024  # 1024=10 Bit data
        tempC = (millivolts - 500) / 10  # 10mv/C   0.5v=0C
        tempF = ((tempC * 9) / 5) + 32
        
        print 'Data={0}  Temp F={1}  Temp C={2}'.format(raw_data, tempF, tempC)
        time.sleep(0.5)

except KeyboardInterrupt:
    pass
    
finally:
    spi.close()
    
    
