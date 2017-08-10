#!/usr/bin/sh
from __future__ import division
import paramiko
import re
import glob
import os
from paramiko import *
from sys import *
import subprocess
from log4erp import *

def sapdelete(hostname, username, password, instance, databasesid, client, location, ref_id):
    command='c:\python27\python ' + location.strip('\\') + '\wmiexec.py ' + username.strip() + ':' + password + '@' + hostname + ' "sqlcmd -E -S ' + hostname + '\\' + instance + ' -Q \\"use ' + databasesid.upper() + ';delete from ' + databasesid.lower() + '.USR02 where BNAME=\'SAP*\' and MANDT=\'' + client + '\'\\""'
    print command
    write('reflogfile.log',command)
    command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
    out, err = command.communicate()
    #print out
    write('reflogfile.log',out)
    if command.returncode == 0:
        print "PRE:P:password has been reseted successfully for sap*"
    else:
        print "PRE:F:password has not been reseted successfully for sap*"
try:
    if argv[1] == "--u":
        print "usage: c:\python27\python  sapstarreset.py <Target Host> <Target Sudo Username> <Target Sudo Password> <instance> <databasesid> <clientno>"
    else:
        sapdelete(argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], argv[8])

except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "PRE:F:GERR_0201:Hostname unknown"
	write('reflogfile.log','PRE:F:GERR_0201:Hostname unknown')
    elif str(e).strip() == "list index out of range":
        print "PRE:F:GERR_0202:Argument/s missing for the script"
	write('reflogfile.log','PRE:F:GERR_0202:Argument/s missing for the script')
    elif str(e) == "Authentication failed.":
        print "PRE:F:GERR_0203:Authentication failed."
	write('reflogfile.log','PRE:F:GERR_0203:Authentication failed.')
    elif str(e) == "[Errno 110] Connection timed out":
        print "PRE:F:GERR_0204:Host Unreachable"
	write('reflogfile.log','PRE:F:GERR_0204:Host Unreachable')
    elif "getaddrinfo failed" in str(e):
        print "PRE:F:GERR_0205: Please check the hostname that you have provide"
	write('reflogfile.log','PRE:F:GERR_0205: Please check the hostname that you have provide')
    elif "[Errno None] Unable to connect to port 22" in str(e):
        print "PRE:F:GERR_0206:Host Unreachable or Unable to connect to port 22"
	write('reflogfile.log','PRE:F:GERR_0206:Host Unreachable or Unable to connect to port 22')
    else:
        print "PRE:F: " + str(e)
	write('reflogfile.log','PRE:F: ' + str(e))

