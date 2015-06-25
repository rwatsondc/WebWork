"""
simple gps test
"""
print "starting up!"

from Phidgets.Devices.GPS import GPS
import datetime, sys

gps = GPS()
gps.openPhidget()
print "waiting for attach"
gps.waitForAttach(10000)
print "attached!"
gps_time = gps.getTime().toString()

def gpsChangeHandler1(e):
    gps_time = gps.getTime().toString()
    gps_lat = gps.getLatitude()
    gps_lon = gps.getLongitude()
    gps_alt = gps.getAltitude()    
    gps_heading = gps.getHeading()
    gps_vel = gps.getVelocity()
    time1 = str(datetime.datetime.now())
    dataElems = [time1, gps_time, gps_lat, gps_lon]
    dataElems = [str(x) for x in dataElems]
    print ','.join(dataElems)
    

print "testing function"
gpsChangeHandler1(1)

print "setting event handler active"
gps.setOnPositionChangeHandler(gpsChangeHandler1)

print("Press Enter to quit....")
chr = sys.stdin.read(1)

print("Closing...")

print "Done!"
