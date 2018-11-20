#!/usr/local/bin/python3
#
# command line approach - get the MAC address table
#
import sys
import os

if (len(sys.argv) == 1):
   print "syntax: python %s <switch> <vlan>" % (sys.argv[0])
   sys.exit()

host = sys.argv[1]
vlan = sys.argv[2]  # a string

oid1 = "1.3.6.1.2.1.17.4.3.1.1"    # MAC Address
oid2 = "1.3.6.1.2.1.17.4.3.1.2"    # MAC Table Interface Index
oid3 = "1.3.6.1.2.1.2.2.1.1"       # Interface Index
oid4 = "1.3.6.1.2.1.2.2.1.2"       # Interface Description
community = "public\@%s" % (vlan)

dot = '.'

#*********************************************************************
cmd = "snmpwalk -v2c -c %s  %s %s "  % (community, host, oid3)
fp = os.popen( cmd )
snmp = fp.read().splitlines()   # split the outout into a list of "lines"
ifTable = {}
for i in range(len(snmp)):
   data = snmp[i].split('=')
   oid = data[0].split(dot)[-1]
   value = data[1].split(':')[1]
   ifTable[ oid ] = int(value)    # integer

#*********************************************************************
cmd = "snmpwalk -v2c -c %s  %s %s "  % (community, host, oid4)
fp = os.popen( cmd )
snmp = fp.read().splitlines()   # split the outout into a list of "lines"
ifDescr = {}
for i in range(len(snmp)):
   data = snmp[i].split('=')
   oid = data[0].split(dot)[-1]
   value = data[1].split(':')[1]
   if oid in ifTable:
      ifDescr[ ifTable[oid] ] = value	# key is integer
#
# ifDescr
   

#*********************************************************************
cmd = "snmpwalk -v2c -c %s  %s %s "  % (community, host, oid1)
fp = os.popen( cmd )
snmp = fp.read().splitlines()   # split the outout into a list of "lines"
macTable = {}
for i in range(len(snmp)):
   data = snmp[i].split('=')
   tmp = data[0].split(dot)[6:11]
   oid = dot.join(tmp)
   value = data[1].split(':')[1]
   # print oid, value
   macTable[ oid ] = value

#*********************************************************************
print "The MAC address table of Switch=%s for VLAN=%s" % (host, vlan)
print "----------------------------------"
print "%-20s  %6s  %-20s %-s" % ("MIB OID", "ifIndex", "MAC address", "interface")
cmd = "snmpwalk -v2c -c %s  %s %s "  % (community, host, oid2)
fp = os.popen( cmd )
snmp = fp.read().splitlines()   # split the outout into a list of "lines"
ifIndex = {}
for i in range(len(snmp)):
   data = snmp[i].split('=')
   tmp = data[0].split(dot)[6:11]
   oid = dot.join(tmp)
   value = int(data[1].split(':')[1])
   if oid in macTable:
      if value in ifDescr:
         print "%-20s  %6d  %-20s %-s" % (oid, value, macTable[oid], ifDescr[value])
      else:
         print "%-20s  %6d  %-20s %-s" % (oid, value, macTable[oid], "unknown")
         # print "Assert:", oid, value, macTable[oid], "unknown ifIndex in the MAC address table"
   else:
         print "Assert:", oid, value, "unknown oid in MAC Address table"
