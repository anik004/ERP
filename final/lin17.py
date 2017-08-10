import paramiko
from paramiko import *
from sys import *
from log4erp import *
import re

try:
    if argv[1] == "--u":    
	print "Usage: python sapstopapp.py <Target application Host> <Target application Login User Name> <Target application User Password> <Target Application SID> <Instance ID> <Instance Host>"
    else:
        hostname = argv[1]
        username = argv[2]
        password = argv[3]
        app_sid = argv[4]

        instance = argv[5]
        logfile= argv[7] + ".log"
        host = argv[6]
	profile_path = argv[8].rstrip('/')	

        user_sap = app_sid.lower() + "adm"

        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname,username = username, password = password)
        channel = client.invoke_shell()

        command = 'sudo su - ' + user_sap + ' -c \'cd ' + profile_path + ' ; ls | grep -i ' + host + ' | grep -v "\." | grep -v "ASC" | cut -d"_" -f2\''
	print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	#print stdout.readlines()
        status = stdout.readlines()[0]
	
        command = 'sudo su - ' + user_sap + ' -c \'startsap -c |grep -i ' + status.strip() + ' --color=never | tail -n -1 | cut -d" " -f4\''
	print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        status = stdout.readlines()
        #if status[0].strip() != "running":
        #    print "PRE:P: The SAP service is already stopped on the target server (HOSTNAME - " + hostname + ")"
        #    log = "PRE:P: The SAP service is already stopped on the target server (HOSTNAME - " + hostname + ")"
        #    write (logfile, log)
        #else:

        command = 'sudo su - ' + user_sap + ' -c "stopsap r3 '  + host + '"'
	print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        status = stdout.channel.recv_exit_status()
        if status == 0:
                print "PRE:P: The SAP service has been stopped on the target server (HOSTNAME - " + hostname + ")"
                log = "PRE:P: The SAP service has been stopped on the target server (HOSTNAME - " + hostname + ")"
                write (logfile, log)
        else:
                print "PRE:F: The SAP server has not been successfully stopped on the target server (HOSTNAME - " + hostname + ")"
                log = "PRE:F: The SAP server has not been successfully stopped on the target server (HOSTNAME - " + hostname + ")"
                write (logfile, log)

        command = "sudo su - " + user_sap + " -c 'ps -ef | grep -i " + user_sap + " | grep -i /usr/sap | grep -v # | grep -i " + host + " |  cut -d\" \" -f4'"
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        all_names = stdout.readlines()
        for n in range (0, (len(all_names))):
                proc = all_names[n].strip()
                command = "sudo su - " + user_sap + ' -c "kill -9 ' + proc + '"'
#		print command
                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
                if stdout.channel.recv_exit_status() == 0:
                    print "PRE:I: The processes related to the SAP has been stopped in the target application server (HOSTNAME - " + hostname + ")"
                    log = "PRE:I: The processes related to the SAP has been stopped in the target application server (HOSTNAME - " + hostname + ")"
                    write (logfile, log)
 #           write (logfile, log)
        channel.close()
        client.close()

except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "PRE:F:GERR_3001:Hostname unknown"
        log4erp.write(logfile,'PRE:F: Hostname unknown [Error Code - 3001]')
    elif str(e).strip() == "list index out of range":
        print "PRE:F:GERR_3002:Argument/s missing for sapstartapp script"
    elif str(e) == "Authentication failed.":
        print "PRE:F:GERR_3003:Authentication failed."
        log4erp.write(logfile,'PRE:F:Authentication failed[Error Code - 3003]')
    elif str(e) == "[Errno 110] Connection timed out":
        print "PRE:F:GERR_3004:Host Unreachable"
        write(logfile,'PRE:F:Host Unreachable.[Error Code - 3004]')
    elif "getaddrinfo failed" in str(e):
        print "PRE:F:GERR_3005: Please check the hostname that you have provide"
        log4erp.write(logfile,'PRE:F: Please check the hostname that you have provide [Error Code - 3005]')
    elif "[Errno None] Unable to connect to port 22 on" in str(e):
        print "PRE:F:GERR_3006:Host Unreachable or Unable to connect to port 22"
        write(logfile,'PRE:F: Host Unreachable or Unable to connect to port 22 [Error Code - 3006]')
    else:
        print "PRE:F: " + str(e)
	write(logfile,"PRE:F: " + str(e))
