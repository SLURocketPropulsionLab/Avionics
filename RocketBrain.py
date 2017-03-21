#!/usr/bin/python

import smbus
import math
import os
from gps import *
from time import *
import threading
import serial
import smbus
import time
import datetime


##############################################################################################
#Initilize hardware functions 
##############################################################################################
#Open Log File

# define a timestamp format you like
FORMAT = '%Y%m%d%H%M%S'
path = 'Rocketlog.txt'
new_path = '%s_%s' % (datetime.now().strftime(FORMAT), path)
f=open(new_path, 'a')


altimeter = serial.Serial(
              
               port='/dev/ttyUSB0',
               baudrate = 9600,
               parity=serial.PARITY_NONE,
               stopbits=serial.STOPBITS_ONE,
               bytesize=serial.EIGHTBITS,
               timeout=1/20
           )
radio = serial.Serial(
              
               port='/dev/ttyAMA0',
               baudrate = 9600,
               parity=serial.PARITY_NONE,
               stopbits=serial.STOPBITS_ONE,
               bytesize=serial.EIGHTBITS,
               timeout=1/20
           )


#seting the global variable
gpsd = None 

class GpsPoller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        global gpsd #bring it in scope
        gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
        self.current_value = None
        self.running = True #setting the thread running to true

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)
  
  def density(alt):
    if alt >= 27000:
        roh = Roh[10]
    elif alt >= 24000:
        roh = Roh[9]
    elif alt >= 21000:
        roh = Roh[8]
    elif alt >= 18000:
        roh = Roh[7]
    elif alt >= 15000:
        roh = Roh[6]
    elif alt >= 12000:
        roh = Roh[5]
    elif alt >= 9000:
        roh = Roh[4]
    elif alt >= 6000:
        roh = Roh[3]
    elif alt >= 3000:
        roh = Roh[2]
    else:
        roh = Roh[1]
    return roh

bus = smbus.SMBus(0) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)



##############################################################################################
#Initilize Variables
##############################################################################################
Alt_proj=0
Alt_current=0
V_current=0
g=32.2 #ft/s^2
Drag= enter drag here
Roh = [0.00217539, 0.00198698, 0.00181132,0.00164779, 0.00149581,0.00135479,0.00122417,0.00110341,0.000991984,0.000889378]
Area=enter area here
Mass = enter mass here
Second_Alt = 0
altcount=0


##############################################################################################
#Main Loop
##############################################################################################
while True:

#################################Altitude ##################################################
    starttime = time.time()
    try:
        Alt_current = int(altimeter.readline())
    except Nullreadline:
        Alt_current = 0


##################################GPS ######################################################

      #print 'latitude    ' , gpsd.fix.latitude
      #print 'longitude   ' , gpsd.fix.longitude
      #print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
      #print 'altitude (m)' , gpsd.fix.altitude
      #print 'eps         ' , gpsd.fix.eps
      #print 'epx         ' , gpsd.fix.epx
      #print 'epv         ' , gpsd.fix.epv
      #print 'ept         ' , gpsd.fix.ept
      #print 'speed (m/s) ' , gpsd.fix.speed
      #print 'climb       ' , gpsd.fix.climb
      #print 'track       ' , gpsd.fix.track
      #print 'mode        ' , gpsd.fix.mode
      #print
      #print 'sats        ' , gpsd.satellites
 

  ################################### Accelerometer ################################################


    print "gyro data"
    print "---------"
    try:
        gyro_xout = int(read_word_2c(0x43))
    except Null_xout:
        gyro_xout = 0
    try:
        gyro_yout = int(read_word_2c(0x45))
    except Null_yout:
        gyro_yout = 0
    try:
        gyro_zout = int(read_word_2c(0x47))
    except Null zout:
        gyro_zout = 0

    print "gyro_xout: ", gyro_xout, " scaled: ", (gyro_xout / 131)
    print "gyro_yout: ", gyro_yout, " scaled: ", (gyro_yout / 131)
    print "gyro_zout: ", gyro_zout, " scaled: ", (gyro_zout / 131)

    print
    print "accelerometer data"
    print "------------------"

    try:
        accel_xout = int(read_word_2c(0x3b))
    except:
        accel_xout = 0
    try
    accel_yout = read_word_2c(0x3d)
    accel_zout = read_word_2c(0x3f)

    accel_xout_scaled = accel_xout / 16384.0
    accel_yout_scaled = accel_yout / 16384.0
    accel_zout_scaled = accel_zout / 16384.0

    #Use print statement variables to create packet 
    print "accel_xout: ", accel_xout, " scaled: ", accel_xout_scaled
    print "accel_yout: ", accel_yout, " scaled: ", accel_yout_scaled
    print "accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled
    print "x rotation: " , get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
    print "y rotation: " , get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
###############################################################################################

    sleep(1/30)  

    remainder = altcount % 10

    if remainder = 0:
        endtime = time.time()
        Second_Alt=altimeter.readline()
        V_current = (abs(Alt_current - Second_Alt))/(abs(starttime-endtime))
    
    else:
        Second_Alt = Alt_Current
        endtime=starttime
    
Alt_proj = (Second_Alt + ((V_current^2) / ( 2 * ((g+Drag*((density(Second_Alt)*(V_current^2))/2)*Area)/Mass))))
##########################################################################################################################

    if brakes == 1:
        brakes.engaged()
        return
        
    if brakes == 0:
        brakes.disengaged()
        return
    
    if parachutes == 1:
        parachutes.out()
        return
    
    if parachutes == 0:
        parachutes.in()
        return
    
#######################################################################################################################    
    
    datain = f.readline()
    datainNoComma = datain.split(",")
    
    if int(datainNoComma[0]) == 1:
      doSomething.on()
      f.write(1 + "\n")
    
    if int(datainNoComma[0]) == 0:
      doSomething.on()
      f.write(0 + "\n")
    
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y/%m/%d %H:%M")
    #Timestamp,Strattoaltitude,GPSAlt,Latitude,Longitude,Xaccel,Yaccel,Zaccel,Xrot,Yrot,Zrot
    outstring = str(timestamp)+","+str(CurrentAltitude)+","+str(gpsd.fix.altitude)+","+str(gpsd.fix.latitude)+","+str(gpsd.fix.longitude)+"\n"
    + str(brakes)+","+str(parachute)+","+str(doSomething)
    f.write(outstring)
    
    radio.write(outstring)
    
    altcount=altcount+1  


    except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
        print "\nKilling Thread..."
        print "Done.\nExiting."   
        f.close()

  



