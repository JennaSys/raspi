import RPi.GPIO as GPIO
import time

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

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line 

# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005
CLR_DELAY = 0.003

def main():
  #GPIO INIT  
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7

  #LCD INIT
  lcd_byte(0x33,LCD_CMD) #initialization
  lcd_byte(0x32,LCD_CMD) #initialization
  lcd_byte(0x28,LCD_CMD) #4bit mode / 2-line / 5x7
  lcd_byte(0x0C,LCD_CMD) #Display ON / Cursor OFF / Blink OFF  
  lcd_byte(0x06,LCD_CMD) #Inc Cursor / No Display Shift
  lcd_byte(0x01,LCD_CMD) #Clear Display  
  time.sleep(CLR_DELAY)

  # Send some text
  lcd_string("Riverside\n       Raspberry")
  time.sleep(3)

  GPIO.cleanup()


def lcd_string(message):
  # Send string to display
  message = message.ljust(LCD_WIDTH," ")  

  for char in message:
    if char == '\n':
      lcd_byte(0xC0, LCD_CMD)  # line 2
    else:
      lcd_byte(ord(char), LCD_CHR)

def lcd_byte(bits, mode):
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

def toggle_enable():
  time.sleep(E_DELAY)    
  GPIO.output(LCD_E, True)  
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)  
  time.sleep(E_DELAY)   
    
    
if __name__ == '__main__':
  main()	

  
  
