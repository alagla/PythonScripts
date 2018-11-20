#!/usr/bin/python
# snmp set example
# bring up or down an interface.
# Caveat: must on VLAN=3, ifIndex >= 19
#
# ifAdminStatus: 1.3.6.1.2.1.2.2.1.7.<ifIndex>

from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902
import sys

statusList = ("none", "up", "down", "unknown")

#*********************************************************
#  main program
#*********************************************************
if (len(sys.argv) == 1):
   print "syntax: python %s <host> <ifIndex> <action>" % sys.argv[0]
   print "action: 1: up  2: down"
   sys.exit()
   
host = sys.argv[1]
ifIndex = int(sys.argv[2])  # an integer of ifIndex
action  = int(sys.argv[3])  # 1:up   2:down
community = 'private'       # read/write
port = 161

if (ifIndex < 19):
   print "error: cannot change interface status for ifIndex<19.  input ifIndex=", ifIndex
   sys.exit()

ifAdminStatus = '1.3.6.1.2.1.2.2.1.7.' + str(ifIndex)

cmdGen = cmdgen.CommandGenerator()   # create an SNMP object

# read the current interface status
errorIndication, errorStatus, errorIndex, results = cmdGen.getCmd(
    cmdgen.CommunityData( community ),
    cmdgen.UdpTransportTarget((host, port)),
    ifAdminStatus
)
for name, val in results:
   print  'Original interface Status: %s = %s (%s)' % (name, val, statusList[int(val)])

# set the new interface status
errorIndication, errorStatus, errorIndex, results = cmdGen.setCmd(
    cmdgen.CommunityData( community ),
    cmdgen.UdpTransportTarget((host, port)),
    (ifAdminStatus, rfc1902.Integer( action ))
)

for name, val in results:
   print  'New interface Status:      %s = %s (%s)' % (name, val, statusList[int(val)])
