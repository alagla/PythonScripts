#!/usr/bin/python
#
#  show the MIB object content

from pysnmp.entity.rfc3413.oneliner import cmdgen
import sys
import snmpwalk

#**************************************************************
# main program
#*************************************************************
if (len(sys.argv) == 1):
   print "syntax: python %s <host> <MIB OID>" % (sys.argv[0])
   sys.exit()

host   = sys.argv[1]
mibOID = sys.argv[2]    # this is a string
community = 'public' 
port = 161

snmpwalk.snmpwalk(host, community, midOID, 0, snmpTable)

for oid, value in snmpTable.items():
   print oid, value
