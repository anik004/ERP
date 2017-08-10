import re
import subprocess
from subprocess import *
from sys import *
import os
from log4erp import *
try:
  hostname = argv[1]
  username = argv[2]
  password = argv[3]
  location = argv[4]
  drive = argv[5]
  logfile = argv[6]
  write(drive.strip('\\') + '\\reflogfile.log','win29: This command is used to delete the share folder')
  command = 'c:\python27\python ' + drive.strip('\\') + '\wmiexec.py ' + argv[2].strip() + ':' + argv[3].strip() + '@' + argv[1] + ' \"rd ' + location[:2] +  '\\erp_trans\"'
  write(drive.strip('\\') + '\\reflogfile.log',command)
  command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
  out, err = command.communicate()
  write(drive.strip('\\') + '\\reflogfile.log',out)
  if command.returncode == 0:
    print 'POST:P:Deletion of sharefolder is successful'
    write(drive.strip('\\') + '\\' + logfile,'POST:P:Deletion of sharefolder is successful')
  else:
    print 'POST:P:Deletion of sharefolder failed'
    write(drive.strip('\\') + '\\' + logfile,'POST:P:Deletion of sharefolder failed')


except Exception as e:
        if str(e) == "[Errno -2] Name or service not known":
            print "PRE:F:GERR_0201:Hostname unknown"
            write(drive.strip('\\') + '\\reflogfile.log','PRE:F:GERR_0201:Hostname unknown')
            write(drive.strip('\\') + '\\' + logfile, 'PRE:F:GERR_0201:Hostname unknown')
        elif str(e).strip() == "list index out of range":
            print "PRE:F:GERR_0202:Argument/s missing for the script"
        elif str(e) == "Authentication failed.":
            print "PRE:F:GERR_0203:Authentication failed."
            write(drive.strip('\\') + '\\reflogfile.log','PRE:F:GERR_0203:Authentication failed.')
            write(drive.strip('\\') + '\\' + logfile, 'PRE:F:GERR_0203:Authentication failed.')
        elif str(e) == "[Errno 110] Connection timed out":
            print "PRE:F:GERR_0204:Host Unreachable"
            write(drive.strip('\\') + '\\reflogfile.log','PRE:F:GERR_0204:Host Unreachable')
            write(drive.strip('\\') + '\\' + logfile, 'PRE:F:GERR_0204:Host Unreachable')
        elif "getaddrinfo failed" in str(e):
            print "PRE:F:GERR_0205: Please check the hostname that you have provide"
            write(drive.strip('\\') + '\\reflogfile.log','PRE:F:GERR_0205: Please check the hostname that you have provide')
            write(drive.strip('\\') + '\\' + logfile,'PRE:F:GERR_0205: Please check the hostname that you have provide')
        elif "[Errno None] Unable to connect to port 22" in str(e):
            print "PRE:F:GERR_0206:Host Unreachable or Unable to connect to port 22"
            write(drive.strip('\\') + '\\reflogfile.log','PRE:F:GERR_0206:Host Unreachable or Unable to connect to port 22')
            write(drive.strip('\\') + '\\' + logfile,'PRE:F:GERR_0206:Host Unreachable or Unable to connect to port 22')
        else:
            print "PRE:F: " + str(e)
            write(drive.strip('\\') + '\\reflogfile.log',"PRE:F: " + str(e))
            write(drive.strip('\\') + '\\' + logfile, "PRE:F: " + str(e))
