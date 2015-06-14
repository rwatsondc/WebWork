#!/usr/bin/python
# -*- coding: UTF-8 -*-# enable debugging
import cgitb
cgitb.enable()
print("Content-Type: text/html;charset=utf-8")
print ""
print("Taking Pictures Now!")

import cv, time

captureA = cv.CaptureFromCAM(0)
cv.SetCaptureProperty(captureA, 3, 1280)
cv.SetCaptureProperty(captureA, 4, 720)

captureB = cv.CaptureFromCAM(1)
cv.SetCaptureProperty(captureB, 3, 1280)
cv.SetCaptureProperty(captureB, 4, 720)


for i in range(10):
    print ""
    print i
    time.sleep(0.2)
    imgA = cv.QueryFrame(captureA)
    imgB = cv.QueryFrame(captureB)
    cv.SaveImage('/var/www/data/A.jpg', imgA)
    cv.SaveImage('/var/www/data/B.jpg', imgB)

print "\nDone!"
