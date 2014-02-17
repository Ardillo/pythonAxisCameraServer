#!/usr/bin/python 
 
# Server listens to port 8888
# If message comes in than place the Camera message in a database
# This is done together with a timestamp

# example> GET ?Message=Cam1

import socket
import re
import time
import datetime
import csv
import sys
#import pymssql
 
HOST = 'localhost'       # Hostname to bind
PORT = 8888              # Open non-privileged port 8888

buttonPressed = False    # Var for checking
#count = 0

#////////// FUNCTIONS /////////////

# split data with regular expression searching for non CHARS and white space
def splitString(data):
   splitData = re.split("\?|$|=|&| |\r\n", data)
   return splitData

# searches the splitted message for the cameraID and returns it
def searchCamName(data):
   for i,item in enumerate(data):
      if item == 'Message':
         camName = data[i+1]
         print "Camera name: " + camName
         return camName
         
# returns string with timestamp formatted in "2014-02-05 13:38:06"
def getTimeStamp():
   timeSeconds = time.time()
   timeStamp = datetime.datetime.fromtimestamp(timeSeconds).strftime('%Y-%m-%d' 
                                                                  + ' %H:%M:%S')
   return timeStamp

# read all rows in CSV file and return the last number
# TODO check if file exists, if not return 0
def readCountInCSV(camID):
   csvName = returnFile(camID)
   try:
      files = open(csvName, 'r')
   except IOError, msg:
      print "File not found, making new one"
      return 0      
   reader = csv.reader(files, delimiter=',')
   lastline = reader.next()
   for line in reader:
      lastline = line
   print "lastentry = " + str(lastline)
   number = lastline[0]
   return int(number)
   
# writes data to a .csv file named with the camID
def writeToCSV(camID):
   csvName = returnFile(camID)
   time = getTimeStamp()
   count = readCountInCSV(camID)
   count += 1
   files = open(csvName, 'a')
   writer = csv.writer(files, delimiter=',')
   writer.writerows([[count, time, camID]])

# return file location and name in string   
def returnFile(camID):
   csvName = "log/" + str(camID) + ".csv"
   return csvName
 
# incrementing counter by one
def counter(cntr):
   cntr += 1
   return cntr
    
# /////////// MAIN ///////////////

# Create TCP/IP socket, 2nd option is for reusing port after ctrl-C
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind socket to the port
server_address = (HOST, PORT)
print "*********************"
print "*  AXIS HTTP server *"
print "*********************"
print "" 
print >> sys.stderr, 'start listening on %s, port %s' % server_address
try:
   server.bind(server_address)
   server.listen(1)
except socket.error, msg:
   print msg
   sys.exit()
   

# Keep program running
while not buttonPressed:
   try:
      conn, addr = server.accept()
      print '\nConnected by', addr, "\n"
      while 1:
          data = conn.recv(1024)
          if "Get ?Message=" in data:
	     strings = splitString(data)
	     camID = searchCamName(strings)
	     writeToCSV(camID)
	     print ""
	  else:
	     print "Received data not as expected format, drop message\n"
          if not data: break
#         conn.send(data)      
      conn.close()
   except socket.error, msg:
      print msg
      sys.exit()
      continue

