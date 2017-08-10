#import paramiko
import re
import log4erp
from log4erp import *
#from paramiko import *
import os.path
from sys import *
import subprocess

try:
    if argv[1] == "--u":
        print "c:\python27\python ' + loc.strip('\\') + '\transport.py <path in Source> <Transport id> <Path in target> <target IP> <target Application SID> <Domain name> <Target Sudo Login User Name> <Target Sudo User Password> <Source Application SID> <Location> <loc.strip() + '\\' + ref_id>"

    else:
		def get_result(out):
			for each in out.split('\n'):
				if 'tp finished with return code' in each:
					return each.split(':')[1]

		s_path = argv[1].rstrip('\\')

		tr_id = str(argv[2]).strip()
		t_path = argv[3].rstrip('\\')

		t_hostname = argv[4]
		t_sid = argv[5].lower()
		domain = argv[6].upper()
		t_username = argv[7]
		t_password = argv[8]
		tr_part = tr_id[4:]
		sid = t_sid.upper()
		s_sid = argv[9].upper()
		s_sid = tr_id[:3].upper()
		ref_id = argv[11]
		location = argv[10].strip('\\') # kernel path
		loc = argv[12]			# script location
		count1 = len(t_sid)
		count2 = len(s_sid)

		write(loc.strip() + '\\' + ref_id,"POST:P:import triggered")
		write(loc.strip('\\') + '\\reflogfile.log',"win13.py :This command is used to check if the share folder exixts or not")
		command = 'c:\\python27\\python ' + loc.strip('\\') + '\\wmiexec.py ' + t_username.strip() + ':' + t_password.strip() + '@' + t_hostname + ' "dir ' + location[:2] + ' /s /b | findstr erp_trans"'
		#print command
		write(loc.strip('\\') + '\\reflogfile.log',command)
		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
		out, err = command.communicate()
		write(loc.strip('\\') + '\\reflogfile.log',out)
		profilepath = out
#		print profilepath
		#print 'Prof: ' + profilepath
		if 'erp_trans' not in profilepath:
			write(loc.strip('\\') + '\\reflogfile.log','win13.py : This command is used to cretae the share folder and give full permission to the shared folder')
			command = 'c:\python27\python ' + loc.strip('\\') + '\wmiexec.py ' + t_username.strip() + ':' + t_password.strip() + '@' + t_hostname + ' \"md ' + location[:2] + '\\erp_trans && net share sharename=' + location[:2] + '\\erp_trans /grant:everyone,full\"'
#			print command
			write(loc.strip('\\') + '\\reflogfile.log',command)
			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
			out, err = command.communicate()
#			print out
			write(loc.strip('\\') + '\\reflogfile.log',out)
		else:
			write(loc.strip('\\') + '\\reflogfile.log','win13.py :If the share folder already exists print skip')
#			print "skip"

		if count1 > 3 or count1 < 3 or count2 > 3 or count2 < 3:
			print "POST:F:Wrong syntax of Target/Source SID"
			write(loc.strip() + '\\' + ref_id,"Wrong syntax of Target/Source SID")
		else:
			for name in "cofiles", "data":
				if name == "cofiles":
					initial = "K"
					filename = initial + tr_part + '.' + s_sid
				else:
					initial = "R"
					filename = initial + tr_part + '.' + s_sid


				localpath = s_path + "\\" + name + "\\" + filename
				write(loc.strip('\\') + '\\reflogfile.log','win13 : This command is used to check the existence of profilepath')
				command = 'c:\\python27\\python.exe ' + loc.strip('\\') + '\wmiexec.py ' + t_username.strip() + ':' + t_password.strip() + '@' + t_hostname + ' "powershell.exe;test-path ' + localpath + '"'
				print command
				write(loc.strip('\\') + '\\reflogfile.log', command)
				command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
				out, err = command.communicate()
				print out
				write(loc.strip('\\') + '\\reflogfile.log', out)

				#if "False" in str(out):
				#	print "POST:F:The local Path does not exists"
				#	write(loc.strip('\\') + '\\' + ref_id, "POST:F:The local Path does not exists")
				#	exit()
				filepath =  t_path + "\\" + name + "\\" + filename
				write(loc.strip('\\') + '\\reflogfile.log','win13.py : This command is used to copy the localpath to the target share folder')
				command = 'copy ' + localpath + ' \\\\' + t_hostname + '\\sharename /Y'
				#print command
				write(loc.strip('\\') + '\\reflogfile.log',command)
				command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
				out, err = command.communicate()
				write(loc.strip('\\') + '\\reflogfile.log',out)
				status = command.returncode
				if "1" in out:
					write(loc.strip('\\') + '\\reflogfile.log','win13.py : This command is used for copying files')
					command = 'c:\python27\python ' + loc.strip('\\') + '\wmiexec.py ' + t_username.strip() + ':' + t_password.strip() + '@' + t_hostname + ' \"copy ' + location[:2] + '\\erp_trans\\' + filename + ' ' + filepath + ' /Y\"'
				#	print command
					write(loc.strip('\\') + '\\reflogfile.log',command)
					command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
					out, err = command.communicate()
					write(loc.strip('\\') + '\\reflogfile.log',out)
					status = command.returncode
					if "1" in out:
						print "POST:P: The File " + initial + tr_part + "." + s_sid + " has been transfered successfully."
						write(loc.strip('\\') + '\\' + ref_id,"POST:P: The File " + initial + tr_part + "." + s_sid + " has been transfered successfully.")
					else:
						print 'POST:F:Agent file transfer failed'
						write(loc.strip('\\') + '\\' + ref_id,'POST:F:Agent file transfer failed')
						exit()
			write(loc.strip('\\') + '\\reflogfile.log','win13.py : This command is used to add to buffer before importing')
			command = 'c:\python27\python ' + loc.strip('\\') + '\wmiexec.py ' + t_username.strip() + ':' + t_password.strip() + '@' + t_hostname + ' \"' + location.strip("\\") + '\\tp addtobuffer ' + tr_id + " " + t_sid  + ' Client=000 pf=' + t_path + '\\bin\TP_' + domain + '.PFL\"'
			print command
			write(loc.strip('\\') + '\\reflogfile.log',command)
			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
			out, err = command.communicate()
			print out
			write(loc.strip('\\') + '\\reflogfile.log',out)
			status = get_result(out)
#			print status
			if status.strip() == '0' or status.strip() == '4':
				write(loc.strip('\\') + '\\reflogfile.log','win13.py : This command is used to tp modifying buffer')
				command = 'c:\python27\python ' + loc.strip('\\') + '\wmiexec.py ' + t_username.strip() + ':' + t_password.strip() + '@' + t_hostname + ' \"' + location.strip("\\") + '\\tp modbuffer ' + tr_id + " " + t_sid  + ' mode=u+12 Client=000 pf=' + t_path + '\\bin\TP_' + domain + '.PFL\"'
				print command
				write(loc.strip('\\') + '\\reflogfile.log',command)
				command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
				out, err = command.communicate()
				print out
				write(loc.strip('\\') + '\\reflogfile.log',out)
				status = get_result(out)
#				print status
				if status.strip() == '0' or status.strip() == '4':
					write(loc.strip('\\') + '\\reflogfile.log','win13.py this command is used for tp import')
					command = 'c:\python27\python ' + loc.strip('\\') + '\wmiexec.py ' + t_username.strip() + ':' + t_password.strip() + '@' + t_hostname + ' \"' + location.strip("\\") + '\\tp import ' + tr_id + " " +  t_sid + ' Client=000 pf=' + t_path + '\\bin\TP_' + domain + '.PFL\"'
					print command
					write(loc.strip('\\') + '\\reflogfile.log',command)
					command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
					out, err = command.communicate()
					print out
					write(loc.strip('\\') + '\\reflogfile.log',out)
					status = get_result(out)
					print status
					if status.strip() == '0' or status.strip() == '4':
						print "POST:P:TR " + tr_id + " import is successfull in the target application server " + t_hostname
						write(loc.strip('\\') + '\\' + ref_id,"POST:P:TR " + tr_id + " import is successfull in the target application server " + t_hostname)
					else:
						print "POST:F: TR " + tr_id + " import is failed with the error code: " + status
						write(loc.strip('\\') + '\\' + ref_id,"POST:F: TR " + tr_id + " import is failed with the error code: " + status)
				else:
					print "POST:F: The modbuffer for the TR " + tr_id + " has failed"
					write(loc.strip('\\') + '\\' + ref_id,"POST:F: The modbuffer for the TR " + tr_id + " has failed")
			else:
				print "POST:F: TR " + tr_id + " is failed with the error code: " + status
				write(loc.strip('\\') + '\\' + ref_id, "POST:F: TR " + tr_id + " is failed with the error code: " + status)



except Exception as e:
	if str(e) == "[Errno -2] Name or service not known":
		print "POST:F:GERR_0201:Hostname unknown"
		write(loc.strip('\\') + '\\' + ref_id,'POST:F:GERR_0201:Hostname unknown')
		write(loc.strip('\\') + '\\reflogfile.log', 'POST:F:GERR_0201:Hostname unknown')
	elif str(e).strip() == "list index out of range":
		print "POST:F:GERR_0202:Argument/s missing for the script"
	elif str(e) == "Authentication failed.":
		print "POST:F:GERR_0203:Authentication failed."
		write(loc.strip('\\') + '\\reflogfile.log', 'POST:F:GERR_0203:Authentication failed.')
		write(loc.strip('\\') + '\\' + ref_id,'POST:F:GERR_0203:Authentication failed.')
	elif str(e) == "[Errno 110] Connection timed out":
		print "POST:F:GERR_0204:Host Unreachable"
		write(loc.strip('\\') + '\\' + ref_id,'POST:F:GERR_0204:Host Unreachable')
		write(loc.strip('\\') + '\\reflogfile.log', 'POST:F:GERR_0204:Host Unreachable')
	elif "getaddrinfo failed" in str(e):
		print "POST:F:GERR_0205: Please check the hostname that you have provide"
		write(loc.strip('\\') + '\\' + ref_id,'POST:F:GERR_0205: Please check the hostname that you have provide')
		write(loc.strip('\\') + '\\reflogfile.log', 'POST:F:GERR_0205: Please check the hostname that you have provide')
	elif "[Errno None] Unable to connect to port 22" in str(e):
		print "POST:F:GERR_0206:Host Unreachable or Unable to connect to port 22"
		write(loc.strip('\\') + '\\' + ref_id,'POST:F:GERR_0206:Host Unreachable or Unable to connect to port 22')
		write(loc.strip('\\') + '\\reflogfile.log','POST:F:GERR_0206:Host Unreachable or Unable to connect to port 22')
	else:
		print "POST:F: " + str(e)
		write(loc.strip('\\') + '\\' + ref_id,"POST:F: " + str(e))
		write(loc.strip('\\') + '\\reflogfile.log', "POST:F: " + str(e))
