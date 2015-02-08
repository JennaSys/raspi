import RPi.GPIO as GPIO
from time import sleep

# Adafruit compatible mapping
LCD_RS = 25
LCD_E  = 24
LCD_D4 = 23
LCD_D5 = 17
LCD_D6 = 27
LCD_D7 = 22


# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005
CLR_DELAY = 0.003

def main():
  # GPIO INIT  
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7

  # LCD INIT
  send_byte(0x33,LCD_CMD) #initialization
  send_byte(0x32,LCD_CMD) #initialization
  send_byte(0x28,LCD_CMD) #4bit mode / 2-line / 5x7
  send_byte(0x0C,LCD_CMD) #Display ON / Cursor OFF / Blink OFF  
  send_byte(0x06,LCD_CMD) #Inc Cursor / No Display Shift
  send_byte(0x01,LCD_CMD) #Clear Display  
  sleep(CLR_DELAY)

  # Send some text
  send_string("Riverside\n       Raspberry")
  sleep(3)

  GPIO.cleanup()


def send_string(message):
  message = message.ljust(LCD_WIDTH," ")  #pad to LCD width  

  for char in message:
    if char == '\n':
      send_byte(0xC0, LCD_CMD)  #Move to line 2
    else:
      send_byte(ord(char), LCD_CHR)


def toggle_enable():
  time.sleep(E_DELAY)    
  GPIO.output(LCD_E, True)  
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)  
  time.sleep(E_DELAY)   
    

def send_byte(bits, mode):
  # mode = True  for character / False for command
  GPIO.output(LCD_RS, mode) # RS

  # High bits
  GPIO.output(LCD_D4, bits&0x10==0x10)
  GPIO.output(LCD_D5, bits&0x20==0x20)
  GPIO.output(LCD_D6, bits&0x40==0x40)
  GPIO.output(LCD_D7, bits&0x80==0x80)

  toggle_enable()      

  # Low bits
  GPIO.output(LCD_D4, bits&0x01==0x01)
  GPIO.output(LCD_D5, bits&0x02==0x02)
  GPIO.output(LCD_D6, bits&0x04==0x04)
  GPIO.output(LCD_D7, bits&0x08==0x08)

  toggle_enable()   

    
if __name__ == '__main__':
  main()	

  
  
