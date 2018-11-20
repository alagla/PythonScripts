#!/usr/bin/python
#
#       Date: January 10, 2017
#       Description: compute the hourly system load average
#       Usage: python hw05script.py {-daily | -hourly | <date1> <data2>
#       Output
#               1. Hour
#               2. Number of top sessions
#               3. Active users
#               4. Average system Load (based on 15-min load average)
#               5. Peak Load (max of 1-min, 5-min, and 15-min load)
#
#	note: two different data formats
#	(1) top - 00:02:02 up 38 days,  6:35,  0 users,  load average: 0.00, 0.00, 0.00   (n=14)
#	(2) top - 17:31:01 up 36 days, 4 min,  0 users,  load average: 0.00, 0.00, 0.00  (n=15)
#-------------------------------------------------------------------------------------

#
import sys
import datetime as dt
from datetime import datetime

SYNTAX = "syntax: python hw05script.py {-daily | -hourly | -raw } <yyyy-mm-dd> <yyyy-mm-dd>\n"
if (len(sys.argv) != 4):
   print SYNTAX
   sys.exit()

op = sys.argv[1]
if op == "-daily":
   opcode = 1
elif op == "-hourly":
   opcode = 2
elif op == "-raw":
   opcode = 3
else:
   print SYNTAX
   sys.exit(1)

#************************************************
#  change date fromat from mm-dd to yyyy-mm-dd
#  programming note: year needs to be changed for new quarter
#************************************************
fmt = "%Y-%m-%d"
d1 = datetime.strptime((sys.argv[2]), fmt).date()  # start date
d2 = datetime.strptime((sys.argv[3]), fmt).date()  # end date

# initialization of Dictionary
session = {}  # number of top sessions based on daily, hourly, or raw
user    = {}  # number of active users in the session
uptime  = {}  # uptime since last reboot (not used)
sysLoad = {}  # systerm load
peak    = {}  # peak load

delta = d2 - d1

prefix = "/home/jyu/cron/top/"
for i in range(delta.days + 1):
   x =  (d1 + dt.timedelta(days=i))
   mmdd = x.strftime('%m-%d')    # change the format from yyyy-mm-dd to mm-dd
   topFile = prefix + "top." + mmdd
   fd = open(topFile)
   topData = fd.readlines()

   lineNo = 0    # not used, for debugging only
   for line in topData:
      if line.startswith('top'):
         inline = line.rstrip('\n')     # remove '\n' at the end of line
         data = inline.split()
         n = len(data)
         (hour, min, sec) = data[2].split(':')
         
         # ******* set the key for Dictionary tables
         if opcode == 1:               # daily data
             key = mmdd
         elif opcode == 2:
             key = mmdd + ":" + hour   # hourly data
         elif opcode == 3:
             key = mmdd + ":" + hour + ":" + min    # raw data
         else:
             print "Program Assert: unknow opcode=", opcode
             sys.exit(1)

         if key in session:
            session[ key ] += 1
         else:      # intialize all Dictionary tables
            session[ key ] = 1
            user[key] = 0
            uptime[key] = ''
            sysLoad[key] = 0.0
            peak[key] = 0.0

         if n == 14:
            uptime[key] = data[4] + data[5] + data[6]
            user[key] += int(data[7])
            pt = 11
         elif n == 15:      # event occur between 00:00 and 00:59
            uptime[key] = data[4] + data[5] + data[6] + data[7]
            user[key]   += int(data[8])
            pt = 12
         else:
            print "data abnormalities"    # there are additional cases not implemented yet
            continue

         # print lineNo, n, load1, load2, load3
         load01 = float(data[pt].rstrip(','))  # not used, keept it for debugging
         load05 = float(data[pt+1].rstrip(','))
         load15 = float(data[pt+2])
         sysLoad[key] += load15   # average is based on 15-min load average
         if key in peak:
             # data is collected at 15-min interval, so it is possible that load15>load05
             if( peak[key] < load01): peak[key] = load01
             if( peak[key] < load05): peak[key] = load05
             if( peak[key] < load05): peak[key] = load15

         # print "DEBUF", lineNo, key, load01, load05, load15
         lineNo += 1
   # end one top file
# end  all top files

print "%8s %7s  %6s %6s %6s" % ("Time", "Session", "User", "Load Avg", "Peak")

for key in  sorted(session.keys()):
   n = session[key]
   if( n < 1):
      print "Program Assert: n=", n
      sys.exit(1)
   avgUser = user[key]/n
   avgOccupancy = sysLoad[key]/n
   print "%8s %7d  %6.1f %6.2f %6.2f" % (key,session[key],avgUser,avgOccupancy,peak[key])
