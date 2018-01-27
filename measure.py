from Tracker import Tracker
from Data import Photo,Sensors
import time

'''
Con questo progetto vogliamo fotografare le aurore boreali e misurare l'interazione del sole con
il campo magnetico terrestre.

Il progetto si compone di due parti la prima chiamata Tracker che serve per eseguire le previsioni
di passaggio nella zona del Canada dove le aurore boreali si manifestano a latitudini piu' basse.
La zona del Canada scelta e' compresa tra una longitudine di 100W e 80W come recuperato da https://en.wikipedia.org/wiki/Aurora.

Per eseguire l'esperimento completamente dovremmo poter avere un'orbita che passa in quel quadrante di notte.
(Possiamo provare a eseguire noi una previsione dei passaggi).

La seconda parte del progetto si measure.py si occupa di eseguire le fotografie, misurare il campo magnetico e le accelerazioni
dovute all'accensione dei motori.

Ci aspettiamo essenzialmente un aumento dell'intensita' del campo magnetico all'avvicinarsi dei poli terrestri
e una diminuzione significativa dello stesso nella parte non al sole della traiettoria della ISS.


'''

iss = Tracker()
photo = Photo()
sensor = Sensors()

iss.retrieveFile()
iss.loadTle('stations.txt')
iss.loadSatellite('ISS (ZARYA)')


contatoreMisura = 0

try:
    while True :
        if iss.optimizeDiff() < 0.05:
            
            #siamo nella parte alta/bassa dell'orbita facciamo le foto piu' spesso
            if contatoreMisura > 10:
                image = photo.captureImage()
                contatoreMisura = 0
                sensor.write_sensors(iss,image)
            else:
                sensor.write_sensors(iss)
                
        else:
            
            '''
            in tutto il resto dell'orbita continuiamo lo stesso a fare foto per curiosita'
            '''
            if contatoreMisura > 120:
                image = photo.captureImage()
                contatoreMisura = 0
                sensor.write_sensors(iss,image)
            else:
                sensor.write_sensors(iss)
                
        contatoreMisura = contatoreMisura +1
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    print('\n! Fine esperimento \n')
    sensor.close()
    photo.close()

    
    
