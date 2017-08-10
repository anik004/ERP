import paramiko
from paramiko import *
from sys import *
from log4erp import *

try:
    if argv[1] == "--u":
        print "usage: python resetlog.py <Target Database Host> <Target Database Sudo User Name> <Target Database Sudo User Password> <Target Database SID> <Refresh ID>"
    else:
        hostname = argv[1]
        username = argv[2]
        password = argv[3]
        db_sid = argv[4]
        
        user = "ora" + argv[4].lower()
        logfile = argv[5] + ".log"

        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname,username = username, password = password)
        channel = client.invoke_shell()

        command = 'sudo su - ' + user + ' -c \"echo \'ALTER DATABASE MOUNT;\' | sqlplus / as sysdba\"'
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	print stdout.readlines()
        status = stdout.channel.recv_exit_status()
        if status == 0:
            print "RESETLOG:I: The database has been mounted in the Target database server (HOSTNAME - " + hostname + ")"
            log = "POST:I: The database has been mounted in the Target database server (HOSTNAME - " + hostname + ")"
            write(logfile,log)
            command = 'sudo su - ' + user + ' -c \"echo \'ALTER DATABASE OPEN RESETLOGS;\' | sqlplus / as sysdba | grep -i -e \'Database altered\' -e \'a database already open by the instance\'\"'
            print command
            stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	    final_status = stdout.readlines()
	    print final_status
            final_status=final_status[0].strip()
	    print final_status
            status = stdout.channel.recv_exit_status()
            print status
#            final_status = stdout.readlines()
#            final_status=final_status[0].strip()
            #command = 'sudo su - ' + user + ' -c \"echo \'ALTER DATABASE OPEN;\' | sqlplus system/Welcome2 | grep -i -e \\"database altered\\" -e \\"a database already open by the instance\\""'
            #stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
            #print command

            #final_status = stdout.readlines()
            print final_status
            if 'Database altered' in final_status:
                print "RESETLOG:P: The resetlogs has been altered on the target server (HOSTNAME - " + hostname + ")"
                log = "POST:P: The resetlogs has been altered on the target server (HOSTNAME - " + hostname + ")"
                write(logfile,log)
            elif 'a database already open by the instance' in final_status:
                print "RESETLOG:P: The resetlogs has been already altered on the target server (HOSTNAME - " + hostname + ")"
                log = "POST:I: The resetlogs has been already altered on the target server (HOSTNAME - " + hostname + ")"
                write(logfile, log)
            else:
                print "RESETLOG:F: The resetlogs are failed to be altered on the target server (HOSTNAME - " + hostname + ")"
                log = "POST:F: The resetlogs are failed to be altered on the target server (HOSTNAME - " + hostname + ")"
                write (logfile, log)
        else:
            print "RESETLOG:F: The database has not been mounted in the Target database server (HOSTNAME - " + hostname + ")"
            log = "POST:F: The database has not been mounted in the Target database server (HOSTNAME - " + hostname + ")"
            write (logfile, log)

except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "RESETLOG:F:GERR_1901:Hostname unknown"
        write(logfile,'POST:F: Hostname unknown [Error Code - 1901]')
    elif str(e).strip() == "list index out of range":
        print "RESETLOG:F:GERR_1902:Argument/s missing for resetlog script"
    elif str(e) == "Authentication failed.":
        print "RESETLOG:F:GERR_1903:Authentication failed."
        write(logfile,'POST:F:Authentication failed[Error Code - 1903]')
    elif str(e) == "[Errno 110] Connection timed out":
        print "RESETLOG:F:GERR_1904:Host Unreachable"
	write(logfile,'POST:F:Host Unreachable.[Error Code - 1904]')
    elif "getaddrinfo failed" in str(e):
        print "RESETLOG:F:GERR_1905: Please check the hostname that you have provide"
        write(logfile,'POST:F: Please check the hostname that you have provide [Error Code - 1905]')
    elif "[Errno None] Unable to connect to port 22 on" in str(e):
        print "RESETLOG:F:GERR_1906:Host Unreachable or Unable to connect to port 22"
        write(logfile,'POST:F: Host Unreachable or Unable to connect to port 22 [Error Code - 1906]')
    else:
        print "RESETLOG:F: " + str(e)
