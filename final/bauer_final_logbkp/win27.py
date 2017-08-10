#!/usr/bin/sh
from __future__ import division
import paramiko
import re
import glob
import os
from paramiko import *
from sys import *
import subprocess
from log4erp import *

try:
	hostname = argv[1]
	username = argv[2]
	password = argv[3]
	db_sid =argv[4]
	path = argv[5].strip('\\') + '\\'

	command = 'c:\python27\python.exe ' + path + 'wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "sqlcmd -E -S ' + hostname + '\\' + db_sid + ' -Q \\"use ' + db_sid + ';SELECT physical_name FROM sys.database_files;\\""'
	write('reflogfile.log',command)
	command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
	output, err = command.communicate()
	write('reflogfile.log',output)
	out = output.split('\n')
	for line in out[6:][:-4]:
		mnt_pnt = line.split()[0]
		print mnt_pnt
		rst_path = line.split(' ', 1)[1].strip()
		print rst_path

except Exception as e:
		if "No such file or directory" in str(e):
			print "No such file"
			write('reflogfile.log','No such file')
		elif "name 'user' is not defined" in str(e):
			print "DB_RESTORE:F: Please enter App for Application Server or Db for Database Server"
			write('reflogfile.log','DB_RESTORE:F: Please enter App for Application Server or Db for Database Server')
		elif str(e).strip() == "list index out of range":
			print "datafile:F:GERR_0202:Argument/s missing for the script"
			write('reflogfile.log','datafile:F:GERR_0202:Argument/s missing for the script')
