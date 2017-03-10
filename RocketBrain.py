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

f=open('RocketLog.txt','a')

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
Roh = enter density array here
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
    Alt_current=altimeter.readline()


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

    gyro_xout = read_word_2c(0x43)
    gyro_yout = read_word_2c(0x45)
    gyro_zout = read_word_2c(0x47)

    print "gyro_xout: ", gyro_xout, " scaled: ", (gyro_xout / 131)
    print "gyro_yout: ", gyro_yout, " scaled: ", (gyro_yout / 131)
    print "gyro_zout: ", gyro_zout, " scaled: ", (gyro_zout / 131)

    print
    print "accelerometer data"
    print "------------------"

    accel_xout = read_word_2c(0x3b)
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
    
    
     Alt_proj = (Second_Alt + ((V_current^2) / ( 2 * ((g+Drag*((Roh*(V_current^2))/2)*Area)/Mass))))
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
    
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y/%m/%d %H:%M")
    #Timestamp,Strattoaltitude,GPSAlt,Latitude,Longitude,Xaccel,Yaccel,Zaccel,Xrot,Yrot,Zrot
    outstring = str(timestamp)+","+str(CurrentAltitude)+","+str(gpsd.fix.altitude)+","+str(gpsd.fix.latitude)+","+str(gpsd.fix.longitude)+"\n"
    + str(brakes)+','+str(parachute)
    f.write(outstring)
    
    radio.write(outstring)
    
    altcount=altcount+1  


    except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
        print "\nKilling Thread..."
        print "Done.\nExiting."   
        f.close()

  



