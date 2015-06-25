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

gpsPoints ={}

for root, subs, files in walkDir:
    walkDict[root]=len(files)
    #read in gps lines
    try:
        numPnts = len(open(os.path.join(root, 'Gps.log'),'r').readlines())
        gpsPoints[os.path.join(root, 'Gps.log')]=numPnts
    except:
        pass
    

print("List of folders with number of files in each folder:")

for dir in walkDict:
    print "<br />"
    print("<br />  &nbsp;  "+dir+": " + str(walkDict[dir]))



print "<br />"
print "<br />"

#Add logic to count GPS points specifically
print "<br />Listing out Points for each Gps.log:"
for pnts in gpsPoints:
    print "<br />"
    print("<br />  &nbsp;  "+pnts+": " + str(gpsPoints[pnts]))


#add free disk space info using subprocess and df -h

import subprocess
df = subprocess.Popen(["df", "-h"], stdout=subprocess.PIPE)
output = df.communicate()[0]

output = output.split("\n")[0:2]

print "<br />"
print "<br />"
print "<br />"
print "Disk Space usage:"

print('<table border="1" style="width:100%">')
for line in output:
    print("<tr>")
    newLine = line.split(' ')
    newLine = [x for x in newLine if x != ''][:5]
    for item in newLine:
        print("<td>")
        print item+"&nbsp;"
        print("</td>")
    print("</tr>")
print("</table>")

#now add free memory, ram stats:
import psutil
print "<br />"
print "<br />"
print "<br />"
print "Current CPU usage: "+str(psutil.cpu_percent(1))+'%'
print "<br />"
memory = psutil.virtual_memory().percent
print "Current Memory usage: "+str(memory)+'%'
                                

