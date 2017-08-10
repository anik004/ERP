import paramiko
from paramiko import *
from sys import *
from log4erp import *
import re

try:
    if argv[1] == "--u":
        print "Usage: python sapstopapp.py <Target application Host> <Target application Login User Name> <Target application User Password> <Target Application SID> <Instance ID> <Instance Host> <reference ID>"
    else:
        hostname = argv[1]
        username = argv[2]
        password = argv[3]
        app_sid = argv[4]

        instance = argv[5]
        logfile= argv[7] + ".log"
        host = argv[6]

        user_sap = app_sid.lower() + "adm"

        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname,username = username, password = password)
        channel = client.invoke_shell()

	command = 'sudo su - ' + user_sap + ' -c "startsap -c" | tail -n -1 | cut -d" " -f4'
	#print command
	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        status = stdout.readlines()
#	print status
	if status[0].strip() == "not":
	    print "SAPSTOP:P: The SAP service is already stopped on the target server (HOSTNAME - " + host + ")"
	    log = "PRE:P:The SAP service is already stopped on the target server (HOSTNAME - " + host + ")"
            write (logfile, log)
	elif "does not exist" in status[0].strip():
	    print "SAPSTOP:F: The Target Application SID - " + app_sid + " entered by the user is incorrect"
	    write (logfile, "PRE:F:The Target Application SID - " + app_sid + " entered by the user is incorrect")
	    exit()

            command = 'sudo su - ' + user_sap + ' -c "stopsap r3 '  + host + '"'
#	    print command
            stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
            status = stdout.channel.recv_exit_status()
	    out = stdout.readlines()
	    out = out[0]
	    if "No instance profiles found" in out.strip():
		print "SAPSTOP:F: The Instance Hostname -" + host + " provided does not exist on the target server (HOSTNAME - " + host + ")"
		log = "PRE:F:The Instance Hostname -" + host + " provided does not exist on the target server (HOSTNAME - " + host + ")"
		write (logfile, log)
		exit()
            if status == 0:
                print "SAPSTOP:P: The SAP service has been stopped on the target server (HOSTNAME - " + host + ")"
                log = "PRE:P:The SAP service has been stopped on the target server (HOSTNAME - " + host + ")"
                write (logfile, log)
            else:
                print "SAPSTOP:F: The SAP server has not been successfully stopped on the target server (HOSTNAME - " + host + ")"
                log = "PRE:F:The SAP server has not been successfully stopped on the target server (HOSTNAME - " + host + ")"
                write (logfile, log)
		exit()
        command = 'sudo su - ' + user_sap + ' -c \'cleanipc ' + instance+ ' remove;cleanipc ' + instance + ' remove\''
#        print command
	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        status = stdout.channel.recv_exit_status()
	out = stdout.readlines()
	#print out[4]
	#print status
	if "Error" in out[4]:
	    print 'SAPSTOP:F: Isntance Id - ' + instance +  'passed does not exist on the target server (HOSTNAME - ' + host + ')'
	    log = 'PRE:F:Isntance Id - ' + instance +  'passed does not exist on the target server (HOSTNAME - ' + host + ')'
	    write (logfile, log)
	    exit()
        if status == 0:
            print 'SAPSTOP:P: The CLEANIPC has been successfully completed on the target server (HOSTNAME - ' + host + ')'
            log = 'PRE:P:The CLEANIPC has been successfully completed on the target server (HOSTNAME - ' + host + ')'
            write (logfile, log)
        else:
            print 'SAPSTOP:F: The CLEANIPC has not been successfully done on the target server (HOSTNAME - ' + host + ')'
            log = 'PRE:F:The CLEANIPC has not been successfully done on the target server (HOSTNAME - ' + host + ')'
            write (logfile, log)
        channel.close()
        client.close()

except Exception as e:
     if str(e) == "[Errno -2] Name or service not known":
                print "SAPSTOPAPP:F:GERR_1201:Hostname unknown for Target Server (" + host + ")"
                write(logfile,'PRE:F:Hostname unknown for Target Server (' + host + ')[Error Code - 1201]')
     elif str(e) == "list index out of range":
                print "SAPSTOPAPP:F:GERR_1202:Argument/s missing for the script"
     elif str(e) == "Authentication failed.":
                print "SAPSTOPAPP:F:GERR_1203:Authentication failed."
                write(logfile,'PRE:F:Authentication failed.[Error Code - 1203]')
     elif str(e) == "[Errno 110] Connection timed out":
                print "SAPSTOPAPP:F:GERR_1204:Target Host Unreachable (" + host + ")"
                write(logfile,'PRE:F:Target Host Unreachable (' + host + ') [Error Code - 1204]')
     elif "getaddrinfo failed" in str(e):
                print "SAPSTOPAPP:F:GERR_1205: Please check the Target Hostname - " + hostname + " that you have provide"
                write(logfile,'PRE:F:Please check the Target Hostname - ' + hostname + ' that you have provide [Error Code - 1205]')
     elif "[Errno None] Unable to connect to port 22 on" in str(e):
                print "SAPSTOPAPP:F:GERR_1206:Host Unreachable or Unable to connect to port 22"
                write(logfile,'PRE:F:Host Unreachable or Unable to connect to port 22 [Error Code - 1206]')
     elif "invalid decimal" in str(e):
                print "SAPSTOPAPP:F:GERR_1207:Unknown Error:" + str(e)
                write(logfile,'PRE:F:Unknown Error:' + str(e) + '[Error Code - 1207]')
     else:
                print "SAPSTOPAPP:F:" + str(e)
