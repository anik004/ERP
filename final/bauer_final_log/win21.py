from __future__ import division
import paramiko
import re
import glob
import os
from paramiko import *
from sys import *
import subprocess
from log4erp import *


def backup(hostname, username, password, instance, database, bkp_path, path, logfile):
    command = 'c:\python27\python.exe ' + path + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "sqlcmd -E -S ' + hostname + '\\' + instance + ' -Q \\"BACKUP DATABASE ' + database + ' TO DISK = \'' + bkp_path + '\'\\""'
    print command
    write('reflogfile.log',command)
    command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    out, err = command.communicate()
    write('reflogfile.log',out)
    print out
    if command.returncode == 0:
        print 'BACKUP:P:backup of database ' + database + ' is successful'
        write(logfile,'BACKUP:P:backup of database ' + database + ' is successful')
    else:
         print 'BACKUP:P:backup of database ' + database + ' is failed'
         write(logfile,'BACKUP:P:backup of database ' + database + ' is failed')
try:
    source_hostname = argv[1]
    source_username = argv[2]
    source_password = argv[3]
    source_instance = argv[4].upper()
    source_database = argv[5].upper()
    source_bkp_path = argv[6]
    target_hostname = argv[7]
    target_username = argv[8]
    target_password = argv[9]
    target_location = argv[10]
    path = argv[11].strip('\\')
    seq = argv[12]
    logfile = argv[13]
    if argv[1] == "--u":
        print "usage: c:\python27\python.exe backup.py <Source Host> <Source Username> <Source Password> <Instance> <Database Name> <backup file path> <target hostname> <target username> <target password> <target location>"
    else:
	if seq == 1:
	        source = backup(argv[1], argv[2], argv[3], argv[4].upper(), argv[5].upper(), argv[6], path, logfile)

################################ SHARE FOLDER HAS ALREADY BEEN CREATED IN EXPORT ##############################################
#        command = 'c:\python27\python.exe ' + path + '\wmiexec.py ' + target_username.strip() + ':' + target_password.strip() + '@' + target_hostname.strip() + ' \"md ' + target_location + '\\test && net share sharename=' + target_location + '\\test /grant:everyone,full\"'
#        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
#        out, err = command.communicate()
###############################################################################################################################
	elif seq == 2:
		command = 'c:\python27\python.exe ' + path + '\wmiexec.py ' + target_username.strip() + ':' + target_password.strip() + '@' + target_hostname.strip() + ' \"copy ' + source_bkp_path + ' \\\\' + target_hostname + '\\sharename\"'
		write('reflogfile.log',command)
	        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        	out, err = command.communicate()
		write('reflogfile.log',out)
		status=command.returncode
		if status == 0:
		   print 'TRF:P:the transfer of source backup to target system is successful'
		   write(logfile,'TRF:P:the transfer of source backup to target system is successful')

		else:
		   print 'TRF:F:the transfer of source backup to target system is not successful'
		   write(logfile,'TRF:F:the transfer of source backup to target system is not successful')


except Exception as e:
    if "No such file or directory" in str(e):
        print "No such file"
        write(logfile,"No such file")
	write('reflogfile.log',"No such file")
    elif "name 'user' is not defined" in str(e):
        print "backup:F: Please enter App for Application Server or Db for Database Server"
        write(logfile,"backup:F: Please enter App for Application Server or Db for Database Server")
	write('reflogfile.log',"backup:F: Please enter App for Application Server or Db for Database Server")
    elif str(e).strip() == "list index out of range":
        print "backup:F:GERR_0202:Argument/s missing for the script"
        write(logfile,"backup:F:GERR_0202:Argument/s missing for the script")
	write('reflogfile.log',"backup:F:GERR_0202:Argument/s missing for the script")
    else:
        print "backup:F" + str(e)
        write(logfile,"backup:F" + str(e))
	write('reflogfile.log',"backup:F" + str(e))

