#!/usr/bin/python
#
# get sinlge MIB object
#
from pysnmp.entity.rfc3413.oneliner import cmdgen

host = '172.26.1.101'
community = 'public'
port = 161
mibName = 'sysContact'

cmdGen = cmdgen.CommandGenerator()  # create an SNMP object
errorIndication, errorStatus, errorIndex, snmpResult = cmdGen.getCmd(
    cmdgen.CommunityData( community ),
    cmdgen.UdpTransportTarget((host, port)),
    cmdgen.MibVariable('SNMPv2-MIB', mibName, 0),
    lookupNames=True, lookupValues=True
)

print snmpResult
for name, val in snmpResult:
   print  'MIB OID: %s ' % (name)
   print  'MIB Value: %s ' % (val)
