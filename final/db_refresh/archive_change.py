import paramiko
from paramiko import *
from sys import *
from log4erp import *

client = SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('sapredhat02',username = 'erpadm', password = 'Welcome2')
channel = client.invoke_shell()

command = "sudo ls --color=never /oracle/DRP/oraarch/DQR*"
print command
stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
str1 = ''.join(stdout.readlines())
print str1
print type(str1)
for files in str1:
	#fi = files.split()
	#print fi
	#print type(fi)
	print files
	command = "sudo ls " + files + "| sed -r \'s#" + "DQR" + "#" + "DRP" + "#\'"
	print command	
	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	filename = stdout.readlines()
	print filename
#	command = "sudo mv " + files + " " + filename[0]  
#	print command
#	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
#	print stdout.readlines()
