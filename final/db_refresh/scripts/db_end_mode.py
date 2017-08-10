import paramiko
from paramiko import *
from sys import *
from log4erp import *

try:
    if argv[1] == "--u":
        print "Usage: python db_end_mode.py <Source database host> <Source sudo user> <Source sudo user passwd> <Source Database SID> <Refresh ID>"
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

	command = 'sudo su - ' + db_user + ' -c \'echo "alter database end backup;" | sqlplus / as sysdba\''
#	print command
	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        status = stdout.channel.recv_exit_status()
#	print status
	out = stdout.readlines()
#	print out
#	print out[13]
	if "does not exist" in out[0].strip():
		print "DB_END_MODE:F:Wrong DB sid - " + argv[4] + " has been passed. Please enter the correct DB sid"
		write(logfile,'POST:F:Wrong DB sid - ' + argv[4] + " has been passed. Please enter the correct DB sid")
		exit()
	if "none of the files are in backup" in out[13].strip():
		print "DB_END_MODE:P: Source Database is already in end backup mode Hostname - " + host
		write(logfile,'POST:P:Source Database is already in end backup mode Hostname - ' + host)
		exit()

	if status == 0:
		print "DB_END_MODE:P: Source Database is in end backup mode Hostname - " + host
		write(logfile,'POST:P:Source Database is in end backup mode Hostname - ' + host)
	else:
		print "DB_END_MODE:F: Failed to put Source Database is in end backup mode Hostname - " + host
		write(logfile,'POST:F: Failed to put Source Database is in end backup mode Hostname - ' + host)

except Exception as e:
     if str(e) == "[Errno -2] Name or service not known":
                print "DB_END_MODE:F:GERR_1301:Hostname unknown"
                write(logfile,'POST:F: Hostname unknown [Error Code - 1301]')
     elif str(e) == "list index out of range":
                print "DB_END_MODE:F:GERR_1302:Argument/s missing for the script"
                write(logfile,'POST:F: Argument/s missing for the script [Error Code - 1302]')
     elif str(e) == "Authentication failed.":
                print "DB_END_MODE:F:GERR_1303:Authentication failed."
                write(logfile,'POST:F:Authentication failed.[Error Code - 1303]')
     elif str(e) == "[Errno 110] Connection timed out":
                print "DB_END_MODE:F:GERR_1304:Host Unreachable"
                write(logfile,'POST:F:Host Unreachable.[Error Code - 1304]')
     elif "getaddrinfo failed" in str(e):
                print "DB_END_MODE:F:GERR_1305: Please check the hostname that you have provide"
                write(logfile,'POST:F: Please check the hostname that you have provide [Error Code - 1305]')
     elif "[Errno None] Unable to connect to port 22 on" in str(e):
                print "DB_END_MODE:F:GERR_1306:Host Unreachable or Unable to connect to port 22"
                write(logfile,'POST:F: Host Unreachable or Unable to connect to port 22 [Error Code - 1306]')
     elif "invalid decimal" in str(e):
                print "DB_END_MODE:F:GERR_1307:Unknown Error:" + str(e)
                write(logfile,'Post:F: Unknown Error:' + str(e) + '[Error Code - 1307]')
     else:
                print "DB_END_MODE:F: " + str(e)
