import paramiko
from paramiko import *
from sys import *
from log4erp import *

try:
	t_host = argv[1]
	t_user = argv[2]
	t_pass = argv[3]
	t_dbsid = argv[4]
	logfile = argv[5]

	client = SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(t_host,username = t_user, password = t_pass)
	channel = client.invoke_shell()

	cmd = "chmod 777 /oracle/" + t_dbsid.upper() + "/oraarch"
	print cmd
	stdin, stdout, stderr = client.exec_command(cmd, timeout=2000, get_pty=True)
	print stdout.readlines()

	cmd = "chmod 777 /oracle/" + t_dbsid.upper() + "/oraarch/*"
	print cmd
	stdin, stdout, stderr = client.exec_command(cmd, timeout=2000, get_pty=True)
	print stdout.readlines()

	cmd = "chown ora" + t_dbsid.lower() + ":dba /oracle/" + t_dbsid.upper() + "/oraarch/*"
	print cmd
	stdin, stdout, stderr = client.exec_command(cmd,timeout=2000,get_pty=True)
	print stdout.readlines()

except Exception as e:
	if str(e) == "[Errno -2] Name or service not known":
                print "SCPARCHIVE:F:GERR_1301:Target Hostname unknown - " + t_host
                write(logfile,'POST:F: Target Hostname unknown - ' + t_host + ' [Error Code - 1301]')
	elif str(e) == "list index out of range":
                print "SCPARCHIVE:F:GERR_1302:Argument/s missing for the script"
	elif str(e) == "Authentication failed.":
                print "SCPARCHIVE:F:GERR_1303:Authentication failed to the Target Server - " + t_host
                write(logfile,'POST:F:Authentication failed to the Target Server - ' + t_host + ' [Error Code - 1303]')
	elif str(e) == "[Errno 110] Connection timed out":
                print "SCPARCHIVE:F:GERR_1304:Target Host Unreachable"
                write(logfile,'POST:F:Target Host Unreachable.[Error Code - 1304]')
	elif "getaddrinfo failed" in str(e):
                print "SCPARCHIVE:F:GERR_1305: Please check the Target hostname that you have provide" + t_host
                write(logfile,'POST:F: Please check the Target hostname that you have provide ' + + t_host + ' [Error Code - 1305]')
	elif "[Errno None] Unable to connect to port 22 on" in str(e):
                print "SCPARCHIVE:F:GERR_1306:Target Host Unreachable or Unable to connect to port 22"
                write(logfile,'POST:F: Target Host Unreachable or Unable to connect to port 22 [Error Code - 1306]')
	elif "invalid decimal" in str(e):
                print "SCPARCHIVE:F:GERR_1307:Unknown Error:" + str(e)
                write(logfile,'Post:F: Unknown Error:' + str(e) + '[Error Code - 1307]')
	else:
                print "SCPARCHIVE:F: " + str(e)
                write(logfile,'Post:F: ' + str(e))

