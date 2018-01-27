from Tracker import Tracker
from Data import Photo,Sensors
import time

iss = Tracker()
photo = Photo()
sensor = Sensors()

iss.retrieveFile()
iss.loadTle('stations.txt')
iss.loadSatellite('ISS (ZARYA)')

numeroMisura = 0

while True:
    max_diff = iss.optimizeDiff()
    
    
    
    if max_diff <= 0.05:
        if numeroMisura > 2:
            numeroMisura = 0
            file = photo.captureImage()
            sensor.write_sensors(iss,file)
        else:
            sensor.write_sensors(iss)
            
    else:
        if numeroMisura > 60:
            numeroMisura = 0
            file = photo.captureImage()
            sensor.write_sensors(iss,file)
        else:
            sensor.write_sensors(iss) 
    
    
    numeroMisura += 1
    time.sleep(1)
    


sensor.close()





