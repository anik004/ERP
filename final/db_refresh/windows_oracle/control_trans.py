import os
from sys import *
import subprocess
import log4erp
from log4erp import *

try:
#	if argv[1] == "--u":
#		print "usage: python control_trans.py <Source POST host> <Source POST sudo user> <Source POST sudo user pass> <source POST sid> <Target POST host> <Target POST sudo user> <Target POST sudo user pass> <Target POST sid>"
#	else:
		
		s_host = argv[1]
		s_username = argv[2]
		s_pass = argv[3]
		s_dbsid = argv[4]
		t_host = argv[5]
		t_username = argv[6]
		t_pass = argv[7]
		t_dbsid = argv[8]
		logfile = argv[9] + ".log"
		s_path = argv[10]
		t_path = argv[11]
		port = 22
		password = s_pass
		username = s_username

		command = 'c:\python27\python ' + drive.strip('\\') + '\wmiexec.py ' + t_username.strip() + ':' + t_pass.strip() + '@' + t_host + ' "md ' + t_path + '\\test && net share sharename=' + t_path + '\\test /grant:everyone,full"'
  		print command
  		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
  		out, err = command.communicate()
		command = 'c:\python27\python ' + drive.strip('\\') +  '\wmiexec.py ' + s_username.strip() + ':' + s_pass.strip() + '@' + s_host.strip() + ' "copy ' + s_path + '\control_script_' + s_dbsid.upper() + '.sql' + ' \\\\' + t_host + '\\sharename"'
		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
		out, err = command.communicate()
		if command.returncode == 0:
			print "CTRLTRANS:P: The control file has been copied from the source " + argv[1] + " to the target " + argv[5] + " server"
			write(logfile,"POST:P:The control file has been copied from the source " + argv[1] + " to the target " + argv[5] + " server")
			command = 'c:\python27\python ' + drive.strip('\\') +  '\wmiexec.py ' + t_username.strip() + ':' + t_pass.strip() + '@' + t_host.strip() + ' "ren ' + t_path + '\test\control_script_' + s_dbsid.upper() + '.sql control_script_' + t_dbsid.upper() + '.sql"'
			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
			out, err = command.communicate()
		else:
			print "CTRLTRANS:F: The control file has not been copied from the source " + argv[1] + " to the target " + argv[5] + " server"
			write(logfile,"POST:F:The control file has not been copied from the source " + argv[1] + " to the target " + argv[5] + " server")
except Exception as e:
     if str(e) == "[Errno -2] Name or service not known":
                print "CTRLTRANS:F:GERR_1701:Hostname unknown"
                write(logfile,'POST:F: Hostname unknown [Error Code - 1701]')
     elif str(e) == "list index out of range":
                print "CTRLTRANS:F:GERR_1702:Argument/s missing for the script"
     elif str(e) == "Authentication failed.":
                print "CTRLTRANS:F:GERR_1703:Authentication failed."
                write(logfile,'POST:F:Authentication failed.[Error Code - 1703]')
     elif str(e) == "[Errno 110] Connection timed out":
                print "CTRLTRANS:F:GERR_1704:Host Unreachable"
                write(logfile,'POST:F:Host Unreachable.[Error Code - 1704]')
     elif "getaddrinfo failed" in str(e):
                print "CTRLTRANS:F:GERR_1705: Please check the hostname that you have provide"
                write(logfile,'POST:F: Please check the hostname that you have provide [Error Code - 1705]')
     elif "[Errno None] Unable to connect to port 22 on" in str(e):
                print "CTRLTRANS:F:GERR_1706:Host Unreachable or Unable to connect to port 22"
                write(logfile,'POST:F: Host Unreachable or Unable to connect to port 22 [Error Code - 1706]')
     else:
                print "CTRLTRANS:F: " + str(e)
