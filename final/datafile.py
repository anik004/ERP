#!/usr/bin/sh
from __future__ import division
import paramiko
import re
import glob
import os
from paramiko import *
from sys import *
from log4erp import *
import subprocess

try:
	hostname = argv[1]
	username = argv[2]
	password = argv[3]
	db_sid =argv[4]
	path = argv[5].strip('\\') + '\\'
	logfile = argv[6]
	print "hi"

	command = 'c:\python27\python.exe ' + path + 'wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "sqlcmd -E -S localhost\\' + db_sid + ' -Q \\"use DRL;SELECT name, physical_name FROM sys.database_files;\\""'
	print command
	command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        output, err = command.communicate()
	print output

except Exception as e:
        if "No such file or directory" in str(e):
                print "No such file"
                write(logfile,"No such file")
        elif "name 'user' is not defined" in str(e):
                print "DB_RESTORE:F: Please enter App for Application Server or Db for Database Server"
                write(logfile,"DB_RESTORE:F: Please enter App for Application Server or Db for Database Server")
        elif str(e).strip() == "list index out of range":
                print "datafile:F:GERR_0202:Argument/s missing for the script"
        else:
                print "db_restore:F" + str(e)
                write(logfile,"db_restore:F" + str(e))

	

