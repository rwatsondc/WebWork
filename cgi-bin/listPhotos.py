#!/usr/bin/python
# -*- coding: UTF-8 -*-# enable debugging
import cgitb
cgitb.enable()
print("Content-Type: text/html;charset=utf-8")
print ""
import os, pprint

inDir = r'/data/geoPhotos'
"""
lDir = os.listdir(inDir)

print "Total log folder files:", len(lDir)
"""

walkDir = os.walk(inDir)
walkDict = {}

for root, subs, files in walkDir:
    walkDict[root]=len(files)

print("List of folders with number of files in each folder:")
print "<br />"
for dir in walkDict:
    print "<br />"
    print("<br />"+dir+": " + str(walkDict[dir]))
