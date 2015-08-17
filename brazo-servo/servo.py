import RPi.GPIO as GPIO
import time

#Librerias para funcion getkey
import termios, sys, os
TERMIOS = termios

#Leer tecla de teclado
def getkey():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
    new[6][TERMIOS.VMIN] = 1
    new[6][TERMIOS.VTIME] = 0
    termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
    c = None
    try:
        c = os.read(fd, 1)
    finally:
        termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
    return c

GPIO.setwarnings(False)

#GPIO.setmode(GPIO.BOARD)
#Pines gpio
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)

p = GPIO.PWM(18,50)
o = GPIO.PWM(24,50)
u = GPIO.PWM(16,50)

p_init = 7.0
o_init = 5.5
u_init = 3.5

p.start(p_init)
o.start(o_init)
u.start(u_init)

time.sleep(1)


try:	
	key = True
	sen = 0.3
	while key:	
		tecla = getkey()
		print tecla
		if tecla == 'q':
			p_init = p_init - sen
		elif tecla == 'e':
                        p_init = p_init + sen
		if tecla == 's':
                        o_init = o_init - sen
		elif tecla == 'w':
                        o_init = o_init + sen
		if tecla == 'f':
                        u_init = u_init - sen
		elif tecla == 'r':
                        u_init = u_init + sen

		print 'Activando servos'
		p.ChangeDutyCycle(p_init)
		o.ChangeDutyCycle(o_init)
		u.ChangeDutyCycle(u_init)
		#time.sleep(0.1)
		print 'Fin while'		

except KeyboardInterrupt:
	print 'Fin'

	p_init = 7.0
	o_init = 5.5
	u_init = 3.5

	p.start(p_init)
	o.start(o_init)
	u.start(u_init)

	time.sleep(1)

	p.stop()
	GPIO.cleanup()
