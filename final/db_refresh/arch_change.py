import paramiko
from paramiko import *
from sys import *
from log4erp import *



t_host = argv[1]
t_user= argv[2]
t_pass = argv[3]
t_dbsid = argv[4]
s_dbsid = argv[5]

client = SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(t_host,username = t_user, password = t_pass)
channel = client.invoke_shell()

cmd = " ls /oracle/" + t_dbsid.upper() + "/oraarch/" + s_dbsid.upper() + "*"
print cmd
stdin, stdout, stderr = client.exec_command(cmd,timeout=2000,get_pty=True)
filename = stdout.readlines()
for a in filename:
	b = a.encode('UTF8')
	#print type(b)
	cmd = "ls " + b.strip() + "| sed -r \'s#" + s_dbsid.upper() + "#" + t_dbsid.upper() + "#\'"
	#print cmd
	stdin, stdout, stderr = client.exec_command(cmd, timeout=2000, get_pty=True)
        filename = stdout.readlines()
        #print filename
        command = "mv -f " + b.strip() + " " + filename[0].strip()
        print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	print stdout.readlines()
