#!/usr/bin/python
#
#       Date: November 12, 2016
#       Description (Acounting Management): get the usage data of each account
#       Usage: python Account_Usage_Info.py   <no parameters>
#

import os
from datetime import datetime

#**************************************
#  function getPID
#  return: pid (a string)
#    using find (instead fo index) to avoid non-found situation
#**************************************
def getPID( tmpStr ):
   n1 = tmpStr.find('[') 
   n2 = tmpStr.find(']')
   if( n2 > n1 ):
      pid = tmpStr[n1+1:n2]
      return pid
   else:
      return "none"

#************************************************
#  main program - 1st step: get syslog files
#************************************************
directory = "/var/log"

year = str(2016)
fmt = "%Y/%b/%d %H:%M:%S"
openTime     = {}      	# initialization of a dictionary, key = process ID
closeSession = {}	# key = account
totalTime    = {}	# key = account

for file in os.listdir( directory ):
   if file.startswith("secure"):
      logFile = directory + "/" + file
      fd = open(logFile)     # default is open for read
      syslog = fd.readlines()

      for line in syslog:
         data = line.split()
         n = len(data)
         if( n > 10):
            if( (data[6] == 'session') and (data[7] == 'opened')  ):
               user = data[10]
               timeRaw = year + "/" + data[0] + "/" + data[1] + " " + data[2]
               timeStamp = datetime.strptime(timeRaw, fmt)   # Time Object
               pid = getPID(data[4])
               if pid == "none": continue
               openTime[ pid ] = timeStamp
            elif( (data[6] == 'session') and (data[7] == 'closed')  ):
               user = data[10]
               timeRaw = year + "/" + data[0] + "/" + data[1] + " " + data[2]
               timeStamp = datetime.strptime(timeRaw, fmt)   # Time Object
               pid = getPID(data[4])
               if( pid in openTime):
                  duration = (timeStamp - openTime[pid]).seconds
                  if( user in totalTime ):
                     closeSession[ user ] += 1
                     totalTime[ user ] += duration
                  else:
                     closeSession[ user ] = 1
                     totalTime[ user ] = duration
                  # print "-- closed", user, pid, timeRaw, timeStamp, dur
   # end of one syslog file
# end of all syslog files

#*****************************************
#    summary
#****************************************
print "Linux05 Account Usage Report"
print "%10s %6s  %10s %8s\n" % ('Account', 'Count', 'Total Time', 'Average')
for user in sorted(closeSession.keys()):
      n = closeSession[user]
      totalUsage = totalTime[user]
      avg = totalUsage/n
      print "%10s %6d  %10d %8.1f" % (user, n, totalUsage, avg)



