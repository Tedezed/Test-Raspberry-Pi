import pylcd
import time
lcd = pylcd.lcd(0x3f,1,1)

#Sin luz de led
#Line 1
lcd.lcd_puts("  Raspberry Pi",1)
#Line 2
lcd.lcd_puts("   @Zerrotajo",2)

