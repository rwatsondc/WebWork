import cv, time, datetime, sys, os, multiprocessing

"""
write a demo multiprocessing cv imager capture test
"""

#input param = camera index, loop exit criteria

def photoLoop(inParams):
    camIndex, exitSeconds, savePath = inParams
    captureA = cv.CaptureFromCAM(camIndex)
    cv.SetCaptureProperty(captureA, 3, 1280)
    cv.SetCaptureProperty(captureA, 4, 720)

    timeA = datetime.datetime.now()
    curFrame = 0
    #need to setup a sys-time, curFrame lookup file
    camLog = open(savePath+'/Cam'+str(camIndex)+'.log','w')
    while True:
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
        
#main run
if __name__ == '__main__':
    outPath = r'/data/geoPhotos/test1'
    #photoLoop(0, 10, outPath)
    paramsA = (0, 10, outPath)
    paramsB = (1, 10, outPath)
    #photoLoop(paramsB)
    timeA = datetime.datetime.now()

    p = multiprocessing.Pool(2)
    p.map(photoLoop, [paramsA, paramsB])

    print "elapsed time:", (datetime.datetime.now()- timeA).seconds
