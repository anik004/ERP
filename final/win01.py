#!/usr/bin/sh
from __future__ import division
import re
import glob
import os
from log4erp import *
from sys import *
import subprocess

def space_check(hostname, username, password, sid, location):
   # print location
    write(location.strip('\\') + '\\reflogfile.log',"win01:This command is used to get the hostname of the target")
    command = 'c:\python27\python ' + location.strip('\\') + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' \"hostname\"'
    #print command
    write(location.strip('\\') + '\\reflogfile.log',command)
    command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
    out, err = command.communicate()
    #print out
    #print out.split('\n')
    write(location.strip('\\') + '\\reflogfile.log',out)
    domain_name = out.split('\n')[2:][0]

    #command='c:\python27\python wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' \'sqlcmd -E -S ' + domain_name + '\\' + sid + ' -Q "use ' + sid + ';SELECT name (size*8)/1024 SizeMB FROM sys.database_files;"\''
    write(location.strip('\\') + '\\reflogfile.log','win01:This command is used to get the size of the datafiles')
    command='c:\python27\python '+ location.strip('\\')+'\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' \"sqlcmd -E -S ' + domain_name.strip() + '\\sql -Q \\"use ' + sid + ';SELECT name, (size*8)/1024 SizeMB FROM sys.database_files;"\\"'
    #print command
    write(location.strip('\\') + '\\reflogfile.log',command)
    command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
    out, err = command.communicate()
    #print out
    write(location.strip('\\') + '\\reflogfile.log',out)
    out=out.split('\n')

    total = []
   # print  out
    #print out[5]
    #print out[:-4]
    for line in out[5:][:-4]:
     #   print line
        total += [str(line.split()[0])]
        total += [str(line.split()[1])]
    #    print total
    return total
 #   print total

try:
    location = argv[5]

    source = space_check(argv[1], argv[2], argv[3], argv[4], argv[5])
  #  print "1st done"
  #  print source

    target = space_check(argv[6], argv[7], argv[8], argv[9], argv[10])
   # print "target"
    for i in range (0, len(source), 2):
        if source[i] in target:
            if int(source[i+1]) > int(target[i+1]):
                print 'PRE:F:In target the mountpoint ' + source[i] + ' does not have enough space'
                exit()
            else:
                print 'PRE:P:In target the mountpoint ' + source[i] + ' has enough space'
        else:
            print 'PRE:F:In target the mountpoint ' + source[i] + ' does not exist'
            exit()

except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "PRE:F:GERR_0201:Hostname unknown"
 #       write(logfile,'PRE:F:GERR_0201:Hostname unknown')
        write(location.strip('\\') + '\\reflogfile.log','PRE:F:GERR_0201:Hostname unknown')
    elif str(e).strip() == "list index out of range":
        print "PRE:F:GERR_0202:Argument/s missing for the script"
        write(location.strip('\\') + '\\reflogfile.log','PRE:F:GERR_0202:Argument/s missing for the script')
    elif str(e) == "Authentication failed.":
        print "PRE:F:GERR_0203:Authentication failed."
#        write(logfile,'PRE:F:GERR_0203:Authentication failed.')
        write(location.strip('\\') + '\\reflogfile.log','PRE:F:GERR_0203:Authentication failed.')
    elif str(e) == "[Errno 110] Connection timed out":
        print "PRE:F:GERR_0204:Host Unreachable"
 #       write(logfile,'PRE:F:GERR_0204:Host Unreachable')
        write(location.strip('\\') + '\\reflogfile.log','PRE:F:GERR_0204:Host Unreachable')
    elif "getaddrinfo failed" in str(e):
        print "PRE:F:GERR_0205: Please check the hostname that you have provide"
  #      write(logfile,'PRE:F:GERR_0205: Please check the hostname that you have provide')
        write(location.strip('\\') + '\\reflogfile.log','PRE:F:GERR_0205: Please check the hostname that you have provide')
    elif "[Errno None] Unable to connect to port 22" in str(e):
        print "PRE:F:GERR_0206:Host Unreachable or Unable to connect to port 22"
   #     write(logfile,'PRE:F:GERR_0206:Host Unreachable or Unable to connect to port 22')
        write(location.strip('\\') + '\\reflogfile.log','PRE:F:GERR_0206:Host Unreachable or Unable to connect to port 22')
    else:
        print "PRE:F: " + str(e)
        write(location.strip('\\') + '\\reflogfile.log',"PRE:F: " + str(e))
