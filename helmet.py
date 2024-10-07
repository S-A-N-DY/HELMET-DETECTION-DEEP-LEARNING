import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
from picamera import PiCamera
from time import sleep
import os
#import RPi.GPIO as GPIO
from gpiozero import LED,Button
from time import sleep
from time import sleep
import RPi.GPIO as GPIO
from gpiozero import LED
from gpiozero import MCP3008
import requests
import serial
import random

RF1 = Button(16)
RF2 = Button(19)


motor = LED(26)
buzzer = LED(21)
pump = LED(20)
motor.on()
buzzer.off()
pump.off()

i=0
j=0

camera = PiCamera()
camera.start_preview()
sleep(1)
camera.stop_preview()


recipient="9844379554"
ser = serial.Serial('/dev/ttyS0', baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS
                    )

ser.write('AT\r\n'.encode())
sleep(1)
ser.write('AT+CMGF=1\r\n'.encode())
sleep(1)

gpgga_info = "$GPGGA,"
GPGGA_buffer = 0
NMEA_buff = 0
lat_in_degrees = 0
long_in_degrees = 0
gps=0

def GPS_Info():
    global NMEA_buff
    global lat_in_degrees
    global long_in_degrees
    nmea_time = []
    nmea_latitude = []
    nmea_longitude = []
    nmea_time = NMEA_buff[0]                    #extract time from GPGGA string
    nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA string
    nmea_longitude = NMEA_buff[3]               #extract longitude from GPGGA string
    
    print("NMEA Time: ", nmea_time,'\n')
    print ("NMEA Latitude:", nmea_latitude,"NMEA Longitude:", nmea_longitude,'\n')
    
    lat = float(nmea_latitude)                  #convert string into float for calculation
    longi = float(nmea_longitude)               #convertr string into float for calculation
    
    lat_in_degrees = convert_to_degrees(lat)    #get latitude in degree decimal format
    long_in_degrees = convert_to_degrees(longi) #get longitude in degree decimal format
    
#convert raw NMEA string into degree decimal format   
def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.4f" %(position)
    return position

if gps==1:
    received_data = (str)(ser.readline())                   #read NMEA string received
    GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string                 
    if (GPGGA_data_available>0):
        GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string 
        NMEA_buff = (GPGGA_buffer.split(','))               #store comma separated data in buffer
        GPS_Info()                                          #get time, latitude, longitude 
        print("lat in degrees:", lat_in_degrees," long in degree: ", long_in_degrees, '\n')
    received_data = (str)(ser.readline())                   #read NMEA string received
    GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string                 
    if (GPGGA_data_available>0):
        GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string 
        NMEA_buff = (GPGGA_buffer.split(','))               #store comma separated data in buffer
        GPS_Info()                                          #get time, latitude, longitude 
        print("lat in degrees:", lat_in_degrees," long in degree: ", long_in_degrees, '\n')
    received_data = (str)(ser.readline())                   #read NMEA string received
    GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string                 
    if (GPGGA_data_available>0):
        GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string 
        NMEA_buff = (GPGGA_buffer.split(','))               #store comma separated data in buffer
        GPS_Info()                                          #get time, latitude, longitude 
        print("lat in degrees:", lat_in_degrees," long in degree: ", long_in_degrees, '\n')
    received_data = (str)(ser.readline())                   #read NMEA string received
    GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string                 
    if (GPGGA_data_available>0):
        GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string 
        NMEA_buff = (GPGGA_buffer.split(','))               #store comma separated data in buffer
        GPS_Info()                                          #get time, latitude, longitude 
        print("lat in degrees:", lat_in_degrees," long in degree: ", long_in_degrees, '\n')
    received_data = (str)(ser.readline())                   #read NMEA string received
    GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string                 
    if (GPGGA_data_available>0):
        GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string 
        NMEA_buff = (GPGGA_buffer.split(','))               #store comma separated data in buffer
        GPS_Info()                                          #get time, latitude, longitude 
        print("lat in degrees:", lat_in_degrees," long in degree: ", long_in_degrees, '\n')
else:
    lat_in_degrees = 13.01212
    long_in_degrees = 80.0123


r =requests.get('http://www.iotclouddata.com/21log/037/iot21.php?A=Lat' + str(lat_in_degrees) +'_Lon' +str(long_in_degrees) )


model = tensorflow.keras.models.load_model('keras_model.h5')


while True:
        px = MCP3008(0)
        Px = px.value * 100
        print('Oxygen=' + str(round(Px)))
        hb = MCP3008(1)
        HB = hb.value * 100
        if Px < 90:
            pump.on()
        else:
            pump.off()


        if HB > 10:
            HB = 0
        else:
            HB=66+((random.random()*100)%20)
        print('HB=' + str(round(HB)))
    
        if HB > 72:
            ser.write('''AT+CMGS="'''.encode() + recipient.encode() + '''"\r'''.encode())
            sleep(1)
            ser.write("Heart Beat Abnormal".encode())
            ser.write(str(lat_in_degrees).encode())
            ser.write(str(long_in_degrees).encode())
            sleep(1)
            ser.write(chr(26).encode())
            sleep(1)
            r =requests.get('http://www.iotclouddata.com/22log/386/iot22.php?A=Alert_Lat' + str(lat_in_degrees) +'_Lon' +str(long_in_degrees) )
        if RF1.is_pressed:        
            buzzer.on()
            print('Zone1')
        if RF2.is_pressed:        
            buzzer.on()
            print('Zone2')
        camera.start_preview(fullscreen=False,window=(100,100,640,480))
        camera.capture('seed.jpg')
        
# Disable scientific notation for clarity
        np.set_printoptions(suppress=True)

# Load the model

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# Replace this with the path to your image
        image = Image.open('seed.jpg')

#resize the image to a 224x224 with the same strategy as in TM2:
#resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)

#turn the image into a numpy array
        image_array = np.asarray(image)

# display the resized image
        image.show()

# Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

# Load the image into the array
        data[0] = normalized_image_array

# run the inference
        prediction = model.predict(data)
        ynew = model.predict_classes(data)
        print(prediction)
        if ynew == [0]:
                print(" ")
        if ynew == [1]:
                print(" Helmet ")
                buzzer.off()
                motor.on()
	elif ynew==[2]:
                print(" NO Helmet ")
                motor.off()
                buzzer.on()
        if ynew == [3]:
                print(" QR ")
                r =requests.get('http://www.iotclouddata.com/22log/386/iot22.php?A=Name:Ganesh_Age:30_IDNO:13894134_VehicleNo:TN02AH0121')
        print(ynew)
