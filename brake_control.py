import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)  #brakes pulse
GPIO.setup(35, GPIO.OUT)  #brakes direction
totalsteps = 0


while true

stepcount = 0
read=('brakes_control.txt','r')
condition=read.readline()


if condition == 1
  GPIO.output(35, GPIO.HIGH)
  while stepcount < 50  and (stepcount + totalsteps) <= 400
  
    GPIO.output(12, GPIO.HIGH)
    time.sleep(.005)
    GPIO.output(12, GPIO.LOW)
    stepcount +=1
    totalsteps +=1
    
    
  else
     GPIO.output(35, GPIO.LOW)
     while stepcount < 50  and (totalsteps-stepcount) >= 0 
  
      GPIO.output(12, GPIO.HIGH)
      time.sleep(.005)
      GPIO.output(12, GPIO.LOW)
      stepcount +=1
      totalsteps -=1

    
   
    
  










GPIO.output(35, GPIO.HIGH)
