import os
from os import *
import sys
from sys import *
import subprocess
from subprocess import *
from log4erp import *

try:
	t_host = argv[1] 
	t_user = argv[2]
	t_pass = argv[3]
	
	t_dbsid = argv[4] 
	t_clnt = argv[5]
	
	location = argv[6].strip('\\')
	ref_id = argv[7]

	local_os = os.name
	############ LINUX #################
	if local_os.lower() == 'posix':
	####################################

		write('reflogfile.log',"wrp_008:This command calls the lin26 script")
		command = 'python lin26 ' + location + '\\lin26 ' + t_host + ' ' + t_user + ' ' + t_pass + ' ' + t_dbsid + ' ' + t_clnt
		write('reflogfile.log',command)
		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()
                status = command.returncode
		if status != 0:
                        print 'POST:F:The script execution has failed'
			write('reflogfile.log','POST:F:The script execution has failed')
	
	########### OTHER (WINDOWS) ########
	else:
	####################################

		write('reflogfile.log',"wrp_008:This command calls the win19 script")
		command = 'c:\\python27\\python.exe ' + location + '\win19 ' + t_host + ' ' + t_user + ' ' + t_pass + ' ' + t_dbsid + ' ' + t_dbsid + ' ' + t_clnt + ' ' + location + ' ' + ref_id
		write('reflogfile.log',command)
		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()
                status = command.returncode
                if status != 0:
                        print 'POST:F:The script execution has failed'
			write('reflogfile.log','POST:F:The script execution has failed')

		
except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "POST:F:GERR_3001:Hostname unknown"
	write('reflogfile.log',"POST:F:GERR_3001:Hostname unknown")
    elif str(e).strip() == "list index out of range":
        print "POST:F:GERR_3002:Argument/s missing"
	write('reflogfile.log',"POST:F:GERR_3002:Argument/s missing")
    elif str(e) == "Authentication failed.":
        print "POST:F:GERR_3003:Authentication failed."
	write('reflogfile.log',"POST:F:GERR_3003:Authentication failed.")
    elif str(e) == "[Errno 110] Connection timed out":
        print "POST:F:GERR_3004:Host Unreachable"
	write('reflogfile.log',"POST:F:GERR_3004:Host Unreachable")
    elif "getaddrinfo failed" in str(e):
        print "POST:F:GERR_3005: Please check the hostname that you have provide"
	write('reflogfile.log',"POST:F:GERR_3005: Please check the hostname that you have provide")
    elif "[Errno None] Unable to connect to port 22 on" in str(e):
        print "POST:F:GERR_3006:Host Unreachable or Unable to connect to port 22"
	write('reflogfile.log',"POST:F:GERR_3006:Host Unreachable or Unable to connect to port 22")
    else:
        print "POST:F: " + str(e)
	write('reflogfile.log',"POST:F: " + str(e))

