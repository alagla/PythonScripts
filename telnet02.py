#!/usr/bin/python
#
# telnet to a Cisco Ethernet switch and show the Spaning-Tree table
#
import sys
import telnetlib

if (len(sys.argv) == 1):
   print "syntax: python telnet02.py <switch>"
   sys.exit()

HOST = sys.argv[1]
VLAN = "3"   # STP is enabled on VLAN=3 only
TIMEOUT = 2
USER    = "user"
PASSWD  = "user"

tn = telnetlib.Telnet(HOST, timeout=TIMEOUT)
command = "show spanning-tree vlan 3"

ret = tn.read_until("Username: ", TIMEOUT)
if ret.find('Username') > 0:    # that is "found"
   tn.write(USER + "\n")
   tn.read_until("Password: ", TIMEOUT)
   tn.write(PASSWD + "\n")
elif ret.find('Password') > 0:    # that is "found"
   tn.write(PASSWD + "\n")
else:
   tn.write(PASSWD + "\n")	  # this part is not needed

tn.write(command + "\r\n")
tn.write("exit\n")

result =  tn.read_all()
tn.close()

for line in result.split('\n'):
   items = line.split()
   if len(items) > 4:
      if( items[0] == 'Spanning' and items[1] == 'tree' ):
         print "STP mode=", items[4]
      if len(items) == 6:
         print "%10s %6s %6s %6s %8s %6s" % (items[0], items[1], items[2], items[3], items[4], items[5])
      if len(items) == 7:
         last = items[5] + " " + items[6]
         print "%10s %6s %6s %6s %8s %6s" % (items[0], items[1], items[2], items[3], items[4], last)
