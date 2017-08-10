import paramiko
from paramiko import *
from sys import *
from log4erp import *

client = SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('sapredhat02',username = 'erpadm', password = 'Welcome2')
channel = client.invoke_shell()

cmd = "sudo ls /oracle/DRP/oraarch/DQR*"
print cmd
stdin, stdout, stderr = client.exec_command(cmd,timeout=2000,get_pty=True)
filename = stdout.readlines()
for a in filename:
	b = a.encode('UTF8')
	#print type(b)
	cmd = "sudo ls " + b.strip() + "| sed -r \'s#" + "DQR" + "#" + "DRP" + "#\'"
	#print cmd
	stdin, stdout, stderr = client.exec_command(cmd, timeout=2000, get_pty=True)
        filename = stdout.readlines()
        #print filename
        command = "sudo mv " + b.strip() + " " + filename[0]
        #print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)

cmd = "sudo ls /oracle/DRP/oraarch/*f?"
stdin, stdout, stderr = client.exec_command(cmd,timeout=2000,get_pty=True)
filenames = stdout.readlines()
for a in filenames:
        b = a.encode('UTF8')
	cmd = "sudo ls " + b.strip() + "| sed -r \'s#" + "f[?]" + "#" + "f" + "#\'"
	print cmd
	stdin, stdout, stderr = client.exec_command(cmd, timeout=2000, get_pty=True)
        filename = stdout.readlines()
	#print filename[0]
	command = "sudo mv " + b.strip() + " " + filename[0]
	print command
	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	print stdout.readlines()

