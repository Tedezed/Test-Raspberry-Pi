import pylcdlight as pylcd

lcd = pylcd.lcd(0x3f,1,1)

#Line 1
lcd.lcd_puts("Raspberry LUZ",1)
#Line 2
lcd.lcd_puts("Take",2)


