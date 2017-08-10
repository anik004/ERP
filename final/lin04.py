#!/usr/bin/python

# target IP - $1
# database sid - $2
# application sid - $3
# schema passwd - $4
import paramiko
from sys import *
from paramiko import *


try:
#    if argv[1] == "--u":
 #       print "usage: python os_user_existence.py <Host> <sudo user> <sudo password> <sid> <DB/AI/CI> <Source/Target>"
  #  else:
	hostname=argv[1]
        sudo_user=argv[2]
	password=argv[3]
	sid=argv[4]

	if argv[5].lower() == "db":
		user = "ora" + argv[4].lower()
	else:
		user = argv[4].lower() + "adm"
	
#	print user
        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect( hostname,username = sudo_user, password = password)
        channel = client.invoke_shell()

	command="sudo su - root '-c grep -iw ^" + user+ " /etc/passwd'"
#	print command
	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	status = stdout.channel.recv_exit_status()
	#print stdout.readlines()
#	print status

	if status == 1:
                print "PRE:F:User existence check for " + user + " failed using sudo user on" + hostname
                channel.close()
                client.close()
	else:
        	print "PRE:P:User existence check for " + user + " using sudo user ( " + sudo_user + " ) is successful on " + hostname
        channel.close()
        client.close()
except Exception as e:
	if str(e) == "[Errno -2] Name or service not known":
        	print "PRE:F:GERR_0201:Hostname unknown"
	elif str(e).strip() == "list index out of range":
                print "PRE:F:GERR_0202:Argument/s missing for the script"
	elif str(e) == "Authentication failed.":
		print "PRE:F:GERR_0203:Authentication failed."
	elif str(e) == "[Errno 110] Connection timed out":
		print "PRE:F:GERR_0204:Host Unreachable"
	elif "getaddrinfo failed" in str(e):
        	print "PRE:F:GERR_0205: Please check the hostname that you have provide"
	elif "[Errno None] Unable to connect to port 22 on" in str(e):
	        print "PRE:F:GERR_0206:Host Unreachable or Unable to connect to port 22"
    	else:
        	print "PRE:F: " + str(e)
