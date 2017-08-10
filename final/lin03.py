from sys import *
from os import *
from subprocess import *
import os
import subprocess
from log4erp import *


try:
    if argv[1] == "--u":
        print "python ping.py <Target Hostname> <string>"
    else:
        t_host = argv[1]
        string = argv[2]
        osname = name
        if osname == "nt":
                command = "ping -n 1 " + str(t_host) #+ " > /dev/null 2>&1"
                response = os.system(command)

        elif osname == "posix":
            command = "ping -c1 -i3 " + str(t_host) + " > /dev/null 2>&1"

            response = os.system(command)

        if response == 0:
                print "PRE:P: The connectivity check for Target " + string + " Server (Hostname: " + t_host + " ) is Successful"
        else:
                print "PRE:F: Please check the IP address. Unable to reach the Host ( Hostname: " + t_host + " )"
#	       write (logfile, "PRE:F: Please check the IP address. Unable to reach the Host ( Hostname: " + t_host + " )")

except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "PRE:F:GERR_0201:Hostname unknown"
#	      write(logfile,'PRE:F:GERR_0201:Hostname unknown')
    elif "list index out of range" in str(e):
        print "PRE:F:GERR_0202:Argument/s missing for the script"
    elif str(e) == "Authentication failed.":
        print "PRE:F:GERR_0203:Authentication failed."
#	       write(logfile,'PRE:F:GERR_0203:Authentication failed.')
    elif str(e) == "[Errno 110] Connection timed out":
        print "PRE:F:GERR_0204:Host Unreachable"
#	       write(logfile,'PRE:F:GERR_0204:Host Unreachable')
    elif "getaddrinfo failed" in str(e):
        print "PRE:F:GERR_0205: Please check the hostname that you have provide"
#	       write(logfile,'PRE:F:GERR_0205: Please check the hostname that you have provide')
    elif "[Errno None] Unable to connect to port 22" in str(e):
        print "PRE:F:GERR_0206:Host Unreachable or Unable to connect to port 22"
#	       write(logfile,'PRE:F:GERR_0206:Host Unreachable or Unable to connect to port 22')
    else:
        print "PRE:F: " + str(e)
#	       write(logfile,'PRE:F: ' + str(e))
