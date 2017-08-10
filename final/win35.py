#!/usr/bin/sh
from __future__ import division
import re
import glob
import os
from sys import *
import subprocess
import log4erp
from log4erp import *
def space_check(hostname, username, password, profilepath, location, logfile):
	print location
	write(location.strip('\\') + '\\reflogfile.log', 'win35 : This command is used to check the existence of profilepath')
	print "hi"
	command = 'c:\\python27\\python.exe ' + location.strip('\\') + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "powershell.exe;test-path ' + profilepath + '"'
	print command
	write(location.strip('\\') + '\\reflogfile.log', command)
	command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	out, err = command.communicate()
	print out
	write(location.strip('\\') + '\\reflogfile.log', out)

	if "False" in str(out):
		print "POST:F:The profile Path does not exists"
		write(location.strip('\\') + '\\' + logfile, "POST:F:The profile Path does not exists")
	else:
		write(location.strip('\\') + '\\reflogfile.log','win35 : this command is used to find the instance')
		command = 'c:\\python27\\python ' + location.strip('\\') + '\\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "dir ' + profilepath + ' /s /b | findstr DVEBMGS* | findstr -V # | findstr -V START"'
		write(location.strip('\\') + '\\reflogfile.log',"win35:" + command)
		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
		out, err = command.communicate()
		write(location.strip('\\') + '\\reflogfile.log',out)
		profilepath = out.split('\n')[3].strip()
		print profilepath
		write(location.strip('\\') + '\\reflogfile.log','win35 : this command is used to get content of profile path ans select rdisp/wp_no_btc ')
		command='c:\\python27\\python ' + location.strip('\\') + '\\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "powershell.exe;\"\\"get-content ' + profilepath + ' | select-string rdisp/wp_no_btc\\"\""'
		write(location.strip('\\') + '\\reflogfile.log',"win35:" + command)
		print command
		command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
		out, err = command.communicate()
		write(location.strip('\\') + '\\reflogfile.log',out)
		#print out
		out=out.split('\n')
		#print out
		out=''.join(out)
		#print out
		if 'rdisp/wp_no_btc' not in out:
			write(location.strip('\\') + '\\reflogfile.log','win35 :this command is used to add content to the profile path and set value as 1')
			command='c:\\python27\\python ' + location.strip('\\') + '\\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "powershell.exe;\"\\"add-content ' + profilepath + ' \'rdisp/wp_no_btc = 1\'\\"\"'
			write(location.strip('\\') + '\\reflogfile.log',"win35:" + command)
			print command
			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
			out, err = command.communicate()
			write(location.strip('\\') + '\\reflogfile.log',out)
			#print out
			if command.returncode == 0:
				print 'PRE:P:parameter set to one'
				write(location.strip('\\') + '\\' + logfile,'PRE:P:parameter set to one')
			else:
				print 'PRE:F:parameter not set to one'
				write(location.strip('\\') + '\\' + logfile,'PRE:F:parameter not set to one')
		else:
			parameter = out.split('used',1)
			#print parameter
			parameter = parameter[1].strip()
			print parameter
			command='c:\\python27\\python ' + location.strip('\\') + '\\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "powershell.exe;\"\\"(Get-Content ' + profilepath +').Replace(\'' + parameter + '\',\'rdisp/wp_no_btc = 1\') | set-content ' + profilepath + '"\\"\"'
			write(location.strip('\\') + '\\reflogfile.log',"win35:" + command)
			print command
			command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
			out, err = command.communicate()
			write(location.strip('\\') + '\\reflogfile.log',out)
			#print out
			if command.returncode == 0:
				print 'PRE:P:parameter set to one'
				write(location.strip('\\') + '\\' + logfile,'PRE:P:parameter set to one')
			else:
				print 'PRE:F:parameter not set to one'
				write(location.strip('\\') + '\\' + logfile,'PRE:F:parameter not set to one')
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
		space_check(argv[1], argv[2], argv[3], argv[4], argv[6], argv[5])
		
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
		write(location.strip('\\') + '\\reflogfile.log',"PRE :" + str(e))
