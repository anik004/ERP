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
def space_check(hostname, username, password, profilepath,logfile, location):
    write(location.strip('\\') + '\\reflogfile.log', 'win16 : This command is used to check the existence of profilepath')
    command = 'c:\\python27\\python.exe ' + location.strip('\\') + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "powershell.exe;test-path ' + profilepath + '"'
    print command
    write(location.strip('\\') + '\\reflogfile.log', command)
    command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    out, err = command.communicate()
    print out
    write(location.strip('\\') + '\\reflogfile.log', out)

    if "False" in str(out):
        print "POST:F:The profile Path does not exists"
        write('\\' + logfile, "POST:F:The profile Path does not exists")
    else:
        write(location.strip('\\') + '\\reflogfile.log','win16.py: This command does dir ')
        command = 'c:\\python27\\python ' + location.strip('\\') + '\\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "dir ' + profilepath + ' /s /b | findstr DVEBMGS* | findstr -V START"'
        print command
        write(location.strip('\\') + '\\reflogfile.log',command)
        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        out, err = command.communicate()
        print out
        write(location.strip('\\') + '\\reflogfile.log',out)
        profilepath = out.split('\n')[3].strip()
        profile = profilepath.split('\\')[-1]
        print profilepath
        #fo = open(location + "profilevalue.txt", "w+")
        #fo.write("3")
        #fo.close()
        write(location.strip('\\') + '\\reflogfile.log','win16.py : This command is used to get the content and find the value of login/no_automatic_user_sapstar')
        command='c:\\python27\\python ' + location.strip('\\') + '\\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "powershell.exe;\"\\"get-content ' + profilepath.strip() + ' | findstr login/no_automatic_user_sapstar\\"\" | findstr -V #"'
        print command
        write(location.strip('\\') + '\\reflogfile.log',command)
        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        out, err = command.communicate()
        write(location.strip('\\') + '\\reflogfile.log',out)
        #print out
        out=out.split('\n')
        #print out
        out=''.join(out)
        #print out
        if 'login/no_automatic_user_sapstar' not in out:
            write(location.strip('\\') + '\\reflogfile.log', 'win15: Tis command is used to check the existence of profilepath')
            command = 'c:\\python27\\python.exe ' + location.strip('\\') + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "powershell.exe;test-path ' + profilepath + '"'
            print command
            write(location.strip('\\') + '\\reflogfile.log', command)
            command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            out, err = command.communicate()
            print out
            write(location.strip('\\') + '\\reflogfile.log', out)
            write(location.strip('\\') + '\\reflogfile.log',"win16.py : This command is used to set the value of login/no_automatic_user_sapstar = 0")
            command='c:\\python27\\python ' + location.strip('\\') + '\\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "powershell.exe;\"\\"add-content ' + profilepath + ' \'login/no_automatic_user_sapstar = 0\'\\"\"'
            write(location.strip('\\') + '\\reflogfile.log',command)
            #command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "brconnect -u system/' + sys_pass + ' -c -f chpass -o SYSTEM -p ' + new_sys_pass + '"'
            print command
            write(location.strip('\\') + '\\reflogfile.log',command)
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            write(location.strip('\\') + '\\reflogfile.log',out)
            #print out
            if command.returncode == 0:
                print 'PRE:P:parameter set to zero'
                write(location.strip('\\') + '\\' + logfile,'PRE:P:parameter set to zero')
            else:
                print 'PRE:F:parameter not set to zero'
                write(location.strip('\\') + '\\' + logfile,'PRE:F:parameter not set to zero')
        else:
            parameter = out.split('used',1)
            #print parameter
            parameter = parameter[1].strip()
            value = parameter.split('=')[1].strip()
            print value
            #fo = open(location + "\\profilevalue.txt", "w+")
            #fo.write(value)
            #fo.close()
            write(location.strip('\\') + '\\reflogfile.log','win16.py: This command is used to copy files ')
            command = 'c:\\python27\\python ' + location.strip('\\') + '\\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' copy ' + profilepath + ' \\\\' + hostname + '\\sharename /y'
            print command
            write(location.strip('\\') + '\\reflogfile.log',command)
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            print out
            write(location.strip('\\') + '\\reflogfile.log',out)
            write(location.strip('\\') + '\\reflogfile.log','win16.py : This command is used to copy files from share folder')
            command = 'copy \\\\' + hostname + '\\sharename\\' + profile + ' ' + location.strip('\\') + ' /y'
            print command
            write(location.strip('\\') + '\\reflogfile.log',command)
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            write(location.strip('\\') + '\\reflogfile.log',out)
            print out
            write(location.strip('\\') + '\\reflogfile.log','win16.py : This command is used to replace the value to 0')
            command = 'powershell.exe;"(Get-Content ' + location.strip('\\') + '\\' + profile + ') -Replace \'' + parameter + '\',\'login/no_automatic_user_sapstar = 0\' | set-content ' + location.strip('\\') + '\\' + profile + '"'
            print command
            write(location.strip('\\') + '\\reflogfile.log',command)
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            write(location.strip('\\') + '\\reflogfile.log',out)
            write(location.strip('\\') + '\\reflogfile.log','win16.py: This command is used to copy files to share folder')
            command = 'copy ' + location.strip('\\') + '\\' + profile + ' \\\\' + hostname + '\\sharename /y'
            print command
            write(location.strip('\\') + '\\reflogfile.log',command)
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            write(location.strip('\\') + '\\reflogfile.log',out)
            print out
            write(location.strip('\\') + '\\reflogfile.log','win16.py: This command is used to copy files from share folder')
            command = 'c:\\python27\\python ' + location.strip('\\') + '\\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' copy \\\\' + hostname + '\\sharename\\' + profile + ' ' + profilepath + ' /y'
            print command
            write(location.strip('\\') + '\\reflogfile.log',command)
            command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            out, err = command.communicate()
            write(location.strip('\\') + '\\reflogfile.log',out)
            print out
            #command='c:\\python27\\python ' + location.strip('\\') + '\\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "powershell.exe;\"\\"(Get-Content ' + profilepath +').Replace(\'' + parameter + '\',\'login/no_automatic_user_sapstar = 0\') | set-content ' + profilepath + '"\\"\"'
            #print command
            #command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
            #out, err = command.communicate()
            #print out
            if "1" in out:
                print 'PRE:P:parameter set to zero'
                write(location.strip('\\') + '\\' + logfile,'PRE:P:parameter set to zero')
            else:
                print 'PRE:F:parameter not set to zero'
                write(location.strip('\\') + '\\' + logfile,'PRE:F:parameter not set to zero')
try:
    if argv[1] == "--u":
        print "usage: c:\\python27\\python ' + location.strip('\\') + '\PRE.py <Target Host> <Target Sudo Username> <Target Sudo Password> <profilepath> <log>"
    else:
        hostname = argv[1]
        username = argv[2]
        password = argv[3]
        profilepath = argv[4]
        logfile = argv[5]
        location = argv[6]
        space_check(argv[1], argv[2], argv[3], argv[4], argv[5], argv[6])
		
except Exception as e:
    if "No such file or directory" in str(e):
        print "No such file"
        write(location.strip('\\') + '\\' + logfile,'F:No such file')
        write(location.strip('\\') + '\\reflogfile.log','F:No such file')
    elif "name 'user' is not defined" in str(e):
        print "PRE:F: Please enter App for Application Server or Db for Database Server"
        write(location.strip('\\') + '\\' + logfile,'PRE:F:Please enter App for Application Server or Db for Database Server')
        write(location.strip('\\') + '\\reflogfile.log','PRE:F:Please enter App for Application Server or Db for Database Server')
    elif str(e).strip() == "list index out of range":
        print "PRE:F:GERR_1212:Argument/s missing for the script"
        write(location.strip('\\') + '\\' + logfile,"PRE:F:GERR_1212:Argument/s missing for the script")
        write(location.strip('\\') + '\\reflogfile.log',"PRE:F:GERR_1212:Argument/s missing for the script")
    else:
        print "PRE :" + str(e)
        write(location.strip('\\') + '\\' + logfile,'PRE:F: ' + str(e))
        write(location.strip('\\') + '\\reflogfile.log','PRE:F: ' + str(e))
