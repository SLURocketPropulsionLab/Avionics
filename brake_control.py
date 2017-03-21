import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)  #brakes pulse
GPIO.setup(35, GPIO.OUT)  #brakes direction

read=('brakes_control.txt','r')

condition=read.readline()




GPIO.output(12, GPIO.HIGH)





GPIO.output(35, GPIO.HIGH)
