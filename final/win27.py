#!/usr/bin/sh
from __future__ import division
import re
import glob
import os
from sys import *
import subprocess
from log4erp import *

try:
	hostname = argv[1]
	username = argv[2]
	password = argv[3]
	db_sid =argv[4]
	db_name = argv[7]
	path = argv[5].strip('\\') + '\\'
	logfile = argv[6]

	write(path + 'reflogfile.log','win27: this command is used to execute SQL query to find the physical name')
	command = 'c:\python27\python.exe ' + path + 'wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "sqlcmd -E -S ' + hostname + '\\' + db_sid + ' -Q \\"use ' + db_name + ';SELECT physical_name FROM sys.database_files;\\""'
	print command
	write(path + 'reflogfile.log',command)
	command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
	output, err = command.communicate()
	write(path + 'reflogfile.log',output)
	out = output.split('\n')
	for line in out[5:][:-4]:
		#mnt_pnt = line.split()[0]
		print line.strip()
		#rst_path = line.split(' ', 1)[1].strip()
		#print rst_path

except Exception as e:
		if "No such file or directory" in str(e):
			print "No such file"
			write(path + 'reflogfile.log','No such file')
			write(path + logfile,'"No such file"')
		elif "name 'user' is not defined" in str(e):
			print "DB_RESTORE:F: Please enter App for Application Server or Db for Database Server"
			write(path + 'reflogfile.log','DB_RESTORE:F: Please enter App for Application Server or Db for Database Server')
			write(path + logfile, "DB_RESTORE:F: Please enter App for Application Server or Db for Database Server")
		elif str(e).strip() == "list index out of range":
			print "datafile:F:GERR_0202:Argument/s missing for the script"
			write(path + 'reflogfile.log','datafile:F:GERR_0202:Argument/s missing for the script')
			write(path + logfile, '"datafile:F:GERR_0202:Argument/s missing for the script"')
