#!/usr/bin/sh
from __future__ import division
#import paramiko
import re
import glob
import os
#from paramiko import *
from sys import *
from log4erp import *
import subprocess
import datetime


def space_check(hostname, username, password, bkp_path,db_sid, path, al11, logfile):
    write(path.strip('\\') + '\\reflogfile.log','win20 : This command is used to get the bkp_path details')
    command = 'c:\python27\python.exe ' + path + 'wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "dir ' + bkp_path + '/s /b /o:gn"'
    print command
    write(path.strip('\\') + '\\reflogfile.log',command)
    command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
    out, err = command.communicate()
    write(path.strip('\\') + '\\reflogfile.log',out)
    print out
    out=out.split('\n')
    length=out.__len__()
    files = ""
    for i in range(2,length-2):
        files = files + "DISK = '" + out[i].strip() + "', "
    files = files.strip().rstrip(',')

    # --------------------------------- Set Rollback ---------------------------------------
    write(path.strip('\\') + '\\reflogfile.log','win20 : This command is used to run SQL command for single user')
    command = 'c:\python27\python.exe ' + path + 'wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "sqlcmd -E -S ' + hostname + '\\' + db_sid + ' -d master -Q \\"ALTER DATABASE ' + db_name + ' SET Single_User WITH Rollback Immediate\\""'
    print command
    write(path.strip('\\') + '\\reflogfile.log',command)
    command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    output, err = command.communicate()
    write(path.strip('\\') + '\\reflogfile.log',output)
    print output
    print "hi"
    # ---------------------- Get path Mapping --------------------------------------------
    file_path = open (al11 + '\\' + logfile + '_restore.txt')
    file_p = file_path.readlines() # --------------- Data will get removed from file_path ------------
    length = len(file_p)
  
    # -------------------------------- Restore -------------------------------------------
    for line in range (0, length):
        mnt_pnt = file_p[line].split('|')[0].strip()
        rst_path = file_p[line].split('|')[1].strip()
        write(path.strip('\\') + '\\reflogfile.log','win20 :this command is used to execute SQL Query to restore database')
        command='c:\python27\python.exe ' + path + 'wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "sqlcmd -E -S ' + hostname + '\\' + db_sid + ' -d master -Q \\"restore database ' + db_name + ' from ' + files + ' WITH REPLACE,MOVE \'' + mnt_pnt + '\' to \'' + rst_path.strip() + '\'\\""'
        print command
        write(path.strip('\\') + '\\reflogfile.log',command)
        out=datetime.datetime.now().__str__().strip()
        write(path.strip('\\') + '\\reflogfile.log',out)
        print "DB:P:The restoration for the database of file " + mnt_pnt + " is starting " + out
        write(path + logfile,"DB:P:The restoration for the database of file " + mnt_pnt + " is starting " + out)
        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        output, err = command.communicate()
        print output
        write(path.strip('\\') + '\\reflogfile.log',output)
        status = command.returncode
        # --------------------------------- Check Status ---------------------------------
    	if 'RESTORE DATABASE successfully processed' in output:
            out=datetime.datetime.now().__str__().strip()
            print "DB:P:The restoration for the database of file " + mnt_pnt + " has completed successfully"
            write(path + logfile,"DB:P:The restoration for the database of file " + mnt_pnt + " has completed successfully " + out)
        else:
            out=datetime.datetime.now().__str__().strip()
            print "DB:F:The restoration for the database of file " + mnt_pnt + " has failed"
            write(path + logfile,"DB:F:The restoration for the database of file " + mnt_pnt + " has failed " + out)
            exit()
    write(path.strip('\\') + '\\reflogfile.log','this command is used to execute SQL qery for multi user')
    command = 'c:\python27\python.exe ' + path + 'wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "sqlcmd -E -S localhost\\' + db_sid + ' -Q \\"ALTER DATABASE ' + db_name + ' SET Multi_User\\""'
    command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    write(path.strip('\\') + '\\reflogfile.log',command)
    output, err = command.communicate()
    write(path.strip('\\') + '\\reflogfile.log',output)
try:
    hostname = argv[1]
    username = argv[2]
    password = argv[3]
    bkp_path = argv[4]
    db_sid =argv[5]
    path = argv[6].strip('\\') + '\\'
    al11 = argv[7]
    logfile = argv[8]
    db_name = argv[9]
    if argv[1] == "--u":
        print "usage: c:\python27\python.exe DB.py <Target Host> <Target Username> <Target Password> <backup file path> < DB sid>"
    else:
        source = space_check(argv[1], argv[2], argv[3], argv[4], argv[5], path, al11, logfile)

except Exception as e:
    if "No such file or directory" in str(e):
        print "No such file"
        write(path + logfile,"No such file")
        write(path + 'reflogfile.log',"No such file")
    elif "name 'user' is not defined" in str(e):
        print "DB:F: Please enter App for Application Server or Db for Database Server"
        write(path + logfile,"DB:F: Please enter App for Application Server or Db for Database Server")
        write(path + 'reflogfile.log',"DB:F: Please enter App for Application Server or Db for Database Server")
    elif str(e).strip() == "list index out of range":
        print "DB:F:GERR_0202:Argument/s missing for the script"
        write(path+logfile,"DB:F:Argument/s missing for the script")
        write(path + 'reflogfile.log',"DB:F:Argument/s missing for the script")
    else:
        print "DB:F" + str(e)
        write(path + logfile,"DB:F:" + str(e))
        write(path + 'reflogfile.log',"DB:F:" + str(e))

