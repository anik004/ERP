import paramiko
from paramiko import *
from sys import *
from log4erp import *

client = SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('sapredhat02',username = 'erpadm', password = 'Welcome2')
channel = client.invoke_shell()

command = "sudo ls /oracle/DRP/oraarch/DQR*"
#print command
stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
filename = stdout.readlines()
str1 = ''.join(filename)
for files in str1.split("\t"):
	fi = files.split()
	#print fi
	command = "sudo ls " + fi[0] + "| sed -r \'s#" + "DQR" + "#" + "DRP" + "#\'"
	#print command	
	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	filename = stdout.readlines()
	print filename
	command = "sudo mv " + fi[0] + " " + filename[0]  
	print command
	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	print stdout.readlines()
