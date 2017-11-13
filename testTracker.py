from Tracker import Tracker
import ephem
from datetime import datetime

test = Tracker()
test.retrieveFile()
test.loadTle('stations.txt')
test.loadSatellite('ISS (ZARYA)')
prev = test.calcTable(10,False)

print("Previsione passaggi alla ora UTC %s ora locale %s \n\n" % (ephem.date(datetime.utcnow()), ephem.date(datetime.now())))


print("Orario,Longitudine,Latitudine,Illuminato,Interessante")

for row in prev:
    print(ephem.Date(row[0]),",",ephem.degrees(row[1]),",",ephem.degrees(row[2]),",",row[3],",",row[4])

