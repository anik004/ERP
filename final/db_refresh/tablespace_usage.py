import paramiko
from paramiko import *
from sys import *
from log4erp import *
import subprocess

try:
    if argv[1] == "--u":
        print "Usage: python db_begin_mode.py <Source database host> <Source sudo user> <Source sudo user passwd> <Source Database SID> <Refresh ID>"
    else:
	host = argv[1]
	sudo_user = argv[2]
	passwd = argv[3]
	db_user = "ora" + argv[4]
	logfile = argv[5]

	client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host,username = sudo_user, password = passwd)
        channel = client.invoke_shell()
	
	command = 'sudo su - ' + db_user + ' -c \'echo "select * From DBA_TABLESPACE_USAGE_METRICS;" | sqlplus / as sysdba\'| awk \'{print $3}\' | awk \'NR>12\' | head -n -4'
	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        status = stdout.channel.recv_exit_status()
	out = stdout.readlines()
	total_size = 0
	for size in out:
		total_size = float(total_size) + float(size.strip())
	total_size = ((total_size / 1024) / 1024) / 1024
	print "Total Space"
	print float(total_size)

	command = 'sudo su - ' + db_user + ' -c \'echo "select * From DBA_TABLESPACE_USAGE_METRICS;" | sqlplus / as sysdba\'| awk \'{print $2}\' | awk \'NR>12\' | head -n -4'
#	print command
	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        status = stdout.channel.recv_exit_status()
#	print status
	out = stdout.readlines()
#	print out
	used_total_size = 0
	for size in out:
		used_total_size = float(used_total_size) + float(size.strip())
	used_total_size = ((used_total_size / 1024) / 1024) / 1024
	print "Used Space"
	print float(used_total_size)
	channel.close()
	client.close()

except Exception as e:
     if str(e) == "[Errno -2] Name or service not known":
                print "DB_BEGIN_MODE:F:GERR_1301:Hostname unknown - " + host 
                write(logfile,'POST:F: Hostname unknown - ' + host + ' [Error Code - 1301]')
     elif str(e) == "list index out of range":
                print "DB_BEGIN_MODE:F:GERR_1302:Argument/s missing for the script"
     elif str(e) == "Authentication failed.":
                print "DB_BEGIN_MODE:F:GERR_1303:Authentication failed to the Source server - " + host
                write(logfile,'POST:F:Authentication failed to the Source server - ' + host + ' [Error Code - 1303]')
     elif str(e) == "[Errno 110] Connection timed out":
                print "DB_BEGIN_MODE:F:GERR_1304:Source Host Unreachable - " + host
                write(logfile,'POST:F:Source Host Unreachable - ' + host + ' [Error Code - 1304]')
     elif "getaddrinfo failed" in str(e):
                print "DB_BEGIN_MODE:F:GERR_1305: Please check the hostname that you have provide"
                write(logfile,'POST:F: Please check the hostname that you have provide [Error Code - 1305]')
     elif "[Errno None] Unable to connect to port 22 on" in str(e):
                print "DB_BEGIN_MODE:F:GERR_1306:Host Unreachable or Unable to connect to port 22"
                write(logfile,'POST:F: Host Unreachable or Unable to connect to port 22 [Error Code - 1306]')
     elif "invalid decimal" in str(e):
                print "DB_BEGIN_MODE:F:GERR_1307:Unknown Error:" + str(e)
                write(logfile,'Post:F: Unknown Error:' + str(e) + '[Error Code - 1307]')
     else:
                print "DB_BEGIN_MODE:F: " + str(e)
		write(logfile,'Post:F: ' + str(e))
