#!/usr/bin/python

import paramiko
from sys import *
from paramiko import *


try:
    if argv[1] == "--u":
        print "usage: python PRE.py <Host> <sudo user> <sudo password> <DB/AI/CI> <Source/Target>"
    else:
	hostname=argv[1]
        sudo_user=argv[2]
	password=argv[3]
	user="root"

        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect( hostname,username = sudo_user, password = password)
        channel = client.invoke_shell()
	command="sudo su - " + user + " '-c exit'"
	#print command
	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	stdin.write(password +'\n')
        stdin.flush()
	status = stdout.channel.recv_exit_status()
	#print stdout.readlines()
	#print status

	if status == 0:
                print "PRE:P:Sudo user " + sudo_user + " has Root access on " + hostname
	else:
		print "PRE:P:Sudo user " + sudo_user + " does not has Root access on " + hostname
        channel.close()
        client.close()
except Exception as e:
 if str(e) == "[Errno -2] Name or service not known":
 	print "PRE:F:GERR_0301:Hostname unknown"
 elif str(e) == "list index out of range":
        print "PRE:F:GERR_0302:Argument/s missing for the script"
 elif str(e) == "Authentication failed.":
	print "PRE:F:GERR_0303:Authentication failed."
 elif str(e) == "[Errno 110] Connection timed out":
	print "PRE:F:GERR_0304:Host Unreachable"
 elif "getaddrinfo failed" in str(e):
        print "PRE:F:GERR_0305: Please check the hostname that you have provide"
 elif "[Errno None] Unable to connect to port 22 on" in str(e):
	print "PRE:F:GERR_0306:Host Unreachable or Unable to connect to port 22"
 else:
        print "F: " + str(e)
