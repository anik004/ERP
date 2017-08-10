import paramiko
from paramiko import *
from sys import *
from log4erp import *

try:
    if argv[1] == "--u":
     print "Usage: python dbstop.py <Target database host> <Target database root> <Target database root passwd> <Target Database SID> <Refresh ID>"
    else:
     if len(argv) < 5:
        print "F:DBSTOP: Argument/s missing for the script [Error Code - 1302]"
     else:

        hostname = argv[1]
        username_db = argv[2]
        password_db = argv[3]
        db_sid = argv[4]

        logfile= argv[5] + ".log"

        user_db = "ora" + db_sid.lower()

        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname,username = username_db, password = password_db)
        channel = client.invoke_shell()
	#write(logfile,'PRE:I: DB Triggered')

        command = 'sudo su - ' + user_db + ' -c \'echo "shutdown immediate" | sqlplus / as sysdba\''
        #print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	out = stdout.readlines()
#	print out[11]
        status = stdout.channel.recv_exit_status()
        #print status
	if "does not exist" in out[0]:
	    print 'DBSTOP:F: The Target Database SID - ' + db_sid + 'passed by the user is incorrect'
	    write (logfile, 'DBSTOP:F: The Target Database SID - ' + db_sid + ' passed by the user is incorrect')
	    exit()
	elif "ORACLE not available" in out[7]:
	    print 'DBSTOP:P: The Target Database is already stopped on the target server (HOSTNAME - ' + hostname + ')'
	    write (logfile, 'PRE:P: The Target Database is already stopped on the target server (HOSTNAME - ' + hostname + ')')
        elif "ORACLE instance shut down" in out[11]: 
            print 'DBSTOP:P: The Database has been stopped on the target server (HOSTNAME - ' + hostname + ')'
            log = 'PRE:P: The Database has been stopped on the target server (HOSTNAME - ' + hostname + ')'
            write (logfile, log)
        command = 'sudo su - ' + user_db + ' -c \'lsnrctl stop\''
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        status = stdout.channel.recv_exit_status()

        if status == 0 or status == 1:
                print 'DBSTOP:P: The listener has been stopped on the target server (HOSTNAME - ' + hostname +')'
                log = 'PRE:P: The listener has been stopped on the target server (HOSTNAME - ' + hostname +')'
                write(logfile, log)
        else:
                print 'DBSTOP:F: The Database is not successfully stopped successfully on the target server (HOSTNAME - ' + hostname + ')'
                log = 'PRE:F: The Database is not successfully stopped successfully on the target server (HOSTNAME - ' + hostname + ')'
                write (logfile, log)
        channel.close()
        client.close()

except Exception as e:
     if str(e) == "[Errno -2] Name or service not known":
                print "DBSTOP:F:GERR_1301:Target Hostname - " + hostname + " unknown"
                write(logfile,'PRE:F: Hostname - ' + hostname + ' unknown [Error Code - 1301]')
     elif str(e) == "list index out of range":
                print "DBSTOP:F:GERR_1302:Argument/s missing for the script"
                write(logfile,'PRE:F: Argument/s missing for the script [Error Code - 1302]')
     elif str(e) == "Authentication failed.":
                print "DBSTOP:F:GERR_1303:Authentication failed to the Target Server."
                write(logfile,'PRE:F:Authentication failed to the Target Server.[Error Code - 1303]')
     elif str(e) == "[Errno 110] Connection timed out":
                print "DBSTOP:F:GERR_1304: Target Host Unreachable"
                write(logfile,'PRE:F:Target Host Unreachable.[Error Code - 1304]')
     elif "getaddrinfo failed" in str(e):
                print "DBSTOP:F:GERR_1305: Please check the hostname that you have provide"
                write(logfile,'PRE:F: Please check the hostname that you have provide [Error Code - 1305]')
     elif "[Errno None] Unable to connect to port 22 on" in str(e):
                print "DBSTOP:F:GERR_1306:Host Unreachable or Unable to connect to port 22"
                write(logfile,'PRE:F: Host Unreachable or Unable to connect to port 22 [Error Code - 1306]')
     elif "invalid decimal" in str(e):
                print "DBSTOP:F:GERR_1307:Unknown Error:" + str(e)
                write(logfile,'PRE:F: Unknown Error:' + str(e) + '[Error Code - 1307]')
     else:
                print "DBSTOP:F: " + str(e)
