import cv, time, datetime, sys, os
#multiprocessing
from multiprocessing import Process

from Phidgets.Devices.GPS import GPS
"""
write a demo multiprocessing cv imager capture test
"""

#input param = camera index, loop exit criteria

def photoLoop(inParams):
    
    camIndex, exitSeconds, savePath, debug = inParams

    captureA = cv.CaptureFromCAM(camIndex)
    cv.SetCaptureProperty(captureA, 3, 1280)
    cv.SetCaptureProperty(captureA, 4, 720)

    timeA = datetime.datetime.now()
    curFrame = 0
    #need to setup a sys-time, curFrame lookup file
    camLog = open(savePath+'/Cam'+str(camIndex)+'.log','w')
    while True:
        if debug:
            print "script running!", curFrame
        eTime = datetime.datetime.now() -timeA

        # exitSeconds = 0 means never exit...
        if eTime.seconds >= exitSeconds and exitSeconds != 0:
            print "exiting..."
            break
        imgName = "ImgCam"+str(camIndex)+"_"+str(curFrame).zfill(7)+'.jpg'
        imgA = cv.QueryFrame(captureA)
        cv.SaveImage(savePath+'/'+imgName, imgA)
        camLog.write(imgName+', '+str(datetime.datetime.now())+'\n')
        #print "curFrame:", curFrame, "elapsed seconds:", eTime.seconds
        curFrame = curFrame + 1
    print "number of photos:", curFrame 



def gpsLoop(inParams):
    #log path
    savePath, printLive = inParams
    #setup gps device
    #wait for gps attach?
    gps = GPS()
    gps.openPhidget()
    gps.waitForAttach(10000)
    print "GPS attached"
    #set up logging:
    gpsLog = open(savePath+'/Gps.log','w')

    #change handler
    def gpsChangeHandler1(e):
        gps_time = gps.getTime().toString()
        gps_lat = gps.getLatitude()
        gps_lon = gps.getLongitude()
        gps_alt = gps.getAltitude()    
        gps_heading = gps.getHeading()
        gps_vel = gps.getVelocity()
        time1 = str(datetime.datetime.now())
        dataElems = [time1, gps_time, gps_lat, gps_lon,gps_alt,gps_heading,gps_vel]
        dataElems = [str(x) for x in dataElems]
        return ','.join(dataElems)+'\n', (gps_lat, gps_lon, gps_alt)
        #(','.join(dataElems)+'\n')
        #gpsLog.flush()

            
    #gps.setOnPositionChangeHandler(gpsChangeHandler1)

    data, xyzPos = gpsChangeHandler1(1)
    gpsLog.write(data)
    while True:
        time.sleep(0.1)
        newData, newXyz = gpsChangeHandler1(1)
        if xyzPos == newXyz:
            pass
        else:
            #log new data
            print "position changed", newXyz
            xyzPos = newXyz
            gpsLog.write(newData)
            gpsLog.flush()
        


    
#main run
if __name__ == '__main__':

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
    #outPath = r'/data/geoPhotos/test1'
    outPath = curPath
#set main script paraaters here...
    #cam index, exit seconds (0 = never), out path to save in
    debugCams = False
    paramsCamA = (0, 0, outPath, debugCams)
    paramsCamB = (1, 0, outPath, debugCams)
    #out path to save in, print live text
    paramsGps = (outPath,True)
    #set up jobs
    jobs = []
    jobs.append(Process(target=photoLoop, args=(paramsCamA,)))
    jobs.append(Process(target=gpsLoop, args=(paramsGps,)))
    
    jobs.append(Process(target=photoLoop, args=(paramsCamB,)))

    #start gps loop first because its an event driven process
    #gpsLoop(paramsGps)

    #photoLoop(paramsCamA)
    
    print 1
    #now start jobs
    map(lambda x: x.start(), jobs)
    print 2
    map(lambda x: x.join(), jobs)

    print "press any key to exit..."
    chr = sys.stdin.read(1)
    print("Closing...")

    
    """
    #old code for single job type
    #photoLoop(0, 10, outPath)

    #photoLoop(paramsB)
    timeA = datetime.datetime.now()

    p = multiprocessing.Pool(2)
    p.map(photoLoop, [paramsA, paramsB])

    print "elapsed time:", (datetime.datetime.now()- timeA).seconds
    """
