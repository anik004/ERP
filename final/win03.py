#!/usr/bin/python
import os
import getpass
import subprocess
import re
from sys import *
from log4erp import *

try:
    hostname = argv[1]
    username = argv[2]
    password = argv[3]
    location = argv[4]
    write(location.strip('\\') + '\\reflogfile.log',"win03:This command is used to check the user existance")
    command = 'c:\python27\python '+ location.strip('\\') + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' \"exit\"'
    #print command
    write(location.strip('\\') + '\\reflogfile.log',command)
    command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
    out, err = command.communicate()
    write(location.strip('\\') + '\\reflogfile.log',out)
    if 'STATUS_LOGON_FAILURE' in out:
        print 'PRE:F:user existance check for the ' + hostname + ' is failed'
    else:
        print 'PRE:P:user existance check for the ' + hostname + ' is successful'

except Exception as e:
        if str(e) == "[Errno -2] Name or service not known":
            print "PRE:F:GERR_0201:Hostname unknown"
            write(location.strip('\\') + '\\reflogfile.log','PRE:F:GERR_0201:Hostname unknown')
        elif str(e).strip() == "list index out of range":
            print "PRE:F:GERR_0202:Argument/s missing for the script"
            write(location.strip('\\') + '\\reflogfile.log','PRE:F:GERR_0202:Argument/s missing for the script')
        elif str(e) == "Authentication failed.":
            print "PRE:F:GERR_0203:Authentication failed."
            write(location.strip('\\') + '\\reflogfile.log','PRE:F:GERR_0203:Authentication failed.')
        elif str(e) == "[Errno 110] Connection timed out":
            print "PRE:F:GERR_0204:Host Unreachable"
            write(location.strip('\\') + '\\reflogfile.log','PRE:F:GERR_0204:Host Unreachable')
        elif "getaddrinfo failed" in str(e):
            print "PRE:F:GERR_0205: Please check the hostname that you have provide"
            write(location.strip('\\') + '\\reflogfile.log','PRE:F:GERR_0205: Please check the hostname that you have provide')
        elif "[Errno None] Unable to connect to port 22" in str(e):
            print "PRE:F:GERR_0206:Host Unreachable or Unable to connect to port 22"
            write(location.strip('\\') + '\\reflogfile.log','PRE:F:GERR_0206:Host Unreachable or Unable to connect to port 22')
        else:
            print "PRE:F: " + str(e)
            write(location.strip('\\') + '\\reflogfile.log',"PRE:F: " + str(e))
