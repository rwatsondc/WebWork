import cv, time, datetime, sys, os
from Phidgets.Devices.GPS import GPS

#set up new directory - 
saveDirBase='/data/geoPhotos/'

today = datetime.datetime.now()
dayString = str(today.month)+"_"+str(today.day)+"_"+str(today.year)
dayRun = 0

keepLooping = True
while keepLooping:
    curPath = os.path.join(saveDirBase, "imgs_"+dayString+"_"+str(dayRun))
    if os.path.exists(curPath):
        dayRun = dayRun + 1
    else:
        os.makedirs(curPath)
        saveDir = curPath
        keepLooping = False



#saveDir = "..."
outLogPath = os.path.join(curPath, "runLog.txt")

#find last log entry, start numbering with most recent, else start over
try:
    inLog = open(outLogPath,'r').readlines()
    #image name first in list
    lastFrame = inLog[-1].split(',')[0]
    print "last frame captured:", lastFrame
    lastFrameCount = int(lastFrame[7:-4])
    curFrame = lastFrameCount+1
except:
    curFrame = 1
    
#raise('oops')

logFile = open(outLogPath,'w')

gps = GPS()
gps.openPhidget()
gps.waitForAttach(10000)
gps_time = gps.getTime().toString()

#eventually add logic for gps fix here...


captureA = cv.CaptureFromCAM(0)
cv.SetCaptureProperty(captureA, 3, 1280)
cv.SetCaptureProperty(captureA, 4, 720)

captureB = cv.CaptureFromCAM(1)
cv.SetCaptureProperty(captureB, 3, 1280)
cv.SetCaptureProperty(captureB, 4, 720)

header = 'imgName,curTime,elpTime,gps_time,gps_vel, gps_heading, gps_lon,gps_lat,gps_alt\n'
logFile.write(header)


#reWrite for infinite loop...
#adding breakout logic after 30 seconds

timeA = datetime.datetime.now()
print "starting photoloop, updating every 10 iterations..."
while True:
    #timeB = datetime.datetime.now()
    eTime = datetime.datetime.now()-timeA
    if eTime.seconds > 30:
        break
    #time.sleep(0.2)
    #print 1
    i = curFrame
    curTime = str(datetime.datetime.now())
    imgName = 'TestImg'+str(i).zfill(6)+'.jpg'
    if i%2==0:
        imgA = cv.QueryFrame(captureA)
        cv.SaveImage(saveDir+'/'+imgName, imgA)
    else:
        imgB = cv.QueryFrame(captureB)
        cv.SaveImage(saveDir+'/'+imgName, imgB)
    #print 2
    #cv.ShowImage("camera", img)
    
    
    #print 3
    #gps stuff...
    gps_time = gps.getTime().toString()
    gps_lat = gps.getLatitude()
    gps_lon = gps.getLongitude()
    gps_alt = gps.getAltitude()    
    gps_heading = gps.getHeading()
    gps_vel = gps.getVelocity()
    elpTime = str(datetime.datetime.now())
    outList = [imgName,curTime,elpTime,gps_time,gps_vel, gps_heading, gps_lon,gps_lat,gps_alt]
    outList = [str(x) for x in outList]
    outStr = ','.join(outList)+'\n'
    
    logFile.write(outStr)
    curFrame = curFrame + 1
    if curFrame %10 ==0:
        logFile.flush()
        print 'Iteration:', i, str(curTime), gps_lon,gps_lat,gps_alt
    
print "loop exit..."
print "photos taken", curFrame
print "elapsed time for photos", eTime.seconds


    #time.sleep(0.1)
    
#logFile.close()
    


#print "Done"
