#!/usr/bin/python
#
#  simple device configuraiton - changing the location
 
import telnetlib
import sys
 
if (len(sys.argv) == 1):
   print "syntax: python telnet05.py <device>"
   sys.exit()

host = sys.argv[1]
username  = "user"
password1 = "user"
password2 = "cisco"
TIMEOUT = 2

tn = telnetlib.Telnet(host, timeout=TIMEOUT)

ret = tn.read_until("Username: ", TIMEOUT)
if ret.find('Username') > 0:    # that is "found"
   tn.write(username + "\n")
   tn.read_until("Password: ", TIMEOUT)
   tn.write(password1 + "\n")
elif ret.find('Password') > 0:    # that is "found"
   tn.write(password1 + "\n")
else:
   print "unexplected", ret
   sys.exit()

# enable: from user mode to privilege mode
tn.write("enable\n")
tn.read_until("Password:")
tn.write(password2+"\n")

# enter into configuration mode
tn.write("configure terminal\n")
tn.read_until("(config)#", TIMEOUT)

tn.write("location CDM-369"+"\n")
tn.write("exit"+"\n")
tn.write("exit"+"\n")
output=tn.read_all()
tn.close()
 
print output
