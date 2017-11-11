from Tracker import Tracker


test = Tracker()
test.loadTle('stations.txt')
test.loadSatellite('ISS (ZARYA)')
point = test.getNetMaxLatitude()
test.checkSunlight(point[0],point[1],point[2])