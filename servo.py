import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

#GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)

p = GPIO.PWM(18,50)
p.start(6.5)
time.sleep(1)


try:	
	while True:
		print 'izquierda'
		p.ChangeDutyCycle(10.5)
		time.sleep(1)

		print 'centro'
		p.ChangeDutyCycle(6.5)
		time.sleep(1)

		print 'derecha'
		p.ChangeDutyCycle(3.5)
		time.sleep(1)

		print 'centro'
		p.ChangeDutyCycle(6.5)
		time.sleep(1)

except KeyboardInterrupt:
	p.stop()
	GPIO.cleanup()
