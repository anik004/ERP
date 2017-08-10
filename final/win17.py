#!/usr/bin/sh
from __future__ import division
#import paramiko
import re
import glob
import os
#from paramiko import *
from sys import *
import subprocess
import log4erp
from log4erp import *
def space_check(hostname, username, password, profilepath, location, logfile):
    write(location.strip('\\') + '\\reflogfile.log','win15: Tis command is used to check the existence of profilepath')
    command = 'c:\\python27\\python.exe ' + location.strip('\\') + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "powershell.exe;test-path ' + profilepath + '"'
    print command
    write(location.strip('\\') + '\\reflogfile.log', command)
    command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    out, err = command.communicate()
    print out
    write(location.strip('\\') + '\\reflogfile', out)
    if "False" in str(out):
        print "POST:F:The profile Path does not exists"
        write(logfile, "POST:F:The profile Path does not exists")
    else:
        write(location.strip('\\') + '\\reflogfile.log','win15.py : This command is used find instances')
        command = 'c:\\python27\\python ' + location.strip('\\') + '\\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "dir ' + profilepath + ' /s /b | findstr DVEBMGS* | findstr -V # | findstr -V START"'
        write(location.strip('\\') + '\\reflogfile.log',command)
        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        out, err = command.communicate()
        write(location.strip('\\') + '\\reflogfile.log',out)
        profilepath = out.split('\n')[3].strip()
        profile = profilepath.split('\\')[-1]
        print profilepath
        write(location.strip('\\') + '\\reflogfile.log','win15.py : This command is used to find  rdisp / wp_no_btc parameter')
        command='c:\python27\python ' + location.strip('\\') + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "powershell.exe;\"\\"get-content ' + profilepath + ' | findstr login/no_automatic_user_sapstar\\"\" | findstr -V #"'
        print command
        write(location.strip('\\') + '\\reflogfile.log',command)
        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        out, err = command.communicate()
        #print out
        write(location.strip('\\') + '\\reflogfile.log',out)
        out=out.split('\n')
        #print out
        out=''.join(out)
        #print out
        if 'login/no_automatic_user_sapstar' not in out:
            write(location.strip('\\') + '\\reflogfile.log','win15.py: This command is used to set the value of rdisp / wp_no_btc')
            command='c:\python27\python ' + location.strip('\\') + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "powershell.exe;\"\\"add-content ' + profilepath + ' \'login/no_automatic_user_sapstar = 1 \'\\"\"'
            print command
            write(location.strip('\\') + '\\reflogfile.log',command)
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            write(location.strip('\\') + '\\reflogfile.log',out)
            #print out
            if command.returncode == 0:
                print 'POST:P:parameter set to default value'
                write(location.strip('\\') + '\\' + logfile,'POST:P:parameter set to default value')

            else:
                print 'POST:F:parameter not set to default value'
                write(location.strip('\\') + '\\' + logfile,'POST:F:parameter not set to default value')
        else:
            parameter = out.split('used',1)
            #print parameter
            parameter = parameter[1].strip()
            print parameter
            write(location.strip('\\') + '\\reflogfile.log','win15.py: This command is used to cpoy profile path')
            command = 'c:\\python27\\python ' + location.strip('\\') + '\\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' copy ' + profilepath + ' \\\\' + hostname + '\\sharename /y'
            print command
            write(location.strip('\\') + '\\reflogfile.log',command)
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            print out
            write(location.strip('\\') + '\\reflogfile.log',out)
            write(location.strip('\\') + '\\reflogfile.log','win15.py :This command is used to copy from share folder')
            command = 'copy \\\\' + hostname + '\\sharename\\' + profile + ' ' + location.strip('\\') + ' /y'
            print command
            write(location.strip('\\') + '\\reflogfile.log',command)
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            write(location.strip('\\') + '\\reflogfile.log',out)
            print out
            write(location.strip('\\') + '\\reflogfile.log','win15.py : This command is used to replace ')
            command = 'powershell.exe;"(Get-Content ' + location.strip('\\') + '\\' + profile + ') -Replace \'' + parameter + '\',\'login/no_automatic_user_sapstar = 1 \' | set-content ' + location.strip('\\') + '\\' + profile + '"'
            print command
            write(location.strip('\\') + '\\reflogfile.log',command)
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            write(location.strip('\\') + '\\reflogfile.log',out)
            write(location.strip('\\') + '\\reflogfile.log','win15.py : this command is used to copy to share folder')
            command = 'copy ' + location.strip('\\') + '\\' + profile + ' \\\\' + hostname + '\\sharename /y'
            print command

            write(location.strip('\\') + '\\reflogfile.log',command)
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            write(location.strip('\\') + '\\reflogfile.log',out)
            print out
            write(location.strip('\\') + '\\reflogfile.log','win13.py : This command is used to copy files')
            command = 'c:\\python27\\python ' + location.strip('\\') + '\\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' copy \\\\' + hostname + '\\sharename\\' + profile + ' ' + profilepath + ' /y'
            print command
            write(location.strip('\\') + '\\reflogfile.log',command)
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            write(location.strip('\\') + '\\reflogfile.log',out)
            print out
            #command='c:\python27\python ' + locationation.strip('\\') + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "powershell.exe;\"\\"(Get-Content ' + profilepath +').Replace(\'' + parameter + '\',\'login/no_automatic_user_sapstar = ' + value + '\') | set-content ' + profilepath + '"\\"\"'
            #print command
            #command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            #out, err = command.communicate()
            #print out
            if "1" in out:
                print 'POST:P:parameter set to default value'
                write(location.strip('\\') + '\\' +logfile,'POST:P:parameter set to default value')
            else:
                print 'POST:F:parameter not set to default value'
                write(location.strip('\\') + '\\' + logfile,'POST:F:parameter not set to default value')
try:
    if argv[1] == "--u":
        print "usage: c:\python27\python  POST.py <Target Host> <Target Sudo Username> <Target Sudo Password> <profilepath> <value> <log>"
    else:
		hostname = argv[1]
		username = argv[2]
		password = argv[3]
		profilepath = argv[4]
		logfile = argv[6]
		#value = argv[]
		location = argv[5]
		#fo = open(location + "\\profilevalue.txt", "r")
		#value = fo.read()
		#fo.close()
		space_check(argv[1], argv[2], argv[3], argv[4],argv[5],argv[6])

except Exception as e:
    if "No such file or directory" in str(e):
        print "No such file"
        write(location.strip('\\') + '\\' +logfile,'POST:F:No such file')
        write(location.strip('\\') + '\\reflogfile.log','No such file')
    elif "name 'user' is not defined" in str(e):
        print "POST:F: Please enter App for Application Server or Db for Database Server"
        write(location.strip('\\') + '\\' + logfile,'POST:F:Please enter App for Application Server or Db for Database Server')
        write(location.strip('\\') + '\\reflogfile.log','POST:F:Please enter App for Application Server or Db for Database Server')
    elif str(e).strip() == "list index out of range":
        print "POST:F:GERR_1212:Argument/s missing for the script"
    else:
        print "POST :" + str(e)
        write(location.strip('\\') + '\\' +logfile,'POST:F: ' + str(e))
        write(location.strip('\\') + '\\reflogfile.log','POST:F: ' + str(e))

