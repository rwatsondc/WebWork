#!/usr/bin/python
# -*- coding: UTF-8 -*-# enable debugging

import os, getpass

print("Content-Type: text/html;charset=utf-8")
print ""
print "starting..."
print "username:", getpass.getuser()

r = open('/var/www/cgi-bin/newfile.txt','w')

import datetime

r.write('new file written\n')

r.write(str(datetime.datetime.now()))
r.close()
print "Done!"
