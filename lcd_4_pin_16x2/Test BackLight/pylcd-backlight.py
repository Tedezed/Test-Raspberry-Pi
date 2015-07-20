#!/usr/bin/env python
# -*- coding: utf-8 -*-
# working 24/11/13
# with backlight control
# and auto Pi Rev detection

import smbus
from time import *
import RPi.GPIO as GPIO

BackLight = True   # LCD backlight enable
Revision = 0       # Pi revision
UP=0
LEFT=0
DOWN=0
RIGHT=0
SELECT=0


# General i2c device class so that other devices can be added easily
class i2c_device:
   def __init__(self, addr, port):
      self.addr = addr
      self.bus = smbus.SMBus(port)

   def write(self, byte):
      if (BackLight == False):
         byte = byte & 0x7F # switch off backlight LED
      else:
         byte = byte | 0x80 # switch on backlight LED

      self.bus.write_byte(self.addr, byte)

   def read(self):
      return self.bus.read_byte(self.addr)

   def read_nbytes_data(self, data, n): # For sequential reads > 1 byte
      return self.bus.read_i2c_block_data(self.addr, data, n)

class lcd:
   #initializes objects and lcd
   '''
   pinout is as follows: PCF8574 - HD44780
   P0 - LCD11 - D4
   P1 - LCD12 - D5
   P2 - LCD13 - D6
   P3 - LCD14 - D7
   P4 - LCD4  - RS
   P5 - LCD5  - R/W
   P6 - LCD6  - E
   P7 - LCD15 - LED BACKLIGHT
   '''
   def __init__(self, addr, port):
      self.lcd_device = i2c_device(addr, port)
      self.lcd_device.write(0x03)
      self.lcd_strobe()
      sleep(0.0005)
      self.lcd_strobe()
      sleep(0.0005)
      self.lcd_strobe()
      sleep(0.0005)
      self.lcd_device.write(0x02)
      self.lcd_strobe()
      sleep(0.0005)

      self.lcd_write(0x28)
      self.lcd_write(0x08)
      self.lcd_write(0x01)
      self.lcd_write(0x06)
      self.lcd_write(0x0C)
      self.lcd_write(0x01)

   # clocks EN to latch command
   def lcd_strobe(self):
      self.lcd_device.write((self.lcd_device.read() | 0x40))
      self.lcd_device.write((self.lcd_device.read() & 0xbF))

   # write a command to lcd
   def lcd_write(self, cmd):
      self.lcd_device.write((cmd >> 4))
      hi= self.lcd_device.read()
      self.lcd_strobe()
      self.lcd_device.write((cmd & 0x0F))
      lo= self.lcd_device.read()
      self.lcd_strobe()
      self.lcd_device.write(0x0)
   #   print 'cmd',cmd,hi,lo

   # write a character to lcd (or character rom)
   def lcd_write_char(self, charvalue):
   #      print "char",charvalue
         self.lcd_device.write((0x10 | (charvalue >> 4)))
         self.lcd_strobe()
         self.lcd_device.write((0x10 | (charvalue & 0x0F)))
         self.lcd_strobe()
         self.lcd_device.write(0x0)

   # put char function
   def lcd_putc(self, char):
      self.lcd_write_char(ord(char))

   # put string function
   def lcd_puts(self, string, line):
      if line == 1:
         self.lcd_write(0x80)
      if line == 2:
         self.lcd_write(0xC0)
      if line == 3:
         self.lcd_write(0x94)
      if line == 4:
         self.lcd_write(0xD4)

      for char in string:
         self.lcd_putc(char)

   # clear lcd and set to home
   def lcd_clear(self):
      self.lcd_write(0x1)
      self.lcd_write(0x2)

   # add custom characters (0 - 7)
   def lcd_load_custon_chars(self, fontdata):
      self.lcd_device.bus.write(0x40);
      for char in fontdata:
         for line in char:
            self.lcd_write_char(line)

   def test(self):
      print("")
      print("toggle E x 10")
      for i in range(10):
         print(".")
         self.lcd_device.write((self.lcd_device.read() | 0x40))
         sleep(1)
         self.lcd_device.write((self.lcd_device.read() & 0xbF))
         sleep(1)

      print("")
      print("toggle RS x 10")
      for i in range(10):
         print(".")
         self.lcd_device.write((self.lcd_device.read() | 0x10))
         sleep(1)
         self.lcd_device.write((self.lcd_device.read() & 0xEF))
         sleep(1)

def get_revision():
   with open('/proc/cpuinfo') as lines:
      for line in lines:
         if line.startswith('Revision'):
            return int(line[line.index(':') + 1:], 16) & 0xFFFF
   raise RuntimeError('No revision found.')

def get_board_revision():
   revision = get_revision()
   if revision in (2, 3):
      return 1
   else:
      return 2

def gpio_setup():
   global UP, DOWN, LEFT, RIGHT, SELECT
   if Revision==1:
      RIGHT=21
   else:
      RIGHT=27
   SELECT=4
   DOWN=17
   UP=22
   LEFT=23
   GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering
   GPIO.setup(SELECT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)    # set as input (Select button)
   GPIO.setup(UP, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)    # set as input (Up button)
   GPIO.setup(DOWN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)    # set as input (Down button)
   GPIO.setup(RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)    # set as input (Right button)
   GPIO.setup(LEFT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)    # set as input (Left button)

def main():
      global Revision
      Revision = get_board_revision()
      print "get board revision=",Revision
      if Revision==1:
         i2cbus=0
      else:
         i2cbus=1
      print "i2cbus=",i2cbus
      device = lcd(0x20,i2cbus)
      gpio_setup()

      device.lcd_clear()
      device.lcd_puts("abcdefghijklmnopqrst",1)
      device.lcd_puts("1234567890abcdefghij",2)
      device.lcd_puts("ABCDEFGHIJKLMNOPQRST",3)
      device.lcd_puts("Line 4 - Hello !!!!!",4)
      sleep(3)
      device.lcd_clear()
      while True:

         if GPIO.input(SELECT): # if port 4 == 1
            device.lcd_puts("SELECT pressed   ",1)
            print "SELECT is 1/HIGH/True"
            if GPIO.input(UP):
               break # quit if SELECT an UP pressed at the same time
         elif GPIO.input(DOWN): # if port 17 == 1
            device.lcd_puts("DOWN pressed     ",1)
            print "DOWN is 1/HIGH/True"
         elif GPIO.input(RIGHT): # if port 21 or 27== 1
            device.lcd_puts("RIGHT pressed    ",1)
            print "RIGHT is 1/HIGH/True"
         elif GPIO.input(UP): # if port 22 == 1
            device.lcd_puts("UP pressed       ",1)
            print "UP is 1/HIGH/True"
         elif GPIO.input(LEFT): # if port 23 == 1
            device.lcd_puts("LEFT pressed     ",1)
            print "LEFT is 1/HIGH/True"
         else:
            device.lcd_puts("No button pressed",1)

if __name__ == '__main__':
    main()