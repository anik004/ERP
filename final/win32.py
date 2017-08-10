import re
import log4erp
from log4erp import *
import os.path
from sys import *
import subprocess

try:
    if argv[1] == "--u":
        print "c:\python27\python ' + loc.strip('\\') + '\transport.py <path in Source> <Transport id> <Path in target> <target IP> <target Application SID> <Domain name> <Target Sudo Login User Name> <Target Sudo User Password> <Source Application SID> <Location> <location.strip('\\') + ref_id>"

    else:


		t_path = argv[1].rstrip('\\')
		t_hostname = argv[2]
		t_username = argv[3]
		t_password = argv[4]


		location.strip('\\') + ref_id = argv[7]
		location = argv[5] # kernel path
		loc = argv[6]			# script location
	
	#	command = 'c:\python27\python ' + loc.strip('\\') + '\wmiexec.py ' + argv[2].strip() + ':' + argv[3].strip() + '@' + argv[1] + ' \'md ' + location + '\\erp_trans && net share sharename=' + argv[7] + '\\erp_trans /grant:everyone,full\''
	#		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
	#    	out, err = command.communicate()
		write(location.strip('\\') + reflogfile.log,"win32:This command creates a directory transport")
		command = 'mkdir ' + loc.strip('\\') + '\\transport'
		write(location.strip('\\') + reflogfile.log,command)
		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
		out, err = command.communicate()
		write(location.strip('\\') + reflogfile.log,out)
		file_path = open (loc + '\\' + location.strip('\\') + ref_id + '_transport.txt')
		file_p = file_path.readlines() # --------------- Data will get removed from file_path ------------
		length = len(file_p)

		for line in range (0, length):
			tr_id = file_p[line].strip()
			tr_part = tr_id[4:]
			s_sid = tr_id[:3].upper()
			for name in "cofiles", "data":
				if name == "cofiles":
					initial = "K"
					filename = initial + tr_part + '.' + s_sid
				else:
					initial = "R"
					filename = initial + tr_part + '.' + s_sid

		#command = 'copy ' + localpath + ' \\\\' + t_hostname + '\\sharename /Y'
	        #print command
    	        #command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
    	        #out, err = command.communicate()
	        #status = command.returncode
		#if status == 0:
		write(location.strip('\\') + reflogfile.log,"win32:This command copies the file to the sharefolder")
		command = 'c:\python27\python ' + loc.strip('\\') + '\wmiexec.py ' + t_username.strip() + ':' + t_password.strip() + '@' + t_hostname + ' \"copy ' + t_path + "\\" + name + "\\" + filename + ' ' + location[:2] + '\\erp_trans\\' + ' /Y\"'
		write(location.strip('\\') + reflogfile.log,command)
		print command
		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
		out, err = command.communicate()
		write(location.strip('\\') + reflogfile.log,out)
		status = command.returncode
		if "1" in out:
				write(location.strip('\\') + reflogfile.log,"win32:This command copies the file from sharefolder to the transport directory")
				command = 'copy \\\\' + t_hostname + '\\sharename\\' + filename + ' ' + loc.strip('\\') + '\\transport /Y'
				write(location.strip('\\') + reflogfile.log,command)
				#print command
				command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
				out, err = command.communicate()
				write(location.strip('\\') + reflogfile.log,out)
				status = command.returncode
				if "1" in out:
					print "POST:P: The File " + initial + tr_part + "." + s_sid + " has been transfered successfully."
					write(location.strip('\\') + ref_id,"POST:P: The File " + initial + tr_part + "." + s_sid + " has been transfered successfully.")
				else:
					print 'POST:F:Agent file transfer failed'
					write(location.strip('\\') + ref_id,'POST:F:Agent file transfer failed')
					exit()

except Exception as e:
	if str(e) == "[Errno -2] Name or service not known":
		print "POST:F:GERR_0201:Hostname unknown"
		write(location.strip('\\') + reflogfile.log,"POST:F:GERR_0201:Hostname unknown")
		write(location.strip('\\') + ref_id,'POST:F:GERR_0201:Hostname unknown')
	elif str(e).strip() == "list index out of range":
		print "POST:F:GERR_0202:Argument/s missing for the script"
		write(location.strip('\\') + reflogfile.log,"POST:F:GERR_0202:Argument/s missing for the script")
	elif str(e) == "Authentication failed.":
		print "POST:F:GERR_0203:Authentication failed."
		write(location.strip('\\') + ref_id,'POST:F:GERR_0203:Authentication failed.')
		write(location.strip('\\') + reflogfile.log,"POST:F:GERR_0203:Authentication failed.")
	elif str(e) == "[Errno 110] Connection timed out":
		print "POST:F:GERR_0204:Host Unreachable"
		write(location.strip('\\') + ref_id,'POST:F:GERR_0204:Host Unreachable')
		write(location.strip('\\') + reflogfile.log,"POST:F:GERR_0204:Host Unreachable")
	elif "getaddrinfo failed" in str(e):
		print "POST:F:GERR_0205: Please check the hostname that you have provide"
		write(location.strip('\\') + ref_id,'POST:F:GERR_0205: Please check the hostname that you have provide')
		write(location.strip('\\') + reflogfile.log,"POST:F:GERR_0205: Please check the hostname that you have provide")
	elif "[Errno None] Unable to connect to port 22" in str(e):
		print "POST:F:GERR_0206:Host Unreachable or Unable to connect to port 22"
		write(location.strip('\\') + ref_id,'POST:F:GERR_0206:Host Unreachable or Unable to connect to port 22')
		write(location.strip('\\') + reflogfile.log,"POST:F:GERR_0206:Host Unreachable or Unable to connect to port 22")
	else:
		print "POST:F: " + str(e)
		write(location.strip('\\') + ref_id,"POST:F: " + str(e))
		write(location.strip('\\') + reflogfile.log,"POST:F: " + str(e))
