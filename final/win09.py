#!/usr/bin/python 
import re
from log4erp import *
from sys import *
import subprocess
import os
try:
  hostname=argv[1]
  username = argv[2]
  password = argv[3]
  appsid = argv[4]
  drive = argv[5]
  location = argv[6]
  logfile = argv[7]
  """
  command = 'c:\python27\python ' + location.strip("\\") + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' \'where /r ' + drive + ': stopsap.exe\''
  command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
  out, err = command.communicate()
  out = out.split('\n')
  for line in out:
    if re.search('DRL',line):
        if re.search('SYS',line):
	    if 'BKP' not in line:
#	    print line
	        path = line.split('\\')
	        del path[-1]
	        path = '\\'.join(path)
  """
  write(location.strip('\\') + '\\reflogfile.log','win09: This command is used to get the instance number of the target system')
  command = 'c:\\python27\\python.exe ' + location.strip('\\') + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "powershell.exe;test-path ' + drive[:1] + ':\usr\sap\\' + appsid + '"'
#  print command
  write(location.strip('\\') + '\\reflogfile.log', command)
  command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
  out, err = command.communicate()
  #print out
  write(location.strip('\\') + '\\reflogfile.log', out)

  if "False" in str(out):
      print "POST:F:The kernel Path does not exists"
      write(location.strip('\\') + '\\' + logfile,"POST:F:The kernel Path does not exists")
  else:


      command='c:\python27\python ' + location.strip('\\') + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "' + drive[:1] + ': & cd \usr\sap\\' + appsid + ' & dir"'
 #     print command
      write(location.strip('\\') + '\\reflogfile.log',command)
      #print "hi"
      command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
      out, err = command.communicate()
      #print out
      write(location.strip('\\') + '\\reflogfile.log',out)
      out = out.split('\n')
      for line in out:
        #print line
        if re.search('DVEBMGS|ASCS',line):
            #print "hello"
            match = line.split()
            match =  match[4]
            instance = match[-2:]
            write(location.strip('\\') + '\\reflogfile.log','win09: This command is used to start the SAP system')
            command = 'c:\python27\python ' + location.strip('\\') + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "' + drive[:1] + ': & cd ' + drive + ' & startsap.exe name=' + appsid + ' nr=' + instance + ' SAPDIAHOST=' + hostname + '"'
  #          print command
            write(location.strip('\\') + '\\reflogfile.log',command)
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            #print out
            write(location.strip('\\') + '\\reflogfile.log',out)
            status = command.returncode
            if "STARTSAP failed" in out:
                print 'POST:F:The sap system has not been started'
                write(location.strip('\\') + '\\' + logfile, 'POST:F:The sap system has not been started')
                exit()

            else:
                print 'POST:P:The sap system has been started successfully'
                write(location.strip('\\') + '\\' + logfile, 'POST:P:The sap system has been started successfully')


except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "SAPSTART:F:GERR_3001:Hostname unknown"
        write(location.strip('\\') + '\\' + logfile,'POST:F: Hostname unknown [Error Code - 3001]')
        write(location.strip('\\') + '\\reflogfile.log','POST:F: Hostname unknown [Error Code - 3001]')
    elif str(e).strip() == "list index out of range":
        print "SAPSTART:F:GERR_3002:Argument/s missing for sapstartapp script"
        write(location.strip('\\') + '\\reflogfile.log','SAPSTART:F:GERR_3002:Argument/s missing for sapstartapp script')
    elif str(e) == "Authentication failed.":
        print "SAPSTART:F:GERR_3003:Authentication failed."
        write(location.strip('\\') + '\\' + logfile,'POST:F:Authentication failed[Error Code - 3003]')
        write(location.strip('\\') + '\\reflogfile.log','POST:F:Authentication failed[Error Code - 3003]')
    elif str(e) == "[Errno 110] Connection timed out":
        print "SAPSTART:F:GERR_3004:Host Unreachable"
        write(location.strip('\\') + '\\' + logfile,'POST:F:Host Unreachable.[Error Code - 3004]')
        write(location.strip('\\') + '\\reflogfile.log','POST:F:Host Unreachable.[Error Code - 3004]')
    elif "getaddrinfo failed" in str(e):
        print "SAPSTART:F:GERR_3005: Please check the hostname that you have provide"
        write(location.strip('\\') + '\\' + logfile,'POST:F: Please check the hostname that you have provide [Error Code - 3005]')
        write(location.strip('\\') + '\\reflogfile.log','POST:F: Please check the hostname that you have provide [Error Code - 3005]')
    elif "[Errno None] Unable to connect to port 22 on" in str(e):
        print "SAPSTART:F:GERR_3006:Host Unreachable or Unable to connect to port 22"
        write(location.strip('\\') + '\\' + logfile,'POST:F: Host Unreachable or Unable to connect to port 22 [Error Code - 3006]')
        write(location.strip('\\') + '\\reflogfile.log','POST:F: Host Unreachable or Unable to connect to port 22 [Error Code - 3006]')
    else:
        print "SAPSTART:F: " + str(e)
        write(location.strip('\\') + '\\' + logfile,"POST:F: " + str(e))
        write(location.strip('\\') + '\\reflogfile.log'.log,'POST:F: ' + str(e))

