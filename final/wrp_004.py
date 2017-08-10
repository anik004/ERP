from os import *
from sys import *
from subprocess import *
import subprocess

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
		profile_path = argv[11]

		if os_name.lower() == 'windows':
			command = 'c:\python27\python ' + location.strip('\\') + '\win10.py ' + hostname + ' ' + username + ' ' + password + ' ' + appsid + ' ' + drive + ' ' + location + ' ' + ref_id + ' ' + inst_no
		elif os_name.lower() == 'redhat' or os_name.lower() == 'aix':
			command = 'python ' + location.strip('\\') + '/lin17 ' + hostname + ' ' + username + ' ' + password + ' ' + appsid + ' ' + inst_no + ' ' + inst_nm + ' ' + ref_id + ' ' +  profile_path
			print command
		elif os_name.upper() == 'SUSE_LINUX':
			command = 'python ' + location.strip('\\') + '/lin17 ' + hostname + ' ' + username + ' ' + password + ' ' + appsid + ' ' + inst_no + ' ' + inst_nm + ' ' + ref_id + ' ' +  profile_path
                        print command

		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
	        out, err = command.communicate()
		print out
        	status = command.returncode
		if status != 0:
			print 'POST:F:The script execution has failed'

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
