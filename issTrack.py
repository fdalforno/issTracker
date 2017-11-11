import ephem
import time
from datetime import datetime
from math import degrees



def longitude_difference(t):
    '''Return how far the satellite is from the target longitude.

    Note carefully that this function does not simply return the
    difference of the two longitudes, since that would produce a
    terrible jagged discontinuity from 2pi to 0 when the satellite
    crosses from -180 to 180 degrees longitude, which could happen to be
    a point close to the target longitude.  So after computing the
    difference in the two angles we run degrees.znorm on it, so that the
    result is smooth around the point of zero difference, and the
    discontinuity sits as far away from the target position as possible.

    '''
    iss.compute(t)
    return ephem.degrees(iss.sublat - target_long).znorm




line0 = 'ISS (ZARYA)'
line1 = '1 25544U 98067A   17313.24531503  .00002638  00000-0  47166-4 0  9995'
line2 = '2 25544  51.6437  35.1846 0004395  99.3897   0.4968 15.54085036 84311'

iss = ephem.readtle(line0, line1, line2)
target_long = ephem.degrees('-50')


t = ephem.date(datetime.utcnow())
iss.compute(t)

d = longitude_difference(t)

while d > 0:
    t += ephem.minute
    d = longitude_difference(t)

while d < 0:
    t += ephem.minute
    d = longitude_difference(t)


tn = ephem.newton(longitude_difference, t - ephem.minute, t)

print('At this specific date and time:', ephem.date(tn))

#print('%f %f %s' % (degrees(iss.sublong), degrees(iss.sublat),d))
