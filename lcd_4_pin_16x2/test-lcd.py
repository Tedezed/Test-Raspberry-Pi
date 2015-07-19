import pylcdlib
lcd = pylcdlib.lcd(0x27,0)
#Line 1
lcd.lcd_puts("RaspberryPi",1)
#Line 2
lcd.lcd_puts("Take",2)
