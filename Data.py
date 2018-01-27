import picamera
import ephem
import time
import datetime as dt
import os
from sense_hat import AstroPi
from sense_hat import SenseHat
import csv

class Photo(object):
    def __init__(self):
        # Picamera object and horizontally flips it
        self.camera = picamera.PiCamera()
        self.camera.hflip = True
        self.camera.annotate_background = picamera.Color('black')
        self.camera.iso = 800
        self.astroPi = AstroPi()
        
        
        self.folder = "./Data"
        
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        
    def captureImage(self):
        timeStamp = time.strftime("%Y%m%d%H%M%S")
        directory = ('%s/img_%s.jpg' % (self.folder,timeStamp))
        self.camera.capture(directory)
        
        return directory
    
    def close(self):
        self.camera.close()
        
class Sensors(object):
    def __init__(self):
        self.folder = "./Data/"
        self.file = "measure.csv"
        self.measure = 0
        
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
            
        self.path = os.path.join(self.folder,self.file)
        self.csv = open(self.path,"a",newline="")
        self.writer = csv.writer(self.csv,delimiter=";",quotechar="'",quoting=csv.QUOTE_NONNUMERIC)
        self.sensors = SenseHat()
        
    def write_sensors(self,tracker = None,photo=None):
        compass = self.sensors.compass_raw
        accelerometer = self.sensors.accelerometer_raw
        timer = time.strftime("%Y%m%d%H%M%S")
        lat = 0.0
        lon = 0.0
        sun = False
        if not tracker is None:
            postion = tracker.getPosition()
            lon = postion[0]
            lat = postion[1]
            sun = tracker.checkSunlight(dt.datetime.utcnow(),lon,lat)
        
        row = []
        row.append(self.measure)
        row.append(timer)
        row.append(sun)
        row.append(lat / ephem.degree)
        row.append(lon / ephem.degree)
        row.append(compass.get('x'))
        row.append(compass.get('y'))
        row.append(compass.get('z'))
        row.append(accelerometer.get('x'))
        row.append(accelerometer.get('y'))
        row.append(accelerometer.get('z'))
        
        row.append(photo)
        
        
        print(row)
        
        self.writer.writerow(row)
        self.measure += 1
        
    def close(self):
        self.csv.close()
    
        
    