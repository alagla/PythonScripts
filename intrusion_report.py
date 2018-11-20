#!/usr/bin/python
#
#       Description: analyze the secure log (var/log/secure) to create an intrusion report
#       Usage: python intrusion_report.py   <no parameters>
#

fd = open('/var/log/secure')  # default is open for read
# fd = open('/var/log/secure-20161016')  # default is open for read
syslog = fd.readlines()

countTable = {}      # initialization of a dictionary
for line in syslog:
   data = line.split()
   items = len(data)
   if( items > 14):
      # print data[6], data[7], data[14]
      if( (data[6] == 'authentication') and (data[7] == 'failure;') and (data[14] == 'user=root') ):
         [tmp, rhost] = data[13].split('=')
         if (rhost in countTable):
            countTable[ rhost ] += 1
         else:
            countTable[ rhost ] = 1    # create a new entry in the dictionary table

print "%48s  %5s" % ("Intrusion IP Address", "Count")
print "-----------------------------------------------------------"
#****************************************
#   sory by value in descending order
#*****************************************
for ip, count in sorted(countTable.items(), key=lambda x: (-x[1], x[0])):
   if count > 10:
      print "%48s  %5d" % (ip, count)
