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
		def get_result(out):
			for each in out.split('\n'):
				if 'tp finished with return code' in each:
					return each.split(':')[1].strip()

		s_path = argv[1].rstrip('\\')
		tr_id = str(argv[2]).strip()
		t_profile_path = argv[3].rstrip('\\')

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
		location = argv[10] # kernel pa		
		loc = argv[12]			# script location
		client = argv[13]
		count1 = len(t_sid)
		count2 = len(s_sid)
	
#	command = 'c:\python27\python ' + loc.strip('\\') + '\wmiexec.py ' + argv[2].strip() + ':' + argv[3].strip() + '@' + argv[1] + ' \'md ' + location + '\\erp_trans && net share sharename=' + argv[7] + '\\erp_trans /grant:everyone,full\''
#	command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
#    	out, err = command.communicate()
		write(loc.strip('\\') + '\\reflogfile.log','win34 : This command is used to check the existence of profilepath')
		command = 'c:\\python27\\python.exe ' + loc.strip('\\') + '\wmiexec.py ' + t_username.strip() + ':' + t_password.strip() + '@' + t_hostname + ' "powershell.exe;test-path ' + t_profile_path + '"'
		print command
		write(loc.strip('\\') + '\\reflogfile.log', command)
		command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		out, err = command.communicate()
		print out
		write(loc.strip('\\') + '\\reflogfile.log', out)

		if "False" in str(out):
			print "POST:F:The profile Path does not exists"
			#write(logfile, "POST:F:The profile Path does not exists")
		else:
			command = 'c:\\python27\\python ' + loc.strip('\\') + '\\wmiexec.py ' + t_username.strip() + ':' + t_password.strip() + '@' + t_hostname + ' "dir ' + t_profile_path + ' /s /b | findstr DVEBMGS* | findstr -V START"'
			write(loc.strip('\\') + '\\reflogfile.log',"win34:" + command)
			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
			out, err = command.communicate()
			write(loc.strip('\\') + '\\reflogfile.log',out)
			profilepath = out.split('\n')[3].strip()
			print profilepath
			command='c:\\python27\\python ' + loc.strip('\\') + '\\wmiexec.py ' + t_username.strip() + ':' + t_password.strip() + '@' + t_hostname + ' "powershell.exe;\"\\"get-content ' + profilepath.strip() + ' | findstr DIR_TRANS\\"\" | findstr -V #"'
			write(loc.strip('\\') + '\\reflogfile.log',"win34:" + command)
			print command
			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
			out, err = command.communicate()
			write(loc.strip('\\') + '\\reflogfile.log',out)
			#print out
			out=out.split('\n')
			#print out
			out=''.join(out)
			parameter = out.split('used',1)
			#print parameter
			parameter = parameter[1].strip()
			t_path = parameter.split('=')[1].strip()
			if count1 > 3 or count1 < 3 or count2 > 3 or count2 < 3:
				print "Wrong syntax of Target/Source SID"
				write(loc.strip('\\') + ref_id,"Wrong syntax of Target/Source SID")
			else:

				write(loc.strip('\\') + '\\reflogfile.log','win34 : this command is used to add to the buffer')
				command = 'c:\python27\python ' + loc.strip('\\') + '\wmiexec.py ' + t_username.strip() + ':' + t_password.strip() + '@' + t_hostname + ' \"' + location.strip("\\") + '\\tp addtobuffer ' + tr_id + " " + t_sid  + ' Client=' + client + '  pf=' + t_path + '\\bin\TP_' + domain + '.PFL\"'
				write(loc.strip('\\') + '\\reflogfile.log',"win34:" + command)
				print command
				command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
				out, err = command.communicate()
				write(loc.strip('\\') + '\\reflogfile.log',out)
				status = get_result(out)
				print status
				if status == '0' or status == '4':
					write(loc.strip('\\') + '\\reflogfile.log','win34 : this command is used to do modbuffer ')
					command = 'c:\python27\python ' + loc.strip('\\') + '\wmiexec.py ' + t_username.strip() + ':' + t_password.strip() + '@' + t_hostname + ' \"' + location.strip("\\") + '\\tp modbuffer ' + tr_id + " " + t_sid  + ' mode=u+12 Client=' + client + '  pf=' + t_path + '\\bin\TP_' + domain + '.PFL\"'
					write(loc.strip('\\') + '\\reflogfile.log',"win34:" + command)
					print command
					command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
					out, err = command.communicate()
					write(loc.strip('\\') + '\\reflogfile.log',out)
					status = get_result(out)
					print status
					if status == '0' or status == '4':
						write(loc.strip('\\') + '\\reflogfile.log','win34 : this command is used to do tp import')
						command = 'c:\python27\python ' + loc.strip('\\') + '\wmiexec.py ' + t_username.strip() + ':' + t_password.strip() + '@' + t_hostname + ' \"' + location.strip("\\") + '\\tp import ' + tr_id + " " +  t_sid + ' Client=' + client + '  pf=' + t_path + '\\bin\TP_' + domain + '.PFL U123689\"'
						write(loc.strip('\\') + '\\reflogfile.log',"win34:" + command)
						print command
						command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
						out, err = command.communicate()
						write(loc.strip('\\') + '\\reflogfile.log',out)
						status = get_result(out)
						print status
						if status == '0' or status == '4':
							print "POST:P:TR " + tr_id + " import is successfull in the target application server " + t_hostname
							write(loc.strip('\\') + ref_id,"POST:P:TR " + tr_id + " import is successfull in the target application server " + t_hostname)
						
						else:
							print "POST:F: TR " + tr_id + " import is failed with the error code: " + status
							write(loc.strip('\\') + ref_id,"POST:F: TR " + tr_id + " import is failed with the error code: " + status)
					else:
						print "POST:F: The modbuffer for the TR " + tr_id + " has failed"
						write(loc.strip('\\') + ref_id,"POST:F: The modbuffer for the TR " + tr_id + " has failed")
				else:
					print "POST:F: TR " + tr_id + " is failed with the error code: " + status
					write(loc.strip('\\') + ref_id, "POST:F: TR " + tr_id + " is failed with the error code: " + status)



except Exception as e:
			if str(e) == "[Errno -2] Name or service not known":
				print "POST:F:GERR_0201:Hostname unknown"
				write(loc.strip('\\') + ref_id,'POST:F:GERR_0201:Hostname unknown')
				write(loc.strip('\\') + '\\reflogfile.log',"POST:F:GERR_0201:Hostname unknown")
			elif str(e).strip() == "list index out of range":
				print "POST:F:GERR_0202:Argument/s missing for the script"
				write(loc.strip('\\') + '\\reflogfile.log',"POST:F:GERR_0202:Argument/s missing for the script")
			elif str(e) == "Authentication failed.":
				print "POST:F:GERR_0203:Authentication failed."
				write(loc.strip('\\') + ref_id,'POST:F:GERR_0203:Authentication failed.')
				write(loc.strip('\\') + '\\reflogfile.log',"POST:F:GERR_0203:Authentication failed.")
			elif str(e) == "[Errno 110] Connection timed out":
				print "POST:F:GERR_0204:Host Unreachable"
				write(loc.strip('\\') + ref_id,'POST:F:GERR_0204:Host Unreachable')
				write(loc.strip('\\') + '\\reflogfile.log',"POST:F:GERR_0204:Host Unreachable")
			elif "getaddrinfo failed" in str(e):
				print "POST:F:GERR_0205: Please check the hostname that you have provide"
				write(loc.strip('\\') + ref_id,'POST:F:GERR_0205: Please check the hostname that you have provide')
				write(loc.strip('\\') + '\\reflogfile.log',"POST:F:GERR_0205: Please check the hostname that you have provide")
			elif "[Errno None] Unable to connect to port 22" in str(e):
				print "POST:F:GERR_0206:Host Unreachable or Unable to connect to port 22"
				write(loc.strip('\\') + ref_id,'POST:F:GERR_0206:Host Unreachable or Unable to connect to port 22')
				write(loc.strip('\\') + '\\reflogfile.log',"POST:F:GERR_0206:Host Unreachable or Unable to connect to port 22")
			else:
				print "POST:F: " + str(e)
				write(loc.strip('\\') + ref_id,"POST:F: " + str(e))
				write(loc.strip('\\') + '\\reflogfile.log',"POST:F: " + str(e))
