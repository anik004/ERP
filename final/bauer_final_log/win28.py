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
		location = argv[5].strip('\\')
		logfile = argv[6]
		stepname = argv[7]
		# ------------------------ get hostname ----------------------------
		command = 'c:\\python27\\python.exe ' + location.strip('\\') + '\\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname.strip() + ' "hostname"'
		write('reflogfile.log',command)
                command=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
                out, err = command.communicate()
		write('reflogfile.log',out)
                #print out
		domain_name = out.split('\n')[3]
		#print domain_name
		# ----------------------- get table names ---------------------------
		command='c:\python27\python '+ location.strip('\\')+'\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' \"sqlcmd -E -S ' + domain_name.strip() + '\\' + sid.upper() + ' -Q \\"use ' + sid.upper() + '; select  TOP 1 TABLE_SCHEMA from INFORMATION_SCHEMA.TABLES\\""'
		#print command
		write('reflogfile.log',command)
		command=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		out, err = command.communicate()
		write('reflogfile.log',out)
		#print out
		schema = out.split('\n')[5].strip()
		#print schema
                if schema:
                        command='c:\python27\python '+ location.strip('\\')+'\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' \"sqlcmd -E -S ' + domain_name.strip() + '\\' + sid.upper() + ' -Q \\"use ' + sid.upper() + '; select CUAMON from ' + schema + '.USBAPILINK\\""'
			write('reflogfile.log',command)
                        command=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
                        out, err = command.communicate()
			write('reflogfile.log',out)
                        cua = out.split('\n')[5].strip()
                        if cua == '':
                                print stepname + ':P:CUA is inactive'
                        else:
                                print stepname + ':F:CUA is active'
# ---------------------------- Exceptions ------------------------------------
except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "PRE:F:GERR_0201:Hostname unknown"
 #       write(logfile,'PRE:F:GERR_0201:Hostname unknown')
	write('reflogfile.log','PRE:F:GERR_0201:Hostname unknown')
    elif str(e).strip() == "list index out of range":
        print "PRE:F:GERR_0202:Argument/s missing for the script"
	write('reflogfile.log','PRE:F:GERR_0202:Argument/s missing for the script')
    elif str(e) == "Authentication failed.":
        print "PRE:F:GERR_0203:Authentication failed."
#        write(logfile,'PRE:F:GERR_0203:Authentication failed.')
	write('reflogfile.log','PRE:F:GERR_0203:Authentication failed.')
    elif str(e) == "[Errno 110] Connection timed out":
        print "PRE:F:GERR_0204:Host Unreachable"
 #       write(logfile,'PRE:F:GERR_0204:Host Unreachable')
	write('reflogfile.log','PRE:F:GERR_0204:Host Unreachable')
    elif "getaddrinfo failed" in str(e):
        print "PRE:F:GERR_0205: Please check the hostname that you have provide"
  #      write(logfile,'PRE:F:GERR_0205: Please check the hostname that you have provide')
	write('reflogfile.log','PRE:F:GERR_0205: Please check the hostname that you have provide')
    elif "[Errno None] Unable to connect to port 22" in str(e):
        print "PRE:F:GERR_0206:Host Unreachable or Unable to connect to port 22"
   #     write(logfile,'PRE:F:GERR_0206:Host Unreachable or Unable to connect to port 22')
	write('reflogfile.log','PRE:F:GERR_0206:Host Unreachable or Unable to connect to port 22')
    else:
        print "PRE:F: " + str(e)
	write('reflogfile.log','PRE:F: ' + str(e))
