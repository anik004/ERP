#!/usr/bin/python 
import re
from sys import *
import subprocess
import os
#from log4erp import *
try:
  hostname=argv[1]
  username = argv[2]
  password = argv[3]
  appsid = argv[4]
  drive = argv[5]
  location = argv[6]
  logfile = argv[7]
  """
  command = 'c:\python27\python ' + location.strip('\\') + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' \'where /r ' + drive + ': stopsap.exe\''
  print command
  command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
  out, err = command.communicate()
  out = out.split('\n')
  #print out
  for line in out:
    if re.search('DRL',line):
        if re.search('SYS',line):
	    if 'BKP' not in line:
    	        #print line
    	        path = line.split('\\')
	        del path[-1]
	        path = '\\'.join(path)
	        #print path
  """
  command='c:\python27\python ' + location.strip('\\') + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "' + drive[:1] + ': & cd \usr\sap\\' + appsid + ' & dir"'
  command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
  out, err = command.communicate()
  out = out.split('\n')
  for line in out:
    if re.search('DVEBMGS|ASCS',line):
	    match = line.split()
	    match =  match[4]
	    instance = match[-2:]
	    command = 'c:\python27\python ' + location.strip('\\') + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "' + drive[:1] + ': & cd '+ drive + ' & stopsap.exe name=' + appsid + ' nr=' + instance + ' SAPDIAHOST=' + hostname + '"'
	    print command
	    command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        out, err = command.communicate()
        #print out
        status = command.returncode
        if status == 0:
            print 'PRE:P:The sap system has been stopped successfully'
#            write (logfile, 'PRE:P:The sap system has been stopped successfully')
        else:
            print 'PRE:F:The sap system has not been stopped'
#            write (logfile, 'PRE:F:The sap system has not been stopped')
	
  except Exception as e:
        if str(e) == "[Errno -2] Name or service not known":
                print "SAPSTOPAPP:F:GERR_1201:Hostname unknown"
#                write(logfile,'PRE:F:Hostname unknown [Error Code - 1201]')
        elif str(e) == "list index out of range":
                print "SAPSTOPAPP:F:GERR_1202:Argument/s missing for the script"
        elif str(e) == "Authentication failed.":
                print "SAPSTOPAPP:F:GERR_1203:Authentication failed."
#                write(logfile,'PRE:F:Authentication failed.[Error Code - 1203]')
        elif str(e) == "[Errno 110] Connection timed out":
                print "SAPSTOPAPP:F:GERR_1204:Host Unreachable"
#                write(logfile,'PRE:F:Authentication failed.[Error Code - 1204]')
        elif "getaddrinfo failed" in str(e):
                print "SAPSTOPAPP:F:GERR_1205: Please check the hostname that you have provide"
#                write(logfile,'PRE:F:Please check the hostname that you have provide [Error Code - 1205]')
        elif "[Errno None] Unable to connect to port 22 on" in str(e):
                print "SAPSTOPAPP:F:GERR_1206:Host Unreachable or Unable to connect to port 22"
#                write(logfile,'PRE:F:Host Unreachable or Unable to connect to port 22 [Error Code - 1206]')
        elif "invalid decimal" in str(e):
                print "SAPSTOPAPP:F:GERR_1207:Unknown Error:" + str(e)
#                write(logfile,'PRE:F:Unknown Error:' + str(e) + '[Error Code - 1207]')
        else:
                print "SAPSTOPAPP:F:" + str(e)
#		write(logfile,"SAPSTOPAPP:F:" + str(e)) 
