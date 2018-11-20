#!/usr/bin/python
#****************************************************
#     getRoutingTable.py 
#	usage: python getRoutingTable.py <host> <vlan>
#
#     Description: get the IP Routing table from remote host/router
#***************************************************

from pysnmp.entity.rfc3413.oneliner import cmdgen
import sys
import snmpwalk

RouteTypeList = ('unknown', 'other', 'valid', 'direct', 'indirect', 'undefined')   # use tupple
RouteProtoList =('unknow', 'other', 'local', 'netmgmt', 'icmp', 'egp', 'ggp', 'hello', 'rip', 'is-is', 'es-is', 'igrp', 'bbn', 'ospf', 'bgp', 'undefined') 

#*********************************************************
#  main program
#*********************************************************
if (len(sys.argv) == 1):
   print "syntax: python %s <host>" % sys.argv[0]
   sys.exit()
   
host = sys.argv[1]
community = 'public' 

#**************************************
#    interface index
#**************************************
oidx = "1.3.6.1.2.1.2.2.1.1"   	
ifTable = {}
snmpResult = snmpwalk.snmpwalk(host, community, oidx, 0, ifTable)

#**************************************
#    interface description (ifDescr)
#**************************************
oidy = "1.3.6.1.2.1.2.2.1.2"	# ifDescr
tmpTbl = {}
ifDescrTable = {}
snmpResult = snmpwalk.snmpwalk(host, community, oidy, 0, tmpTbl)
for x in tmpTbl:
   if x in ifTable:
      ifDescrTable[ifTable[x]] = tmpTbl[x]  # key: ifIndex   val: ifDescr

     
#**************************************
#    ipRouteDest 
#**************************************
oid1 = "1.3.6.1.2.1.4.21.1.1"
ipRouteDest = {}
snmpwalk.snmpwalk(host, community, oid1, 1, ipRouteDest)

#**************************************
#    ipRouteIf 
#**************************************
oid2 = "1.3.6.1.2.1.4.21.1.2"
tmpTbl = {}
snmpwalk.snmpwalk(host, community, oid2, 0, tmpTbl)
for x in tmpTbl:
   if x in ifDescrTable:
      ipRouteIfTbl[x] = ifDescrTable[x]

#**************************************
#    ipRouteNextHop 
#**************************************
oid7 = "1.3.6.1.2.1.4.21.1.7"
ipRouteNextHop = {}
snmpwalk.snmpwalk(host, community, oid7, 1, ipRouteNextHop)

#**************************************
#    ipRouteType 
#**************************************
oid8 = "1.3.6.1.2.1.4.21.1.8"
ipRouteType = {}
snmpwalk.snmpwalk(host, community, oid8, 0, ipRouteType)

oid9 = "1.3.6.1.2.1.4.21.1.9"
ipRouteProto = {}
snmpwalk.snmpwalk(host, community, oid9, 0, ipRouteProto)

oid11 = "1.3.6.1.2.1.4.21.1.11"
ipRouteMask = {}
snmpwalk.snmpwalk(host, community, oid11, 1, ipRouteMask)

#**********************************************
#   complete reading SNMP data
#   print the ARP table
#*********************************************
print "%16s %16s %16s %12s %14s %16s\n" % ('OID', 'Interface', 'ipRouteNextHop', 'ipRouteType', 'ipRouteProto', 'ipRouteMask')
for i in ipRouteDest:
   rtype  = RouteTypeList[ ipRouteType[i] ]
   rproto = RouteProtoList[ ipRouteProto[i] ]
   print "%16s %16s %16s %8s(%d) %12s(%d) %16s" % (i, ipRouteDest[i], ipRouteNextHop[i], rtype, ipRouteType[i], rproto, ipRouteProto[i], ipRouteMask[i])
