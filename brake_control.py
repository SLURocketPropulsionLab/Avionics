import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)  #brakes pulse
GPIO.setup(35, GPIO.OUT)  #brakes direction

read=('brakes_control.txt','r')
condition=read.readline()

totalsteps = 0


while true

stepcount = 0

if condition == 1
  GPIO.output(35, GPIO.HIGH)
  while stepcount < 200  && (stepcount + totalsteps) <= 10000
  
    GPIO.output(12, GPIO.HIGH)
    time.sleep(.00005)
    GPIO.output(12, GPIO.LOW)
    stepcount +=1
    totalsteps +=1
    return
    
  else
     GPIO.output(35, GPIO.LOW)
     while stepcount < 200  && (totalsteps-stepcount) >= 0 
  
      GPIO.output(12, GPIO.HIGH)
      time.sleep(.00005)
      GPIO.output(12, GPIO.LOW)
      stepcount +=1
      return

    
return   
    
  










GPIO.output(35, GPIO.HIGH)
