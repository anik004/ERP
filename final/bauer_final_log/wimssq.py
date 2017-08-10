import os
from os import *
import sys
from sys import *
import subprocess
from subprocess import *
from log4erp import *

try:
	s_hostname = argv[1]
	s_username = argv[2]
	s_password = argv[3]
	s_db_sid = argv[4]
	s_bkp = argv[5]
	t_hostname = argv[6]
        t_username = argv[7]
        t_password = argv[8]
	t_db_sid = argv[9]
	t_bkp = argv[10]
	scr = argv[11].strip('\\') + '\\'
	ref_id = argv[12]
	seq = argv[13]

	local_os = os.name
	############ LINUX #################
	if local_os.lower() == 'posix':
	####################################

		command = 'echo "script is not available for this selection"'
		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()
                status = out.returncode
	
	########### OTHER (WINDOWS) ########
	else:
	####################################
		if str(seq).strip() == '1' or str(seq).strip() == '2':
			write('reflogfile.log',"wimssq:This command calls the win21 script")
			command = 'c:\python27\python.exe ' + scr + 'win21 ' + s_hostname + ' ' + s_username + ' ' + s_password + ' ' + s_db_sid + ' ' + s_db_sid + ' ' + s_bkp + ' ' + t_hostname + ' ' + t_username + ' ' + t_password + ' ' + t_bkp + ' ' + scr + ' ' + seq + ' ' + ref_id
			write('reflogfile.log',command)
			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                	out, err = command.communicate()
			print out

		elif str(seq).strip() == '3':
			write('reflogfile.log',"wimssq:This command calls the win20 script")
			command = 'c:\python27\python.exe ' + scr + 'win20 ' + t_hostname + ' ' + t_username + ' ' + t_password + ' ' + t_bkp + ' ' + t_db_sid + ' ' + scr +  ' ' + scr + ' ' + ref_id
			write('reflogfile.log',command)
			print command
			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                	out, err = command.communicate()
			print out

		else:
			print 'DB:F:The seq number (' + str(seq).strip() + ') entered here is wrong'
			write('reflogfile.log','DB:F:The seq number (' + str(seq).strip() + ') entered here is wrong')
		
except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "DB:F:GERR_3001:Hostname unknown"
	write('reflogfile.log',"DB:F:GERR_3001:Hostname unknown")
        #write(ref_id,'DB:F: Hostname unknown [Error Code - 3001]')
    elif str(e).strip() == "list index out of range":
        print "DB:F:GERR_3002:Argument/s missing"
	write('reflogfile.log',"DB:F:GERR_3002:Argument/s missing")
    elif str(e) == "Authentication failed.":
        print "DB:F:GERR_3003:Authentication failed."
	write('reflogfile.log',"DB:F:GERR_3003:Authentication failed.")
        #write(ref_id,'DB:F:Authentication failed[Error Code - 3003]')
    elif str(e) == "[Errno 110] Connection timed out":
        print "DB:F:GERR_3004:Host Unreachable"
	write('reflogfile.log',"DB:F:GERR_3004:Host Unreachable")
        #write(ref_id,'DB:F:Host Unreachable.[Error Code - 3004]')
    elif "getaddrinfo failed" in str(e):
        print "DB:F:GERR_3005: Please check the hostname that you have provide"
	write('reflogfile.log',"DB:F:GERR_3005: Please check the hostname that you have provide")
        #write(ref_id,'DB:F: Please check the hostname that you have provide [Error Code - 3005]')
    elif "[Errno None] Unable to connect to port 22 on" in str(e):
        print "DB:F:GERR_3006:Host Unreachable or Unable to connect to port 22"
	write('reflogfile.log',"DB:F:GERR_3006:Host Unreachable or Unable to connect to port 22")
        #write(ref_id,'DB:F: Host Unreachable or Unable to connect to port 22 [Error Code - 3006]')
    else:
        print "DB:F: " + str(e)
	write('reflogfile.log',"DB:F: " + str(e))
        #write(ref_id,"PRE:F: " + str(e))

