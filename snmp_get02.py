#!/usr/bin/python
# get multiple SNMP objects

from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen = cmdgen.CommandGenerator()
errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    cmdgen.CommunityData('public'),
    cmdgen.UdpTransportTarget(('192.168.1.101', 161)),
    '1.3.6.1.2.1.1.1.0',
    '1.3.6.1.2.1.1.4.0',
    '1.3.6.1.2.1.1.5.0',
    '1.3.6.1.2.1.1.6.0'
)

for name, val in varBinds:
   print '%s = %s' % (name, val)
