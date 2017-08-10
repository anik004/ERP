import paramiko
from sys import *
from paramiko import *
from log4erp import *
import log4erp
import os

try:
    if argv[1] == "--u":
        print "usage: python ops.py <Target Database Host>  <Target Sudo User> <Target Sudo Password> <Target Database SID> <Target APP SID> <Source Application SID> <Source DB SID> <Refresh ID>"
    else:
        t_db_user = "ora" + argv[4].lower()
        t_dbsid = argv[4].upper()
	t_appsid = argv[5].upper()
	s_appsid = argv[6].upper()
	s_dbsid = argv[7].upper()
	refresh_id = argv[8] + ".log"
        t_appuser = "OPS\$" + t_appsid + "ADM"
        dbuser = "OPS\$ORA"
        t_dbuser = dbuser + t_dbsid

        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(argv[1], username=argv[2], password=argv[3])
        channel = client.invoke_shell()

        print "OPS:I: Connection established Successfully (Hostname -" + argv[1] + ")"
        log4erp.write(refresh_id, 'POST:I: Connection established Successfully (Hostname -' + argv[1] + ')')

        print "OPS:I: Checking User Existence in target server (Hostname -" + argv[1] + ")"
        log4erp.write(refresh_id, 'POST:I: Checking User Existence in target server (Hostname -' + argv[1] + ')')

	command = "sudo su - " + t_db_user + " -c 'exit'; echo $?"
        stdin, stdout, stderr = client.exec_command(command, timeout=60, get_pty=True)
        status = stdout.readline()[0].rstrip()
#        print command
        if status != "0":
		print "OPS:F: The Target Database SID passed - " + t_dbsid + " by the user is incorrect"
		log4erp.write(refresh_id,'POST:F: The Target Database SID passed - ' + t_dbsid + ' by the user is incorrect')
		exit(0)
        else:
		print "OPS:I: User " + t_db_user + " exist in target server (Hostname -" + argv[1] + ")"
		log4erp.write(refresh_id, 'POST:I: User ' + t_db_user + ' exist in target server (Hostname -' + argv[1] + ')')


#################################################### CREATING APP USER ############################################

		status = "sudo su - " + t_db_user + " -c \"echo \'SELECT USERNAME FROM DBA_USERS;\' | sqlplus / as sysdba \" | grep -w -i --color=never OPS\$" + t_appsid + "ADM"
		print status
                stdin, stdout, stderr = client.exec_command(status, timeout=1000, get_pty=True)
		out = stdout.readlines()
		#print out
		#print out[0]
		if not out:
			command = "sudo su - " + t_db_user + " -c \"echo \'CREATE USER " + "\"" + t_appuser + "\"" + " DEFAULT TABLESPACE SYSTEM TEMPORARY TABLESPACE PSAPTEMP IDENTIFIED EXTERNALLY;\' | sqlplus / as sysdba\""
	                print command
			stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
			out = stdout.readlines()
			if "User created." in out[10]:
				print "OPS:I: Creating App User " + t_appuser + " in the target database server"
		                log4erp.write(refresh_id, 'POST:I: Creating App User ' + t_appuser + ' in the target database server')
                	else:
                    		print "OPS:I: Not able to create App User " + t_appuser + " in the target database server"
		                log4erp.write(refresh_id, 'POST:I: Not able to create App User ' + t_appuser + ' in the target database server')
				exit(0)
		else:			
			print "Application user exist"

################################################## CREATING DB USER #####################################################

		status = "sudo su - " + t_db_user + " -c \"echo \'SELECT USERNAME FROM DBA_USERS;\' | sqlplus / as sysdba \" | grep -w -i --color=never OPS\$ORA" + t_dbsid.upper()
		print status
                stdin, stdout, stderr = client.exec_command(status, timeout=1000, get_pty=True)
                out = stdout.readlines()
		if not out:
                        command = "sudo su - " + t_db_user + " -c \"echo \'CREATE USER " + "\"" + t_dbuser + "\"" + " DEFAULT TABLESPACE SYSTEM TEMPORARY TABLESPACE PSAPTEMP IDENTIFIED EXTERNALLY;\' | sqlplus / as sysdba\""
                        print command
                        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
                        out = stdout.readlines()
                        if "User created." in out[10]:
                                print "OPS:I: Creating DB User " + t_dbuser + " in the target database server"
                                log4erp.write(refresh_id, 'POST:I: Creating DB User ' + t_dbuser + ' in the target database server')
                        else:
                                print "OPS:I: Not able to create DB user " + t_dbuser + " in the target database server"
				log4erp.write(refresh_id, 'POST:F: Not able to create DB User ' + t_dbuser + ' in the target database server')
				exit()
		else:
			 print "DB user exist in the target database server"

################################################3 GRANTING PERMISSION ###############################################

		command = "sudo su - " + t_db_user + " -c \"echo \'GRANT DBA, SAPDBA, CONNECT, RESOURCE TO " + "\"" + t_appuser + "\"" + ";\' | sqlplus / as sysdba\""
                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
		out = stdout.readlines()
		if "Grant succeeded" in out[10]:
			print "OPS:I: Granting DBA, SAPDBA, CONNECT, RESOURCE permission to " + t_appuser
			log4erp.write(refresh_id,'POST:I: Granting DBA, SAPDBA, CONNECT, RESOURCE permission to ' + t_appuser + '')
		else:
			print "OPS:F: Not able to Grant DBA, SAPDBA, CONNECT, RESOURCE permission to " + t_appuser
	                log4erp.write(refresh_id,'POST:F: Not able to Grant DBA, SAPDBA, CONNECT, RESOURCE permission to ' + t_appuser + '')
			exit()
		
################################################### GRANTING PERMISSION to DB User ##############################

		command = "sudo su - " + t_db_user + " -c \"echo \'GRANT DBA, SAPDBA, CONNECT, RESOURCE TO " + "\"" + t_dbuser + "\"" + ";\' | sqlplus / as sysdba\""
                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
		out = stdout.readlines()
                if "Grant succeeded" in out[10]:
                        print "OPS:P: Granting DBA, SAPDBA, CONNECT, RESOURCE permission to " + t_dbuser
			log4erp.write(refresh_id,'POST:P: Granting DBA, SAPDBA, CONNECT, RESOURCE permission to ' + t_dbuser + '')
		else:
                        print "OPS:F: Not able to Grant DBA, SAPDBA, CONNECT, RESOURCE permission to " + t_dbuser
			log4erp.write(refresh_id,'POST:F: Not able to Grant DBA, SAPDBA, CONNECT, RESOURCE permission to ' + t_dbuser + '')
			exit()
		
except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "OPS:F:GERR_2801:Target Hostname unknown - " + argv[1]
        log4erp.write(refresh_id,'POST:F: Target Hostname unknown - ' + argv[1] + ' [Error Code - 2801]')
    elif str(e).strip() == "list index out of range":
        print "OPS:F:GERR_2802:Argument/s missing for the script"
    elif str(e) == "Authentication failed.":
        print "OPS:F:GERR_2803:Authentication failed to the Target Server - " + argv[1]
        log4erp.write(refresh_id,'POST:F:Authentication failed to the Target Server - ' + argv[1] + ' [Error Code - 2803]')
    elif str(e) == "[Errno 110] Connection timed out":
        print "OPS:F:GERR_2804:Target Host Unreachable"
        write(refresh_id,'POST:F:Target Host Unreachable.[Error Code - 2804]')
    elif "getaddrinfo failed" in str(e):
        print "OPS:F:GERR_2805: Please check the target hostname that you have provide"
        log4erp.write(refresh_id,'POST:F: Please check the target hostname that you have provide [Error Code - 2805]')
    elif "[Errno None] Unable to connect to port 22 on" in str(e):
        print "OPS:F:GERR_2806:Host Unreachable or Unable to connect to port 22"
        write(refresh_id,'POST:F: Host Unreachable or Unable to connect to port 22 [Error Code - 2806]')
    else:
        print "OPS:F: " + str(e)
        write(refresh_id,'POST:F: ' + str(e))
