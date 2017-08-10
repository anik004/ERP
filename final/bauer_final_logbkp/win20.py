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
import datetime


def space_check(hostname, username, password, bkp_path,db_sid, path, al11, logfile):
    # --------------------------------- Set Rollback ---------------------------------------
    command = 'c:\python27\python.exe ' + path + 'wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "sqlcmd -E -S ' + hostname + '\\' + db_sid + ' -Q \\"ALTER DATABASE ' + db_sid + ' SET Single_User WITH Rollback Immediate\\""'
    print command
    write('reflogfile.log',command)
    command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    output, err = command.communicate()
    write('reflogfile.log',output)
    print output
    # ---------------------- Get path Mapping --------------------------------------------
    file_path = open (al11 + '\\' + logfile + '_restore.txt')
    file_p = file_path.readlines() # --------------- Data will get removed from file_path ------------
    length = len(file_p)
  
    # -------------------------------- Restore -------------------------------------------
    for line in range (0, length):
        mnt_pnt = file_p[line].split('|')[0].strip()
        rst_path = file_p[line].split('|')[1].strip()
        command='c:\python27\python.exe ' + path + 'wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "sqlcmd -E -S ' + hostname + '\\' + db_sid + ' -Q \\"use master; restore database ' + db_sid + ' from disk = \'' + bkp_path + '\' WITH REPLACE,MOVE \'' + mnt_pnt + '\' to \'' + rst_path.strip() + '\'\\""'
	print command
	write('reflogfile.log',command)
	out=datetime.datetime.now().__str__().strip()
	write('reflogfile.log',out)
	print "DB:P:The restoration for the database of file " + mnt_pnt + " is starting " + out
        write(logfile,"DB:P:The restoration for the database of file " + mnt_pnt + " is starting " + out)
        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
	write('reflogfile.log',command)
        output, err = command.communicate()
        print output
	write('reflogfile.log',output)
    	status = command.returncode
        # --------------------------------- Check Status ---------------------------------
    	if status == 0:
	    out=datetime.datetime.now().__str__().strip()
	    write('reflogfile.log',out)
    	    print "DB:P:The restoration for the database of file " + mnt_pnt + " has completed successfully " + out
	    write(logfile,"DB:P:The restoration for the database of file " + mnt_pnt + " has completed successfully " + out)
    	else:
	    out=datetime.datetime.now().__str__().strip()
	    write('reflogfile.log',out)
    	    print "DB:F:The restoration for the database of file " + mnt_pnt + " has failed " + out
	    write(logfile,"DB:F:The restoration for the database of file " + mnt_pnt + " has failed " + out)
    command = 'c:\python27\python.exe ' + path + 'wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "sqlcmd -E -S localhost\\' + db_sid + ' -Q \\"ALTER DATABASE ' + db_sid + ' SET Multi_User\\""'
    write('reflogfile.log',command)
    command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    output, err = command.communicate()
    write('reflogfile.log',output)
try:
    hostname = argv[1]
    username = argv[2]
    password = argv[3]
    bkp_path = argv[4]
    db_sid =argv[5]
    path = argv[6].strip('\\') + '\\'
    al11 = argv[7]
    logfile = argv[8]
    if argv[1] == "--u":
        print "usage: c:\python27\python.exe DB.py <Target Host> <Target Username> <Target Password> <backup file path> < DB sid>"
    else:
        source = space_check(argv[1], argv[2], argv[3], argv[4], argv[5], path, al11, logfile)

except Exception as e:
	if "No such file or directory" in str(e):
		print "No such file"
		write(logfile,"No such file")
		write('reflogfile.log',"No such file")
	elif "name 'user' is not defined" in str(e):
		print "DB:F: Please enter App for Application Server or Db for Database Server"
	        write(logfile,"DB:F: Please enter App for Application Server or Db for Database Server")
		write('reflogfile.log',"DB:F: Please enter App for Application Server or Db for Database Server")
	elif str(e).strip() == "list index out of range":
                print "DB:F:GERR_0202:Argument/s missing for the script"
	        write(logfile,"DB:F:Argument/s missing for the script")
		write('reflogfile.log',"DB:F:Argument/s missing for the script")
	else:
		print "DB:F" + str(e)
		write(logfile,"DB:F:" + str(e))
		write('reflogfile.log',"DB:F:" + str(e))

