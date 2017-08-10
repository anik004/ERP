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
		drive = argv[5]
		ref_id = argv[6]
		os_name = argv[7]
		inst_no = argv[8]
		inst_nm = argv[9]
		location = argv[10]

		if os_name.lower() == 'windows':
			write('reflogfile.log',"wrp_004:This command calls the win10 script")
			command = 'c:\python27\python ' + location.strip('\\') + '\win10 ' + hostname + ' ' + username + ' ' + password + ' ' + appsid + ' ' + drive + ' ' + location + ' ' + ref_id
			write('reflogfile.log',command)
		elif os_name.lower() == 'redhat':
			write('reflogfile.log',"wrp_004:This command calls the lin17 script")
			command = 'python ' + location.strip('\\') + '/lin17 ' + hostname + ' ' + username + ' ' + password + ' ' + appsid + ' ' + inst_no + ' ' + inst_nm + ' ' + ref_id
			write('reflogfile.log',command)
			print command

		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
	        out, err = command.communicate()
		print out
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
