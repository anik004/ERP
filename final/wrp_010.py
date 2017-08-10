import os
from os import *
import sys
from sys import *
import subprocess
from subprocess import *
from log4erp import *

try:
	hostname = argv[1]
	username = argv[2]
	password = argv[3]
	prof_path = argv[4]
	scr = argv[5].strip('\\')
	ref_id = argv[6]
	app_sid = argv[7]

	local_os = os.name
	############ LINUX #################
	if local_os.lower() == 'posix':
	####################################

		app_sid = argv[7]
		command = 'python ' + scr + '/lin23 ' + hostname + ' ' + username + ' ' + password + ' ' + app_sid + ' ' + prof_path
		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()
		print out
                status = command.returncode
		if status != 0:
                        print 'POST:F:The script execution has failed'
                        write(ref_id, 'POST:F:The script execution has failed')
	
	########### OTHER (WINDOWS) ########
	else:
	####################################

		command = 'c:\\python27\\python.exe ' + scr + '\win16 ' + hostname + ' ' + username + ' ' + password + ' ' + prof_path + ' ' + ref_id + ' ' + scr
		print command	
		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()
		print out
                status = command.returncode
                if status != 0:
                        print 'POST:F:The script execution has failed'
                        write(ref_id, 'POST:F:The script execution has failed')


		
except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "POST:F:GERR_3001:Hostname unknown"
    elif str(e).strip() == "list index out of range":
        print "POST:F:GERR_3002:Argument/s missing"
    elif str(e) == "Authentication failed.":
        print "POST:F:GERR_3003:Authentication failed."
    elif str(e) == "[Errno 110] Connection timed out":
        print "POST:F:GERR_3004:Host Unreachable"
    elif "getaddrinfo failed" in str(e):
        print "POST:F:GERR_3005: Please check the hostname that you have provide"
    elif "[Errno None] Unable to connect to port 22 on" in str(e):
        print "POST:F:GERR_3006:Host Unreachable or Unable to connect to port 22"
    else:
        print "POST:F: " + str(e)

