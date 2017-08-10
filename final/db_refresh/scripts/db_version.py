import paramiko
from paramiko import *
from sys import *
from log4erp import *

try:
    if argv[1] == "--u":
        print "Usage: python db_version.py <Target database host> <Target DB sudo user> <Target DB sudo user passwd> <Target Database SID> <Refresh ID>"
    else:
	host = argv[1]
	sudo_user = argv[2]
	passwd = argv[3]
	database_sid = argv[4]
	db_user = "ora" + database_sid.lower()
	logfile = argv[5]

	client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host,username = sudo_user, password = passwd)
        channel = client.invoke_shell()

	command = 'sudo su - ' + db_user + ' -c \'echo select version from v\$"instance;" | sqlplus / as sysdba \' '
        print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        status = stdout.channel.recv_exit_status()
#       print status
        out = stdout.readlines()
	out = out[12].strip()

	command = "whoami"
        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        out, err = command.communicate()
        directory = out.strip()
	
	command = " echo \'" + out + "\' > /home/" + directory + "/geminyo/scripts/version.txt"
        command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        out, err = command.communicate()

		#print "DB_END_MODE:F: Failed to put Source Database is in end backup mode Hostname - " + host
		#write(logfile,'POST:F: Failed to put Source Database is in end backup mode Hostname - ' + host)

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
