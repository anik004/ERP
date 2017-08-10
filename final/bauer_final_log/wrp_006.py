from os import *
from sys import *
from subprocess import *
import subprocess
from log4erp import *

try:
	if argv[1] == '--ani':
		print 'usage: h u p app dr ref os no nm'
	else:
		hostname = argv[1]
		username = argv[2]
		password = argv[3]
		appsid = argv[4]
		client_name = argv[5]
		step_name = argv[6]
		location = argv[7]
		drive = argv[8]
		logfile = argv[9]
		os_name = argv[10]
		steps=["PRE_DB13","PRE_JOBS","PRE_HTTPURLLOC","PRE_STRUST","PRE_SMTP","PRE_SICF","PRE_SE61","PRE_SE06_SCC4","PRE_RZ12SMLG","PRE_RFC","PRE_PRINTER","PRE_PARTNER","PRE_OPMODE","PRE_BTCOPTIONS","PRE_AL11","PRE_RZ70","PRE_SDCCN","PRE_SE06SCC4","PRE_SMQRSMQS","PRE_STMS","PRE_TPFET","PRE_BD54","PRE_BD64","PRE_WE21","PRE_USER","PRE_SM13","PRE_SM69","PRE_SMQ1SMQ2","PRE_TLOCK","PRE_MONI"]
		for step_name in steps:

		        if os_name.lower() == 'windows':
				write('reflogfile.log',"wrp_006:This command calls the win12 script")
				command = 'c:\python27\python ' + drive.strip('\\') + '\win12 ' + hostname + ' ' + username + ' ' + password + ' ' + appsid + ' ' + client_name + ' ' + step_name + ' ' + location + ' ' + drive
				write('reflogfile.log',command)
			elif os_name.lower() == 'redhat':
				write('reflogfile.log',"wrp_006:This command calls the lin19 script")
				command = 'python ' + drive.strip('\\').strip('\\') + '/lin19 ' + hostname + ' ' + username + ' ' + password + ' ' + client_name + ' ' + step_name + ' ' + appsid + ' ' + logfile + ' ' + drive
				write('reflogfile.log',command)
			print command
			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
	        	out, err = command.communicate()
			print out
        		status = command.returncode
			if status != 0:
				print 'PRE:F:The script execution has failed'
				write('reflogfile.log','PRE:F:The script execution has failed')

except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "PRE:F:GERR_3001:Hostname unknown"
	write('reflogfile.log',"PRE:F:GERR_3001:Hostname unknown")
    elif str(e).strip() == "list index out of range":
        print "PRE:F:GERR_3002:Argument/s missing"
	write('reflogfile.log',"PRE:F:GERR_3002:Argument/s missing")
    elif str(e) == "Authentication failed.":
        print "PRE:F:GERR_3003:Authentication failed."
	write('reflogfile.log',"PRE:F:GERR_3003:Authentication failed.")
    elif str(e) == "[Errno 110] Connection timed out":
        print "PRE:F:GERR_3004:Host Unreachable"
	write('reflogfile.log',"PRE:F:GERR_3004:Host Unreachable")
    elif "getaddrinfo failed" in str(e):
        print "PRE:F:GERR_3005: Please check the hostname that you have provide"
	write('reflogfile.log',"PRE:F:GERR_3005: Please check the hostname that you have provide")
    elif "[Errno None] Unable to connect to port 22 on" in str(e):
        print "PRE:F:GERR_3006:Host Unreachable or Unable to connect to port 22"
	write('reflogfile.log',"PRE:F:GERR_3006:Host Unreachable or Unable to connect to port 22")
    else:
        print "PRE:F: " + str(e)
	write('reflogfile.log',"PRE:F: " + str(e))
