import ephem
import math
from datetime import datetime
import logging
import urllib.request
import shutil


class Tracker(object):
    def __init__(self):
        self.sat = None
        self.targetLon = None
        self.satlist = {}

    def retrieveFile(self):
        url = "https://www.celestrak.com/NORAD/elements/stations.txt"
        file_name = "stations.txt"

        try:
            with urllib.request.urlopen(url,timeout=10) as response, open(file_name, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
        except(urllib.error.HTTPError, urllib.error.URLError)as error:
            print('Data of %s not retrieved because %s' % (file_name,error))



    def loadTle(self,fileName):
        f = open(fileName)
        self.satlist = {}
        l1 = f.readline()
        while l1:
            l2 = f.readline()
            l3 = f.readline()
            sat = ephem.readtle(l1, l2, l3)
            self.satlist[sat.name] = sat
            print(sat.name)
            l1 = f.readline()

        f.close()
        print("%i satellites loaded into list" % len(self.satlist))

    def loadSatellite(self,satName):
        self.sat = self.satlist.get(satName)


    def getPosition(self,time = None):
        if(self.sat):
            if(time is None):
                self.sat.compute()
            else:
                self.sat.compute(time)
            return (self.sat.sublong,self.sat.sublat)
        else:
            return (None,None)

    def longitude_difference(self,t):
        currPos = self.getPosition(t)[1]

        t += ephem.minute
        nextPos = self.getPosition(t)[1]

        difference = ephem.degrees(currPos - nextPos).znorm
        return difference

    def optimizeDiff(self, t = None):
        position = self.getPosition(t)[1]
        return self.sat._inc - ephem.degrees(math.fabs(position))


    def bisect(self,func,a,b,eps = 0.00001):
        Fa, Fb = func(a), func(b)

        while (b - a > eps):
            x = (a + b) / 2.0
            f = func(x)
            if f * Fa > 0:
                a = x
            else:
                b = x

        #print(b - a)
        return x

    def getNetMaxLatitude(self,t = None):
        if(t is None):
            t = ephem.date(datetime.utcnow())

        #print(ephem.Date(t))

        start = t

        difference = self.longitude_difference(t)

        if (difference > 0):
            #print("Descending phase %s" % difference)
            while difference > 0:
                t += ephem.minute
                difference = self.longitude_difference(t)
        else:
            #print("Ascending phase %s" % difference)
            while difference < 0:
                t += ephem.minute
                difference = self.longitude_difference(t)


        tn = self.bisect(self.optimizeDiff, t - (ephem.minute * 2), t)
        position = self.getPosition(tn)

        #print("Next pass is at %s position %s %s" % (ephem.Date(tn),position[0],position[1]))
        daysDiff = tn - start
        minutesDiff = daysDiff * 24 * 60
        #print("Wait minutes ", minutesDiff)
        return(tn,position[0],position[1])


    def checkSunlight(self, time, longitude,latitude):
        point = ephem.Observer()
        point.date = time
        point.lat = latitude
        point.lon = longitude
        sun = ephem.Sun()
        sun.compute(point)

        sun_is_up = point.previous_rising(sun) > point.previous_setting(sun)

        return sun_is_up

    def interestingPoint(self,longitude,latitude):
        interesting = False


        if  ephem.degrees('-100') <= longitude <= ephem.degrees('-80') and latitude >=  ephem.degrees('50'):
            interesting = True

        if  ephem.degrees('80') <= longitude <= ephem.degrees('100') and latitude <=  ephem.degrees('-50'):
            interesting = True

        return interesting

    def calcTable(self,num_step = 10,filter = False):
        passages = []
        t = ephem.date(datetime.utcnow())
        for c in range(num_step):
            passage = self.getNetMaxLatitude(t)
            in_sun = self.checkSunlight(passage[0], passage[1], passage[2])
            interesting = self.interestingPoint( passage[1], passage[2])

            data = (passage[0], passage[1], passage[2], in_sun,interesting)

            if filter and interesting:
                passages.append(data)
            elif not filter:
                passages.append(data)

            t = passage[0] + (ephem.minute * 5)

        return passages
