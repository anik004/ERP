import os
from os import *
import sys
from sys import *
import subprocess
from subprocess import *
from log4erp import *

try:
	s_path = argv[1]
	tr_id = argv[2]
	
	t_path = argv[3]
	t_host = argv[4]
	t_sid = argv[5]
	
	dom = argv[6]
	t_user = argv[7]
	t_passwd = argv[8]

	s_sid = argv[9]
	ref_id = argv[10]
	kernel = argv[11]
	path = argv[12].strip('\\')

	local_os = os.name
	############ LINUX #################
	if local_os.lower() == 'posix':
	####################################

		write('reflogfile.log',"wrp_016:This command calls the lin20 script")
		command = 'python ' + path + '\\lin20 ' + s_path + ' ' + tr_id + ' ' + t_path + ' ' + t_host + ' ' + t_sid + ' ' + dom + ' ' + t_user + ' ' + t_passwd + ' ' + s_sid + ' ' + ref_id
		write('reflogfile.log',command)
		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()
                status = command.returncode
	
	########### OTHER (WINDOWS) ########
	else:
	####################################

		write('reflogfile.log',"wrp_016:This command calls the win36 script")
		command = 'c:\\python27\\python.exe ' + path + '\win36 ' + s_path + ' ' + tr_id + ' ' + t_path + ' ' + t_host + ' ' + t_sid + ' ' + dom + ' ' + t_user + ' ' + t_passwd + ' ' + s_sid + ' ' + kernel + ' ' + ref_id + ' ' + path
		write('reflogfile.log',command)
		print command
		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()
		print out
                status = command.returncode
                if status != 0:
                        print 'POST:F:The script execution has failed'
                        write(ref_id, 'POST:F:The script execution has failed')
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

