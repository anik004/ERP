from sys import argv
import subprocess
import os
from log4erp import *

try:
	if argv[1] == '--ani':
		print "usage"
	else:
		#----------------------- variable declaration --------------------
		hostname = argv[1]
		username = argv[2]
		password = argv[3]
		sid = argv[4]
		db_n =argv[8]
		location = argv[5].strip('\\')
		logfile = argv[6]
		stepname = argv[7]
		# ------------------------ get hostname ----------------------------
		write(location + '\\reflogfile.log','win28: this command is used to get the hostname')
		command = 'c:\\python27\\python.exe ' + location.strip('\\') + '\\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname.strip() + ' "hostname"'
		print command
		write(location + '\\reflogfile.log',command)
		command=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		out, err = command.communicate()
		print out
		write(location + '\\reflogfile.log',out)
		#print out
		domain_name = out.split('\n')[2]
		print "hi"
		print domain_name
		# ----------------------- get table names ---------------------------
		write(location + '\\reflogfile.log','win28: This command is used to get the table names')
		command='c:\python27\python '+ location.strip('\\')+'\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' \"sqlcmd -E -S ' + domain_name.strip() + '\\' + sid.upper() + ' -Q \\"use ' + db_n.upper() + '; select  TOP 1 TABLE_SCHEMA from INFORMATION_SCHEMA.TABLES\\""'
		print command
		write(location + '\\reflogfile.log',command)
		command=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		out, err = command.communicate()
		write(location + '\\reflogfile.log',out)
		print out
		schema = out.split('\n')[5].strip()
		print schema
        if schema:
			write(location + '\\reflogfile.log','win28 : This command is used to select CUAMON')
			command='c:\python27\python '+ location.strip('\\')+'\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' \"sqlcmd -E -S ' + domain_name.strip() + '\\' + sid.upper() + ' -Q \\"use ' + sid.upper() + '; select CUAMON from ' + schema + '.USBAPILINK\\""'
			write(location + '\\reflogfile.log',command)
			command=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
			out, err = command.communicate()
			write(location + '\\reflogfile.log',out)
			cua = out.split('\n')[5].strip()
			if cua == '':
				print stepname + ':P:CUA is inactive'
				write(location + '\\' + logfile,':P:CUA is inactive')
			else:
				print stepname + ':F:CUA is active'
				write(location + '\\' + logfile,':F:CUA is active')
# ---------------------------- Exceptions ------------------------------------
except Exception as e:
	if str(e) == "[Errno -2] Name or service not known":
		print "PRE:F:GERR_0201:Hostname unknown"
		write(location + '\\' + logfile,'PRE:F:GERR_0201:Hostname unknown')
		write(location + '\\reflogfile.log','PRE:F:GERR_0201:Hostname unknown')
	elif str(e).strip() == "list index out of range":
		print "PRE:F:GERR_0202:Argument/s missing for the script"
		write(location + '\\reflogfile.log','PRE:F:GERR_0202:Argument/s missing for the script')
	elif str(e) == "Authentication failed.":
		print "PRE:F:GERR_0203:Authentication failed."
		write(location + '\\' + logfile,'PRE:F:GERR_0203:Authentication failed.')
		write(location + '\\reflogfile.log','PRE:F:GERR_0203:Authentication failed.')
	elif str(e) == "[Errno 110] Connection timed out":
		print "PRE:F:GERR_0204:Host Unreachable"
		write(location + '\\' + logfile,'PRE:F:GERR_0204:Host Unreachable')
		write(location + '\\reflogfile.log','PRE:F:GERR_0204:Host Unreachable')
	elif "getaddrinfo failed" in str(e):
		print "PRE:F:GERR_0205: Please check the hostname that you have provide"
		write(location + '\\' + logfile,'PRE:F:GERR_0205: Please check the hostname that you have provide')
		write(location + '\\reflogfile.log','PRE:F:GERR_0205: Please check the hostname that you have provide')
	elif "[Errno None] Unable to connect to port 22" in str(e):
		print "PRE:F:GERR_0206:Host Unreachable or Unable to connect to port 22"
		write(location + '\\' + logfile,'PRE:F:GERR_0206:Host Unreachable or Unable to connect to port 22')
		write(location + '\\reflogfile.log','PRE:F:GERR_0206:Host Unreachable or Unable to connect to port 22')
	else:
		print "PRE:F: " + str(e)
		write(location + '\\reflogfile.log','PRE:F: ' + str(e))
		write(location + '\\' + logfile,"PRE:F: " + str(e))

