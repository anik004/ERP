#print 'PRE:W:The database type "Sybase" is not supported'
# -*- coding: utf-8 -*- 
from paramiko import *
import paramiko
from sys import *
import re
import subprocess

#from log4erp import *
try:

	hostname = argv[1]
	username = argv[2]
	password = argv[3]
	database_sid=argv[4].strip()
	db_user = argv[5]
	db_password = argv[6]
	path = argv[7]
	
	user = "syb" + database_sid.lower()

	client = SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect( hostname,username = username, password = password)
	channel = client.invoke_shell()
	jobtables = ['BTCEVTJOB','BTC_CRITERIA','BTC_CRITNODES','BTC_CRITPROFILES','BTC_CRITTYPES','BTC_TYPEFIELDS','REORGJOBS','TBTCA','TBTCB','TBTCCNTXT','TBTCCTXTT','TBTCCTXTTP','TBTCI','TBTCJSTEP','TBTCO','TBTCP','TBTCR','TBTCS']
	file=open("truncatetable.sql","w+")
	file.write('use ' + database_sid.upper() + '\n')
	for i in jobtables:
		file.write('Truncate TABLE SAPSR3.' + i + '\n')
	file.write("go");
	file.close()

	port = 22

	remote= '/tmp/truncatetable.sql'
        print remote
        local= path + '/truncatetable.sql'
        print local

	transport = paramiko.Transport((hostname, port))
	transport.connect(username = username, password = password)
	sftp = paramiko.SFTPClient.from_transport(transport)
	sftp.put(local, remote)

	
	command = "sudo su - " + user + " -c \' isql -U" + db_user + " -P" + db_password + " -S"+ database_sid.upper() +" -X -i/tmp/truncatetable.sql \'"""
	print command
	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	print stdout.readlines()
	print "hi"
	status = stdout.channel.recv_exit_status()
	print status
	out = stdout.readlines()
	print out
	if not out:
		print "PRE:P:Database login  check for " + user + " is successful on  server " + hostname
	else:
		print "PRE:F:Database login  check for " + user + " is failed on  server " + hostname
#p = []
#out = str(out).replace(" ","")
#p = ' \n'.join(out.split()) 
#out= (out.strip()).split('\n')
#print type(p)
#for each in out:
#	print each.split(' ')
	sftp.close()
	transport.close()
	channel.close()
	client.close()
except Exception as e:
        if str(e) == "[Errno -2] Name or service not known":
                print "PRE:F:GERR_0201:Hostname unknown"
        elif str(e).strip() == "list index out of range":
                print "PRE:F:GERR_0202:Argument/s missing for the script"
        elif str(e) == "Authentication failed.":
                print "PRE:F:GERR_0203:Authentication failed for the " + string + " system " + hostname + " for user " + sudo_user
        elif str(e) == "[Errno 110] Connection timed out":
                print "PRE:F:GERR_0204:Host Unreachable"
        elif "getaddrinfo failed" in str(e):
                print "PRE:F:GERR_0205: Please check the hostname that you have provide"
        elif "[Errno None] Unable to connect to port 22 on" in str(e):
                print "PRE:F:GERR_0206:Host Unreachable or Unable to connect to port 22"
        else:
                print "PRE:F: " + str(e)

