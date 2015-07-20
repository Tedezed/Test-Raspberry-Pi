import pylcdlib
lcd = pylcdlib.lcd(0x3f,1,1)

#Line 1
lcd.lcd_puts("HELLO",1)
#Line 2
lcd.lcd_puts("ZERROT",2)
