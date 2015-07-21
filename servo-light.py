import RPi.GPIO as GPIO
import time

import pylcd
lcd = pylcd.lcd(0x3f,1,1)


GPIO.setwarnings(False)

#GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)

p = GPIO.PWM(18,50)
p.start(6.5)

lcd.lcd_puts("Raspberry Servo",1)
time.sleep(2)

try:	
	while True:
		#Line 1
		lcd.lcd_clear()
		lcd.lcd_puts("IZQUIERDA",2)
		p.ChangeDutyCycle(10.5)
		time.sleep(1)

		lcd.lcd_clear()
		lcd.lcd_puts("CENTRO",2)
		p.ChangeDutyCycle(6.5)
		time.sleep(1)

		lcd.lcd_clear()
		lcd.lcd_puts("DERECHA",2)
		p.ChangeDutyCycle(3.5)
		time.sleep(1)

except KeyboardInterrupt:
	print 'centro'
	p.ChangeDutyCycle(6.5)
	time.sleep(1)

	p.stop()
	GPIO.cleanup()
