#!/usr/bin/sh

# source IP - $1
# database sid - $2
# target IP - $3
# database sid - $4
# source application sid - $5
import paramiko
from sys import *
from paramiko import *
import log4erp
import subprocess

try:
    if argv[1] == "--u":
        print "usage: python temptable.py <Source DB Host> <Source Sudo user> <source sudo pass> <Source DB SID> <Target DB Host> <target sudo user> <target sudo pass>  <Target Application sid> <Target DB sid> <Refersh ID> "
    else:
	s_host = argv[1]
	s_user = argv[2]
	s_pass = argv[3]
	s_dbsid = argv[4]
	t_host = argv[5]
	t_user = argv[6]
	t_pass  = argv[7]
	t_appsid = argv[8]
	t_dbsid = argv[9]
        refresh_id = argv[10] + ".log"
		
        print "TEMPTABLE:I: Establishing Connection on source server ( Hostname - " + argv[1] + " )"
        log4erp.write(refresh_id,"POST:I: Establishing Connection on source server ( Hostname - " + argv[1] + " )")
		
        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect( argv[1],username = argv[2], password = argv[3])
        channel = client.invoke_shell()
		
        print "TEMPTABLE:I: Connection established successfully on source server ( Hostname - " + argv[1] + " )"
        log4erp.write(refresh_id,"POST:I: Connection established successfully on source server ( Hostname - " + argv[1] + " )")

        print "TEMPTABLE:I: Establishing Connection on target server ( Hostname - " + argv[5] + " )"
        log4erp.write(refresh_id,"POST:I: Establishing Connection on target server ( Hostname - " + argv[5] + " )")
		
        client1 = SSHClient()
        client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client1.connect( argv[5],username = argv[6], password = argv[7])
        channel1 = client1.invoke_shell()
		
        print "TEMPTABLE:I: Connection established successfully on target server ( Hostname - " + argv[5] + " )"
        log4erp.write(refresh_id,"POST:I: Connection established successfully on target server ( Hostname - " + argv[5] + " )")

        s_dbuser="ora" + argv[4].lower()
        t_dbuser="ora" + argv[9].lower()
	
	cmd = "sudo su - " +  t_dbuser + " -c \"echo \'Select contents from dba_tablespaces where tablespace_name='\\'PSAPTEMP\\'' ; ' | sqlplus / as sysdba\""
	print cmd
	stdin, stdout, stderr = client1.exec_command(cmd, timeout=1000, get_pty=True)
	out = stdout.readlines()
	print out[12]
	if "PERMANENT" in out[12]:
		print "PSAPTEMP is permanent"
		exit()
	else:
	        print "TEMPTABLE:I: Getting temporary tablespace and associated datafile details on source server ( Hostname - " + argv[1] + " )"
        	log4erp.write(refresh_id,"POST:I: Getting temporary tablespace and associated datafile details on source server ( Hostname - " + argv[1] + " )")
	        path="sudo su - " +  s_dbuser + " -c \"echo \'select tablespace_name,file_name from DBA_TEMP_FILES;\' | sqlplus / as sysdba\" | grep \".data\" | grep -v \"asdasd\""
        	print path
	        stdin, stdout, stderr = client.exec_command(path, timeout=1000, get_pty=True)
        	path1 = stdout.readlines()
		print path1
        	print "TEMPTABLE:I: Fetched details of temporary tablespace and associated datafiles successfully on source server ( Hostname - " + argv[1] + " )"
	        log4erp.write(refresh_id,"POST:I: Fetched details of temporary tablespace and associated datafiles successfully on target server ( Hostname - " + argv[1] + " )")
        	for source_path in path1:
	        	actual_path=source_path.strip().replace(s_dbsid.upper(),t_dbsid.upper())
        	        command = "ls " + actual_path + " >&1 /dev/null"
                	print command
	                stdin, stdout, stderr = client1.exec_command(command, timeout=1000, get_pty=True)
        	        status = stdout.channel.recv_exit_status()

			if status == 0:
	                	print "TEMPTABLE:I: Adding Tempfile \'" + actual_path + "' in Temporary Tablespace on target server ( Hostname - " + argv[3] + " )"
				command = "echo \"ALTER TABLESPACE PSAPTEMP ADD TEMPFILE \'" + actual_path + "\' SIZE 2000M REUSE AUTOEXTEND ON next 200m maxsize 16G;\" > /home/oradrp/sql1.sql; chmod 777 /home/oradrp/sql1.sql"
				print command
				stdin, stdout, stderr = client1.exec_command(command, timeout=1000, get_pty=True)
	                        status = stdout.channel.recv_exit_status()

				command="sudo su - " + t_dbuser + " -c \"echo \'@/home/" + t_dbuser + "/sql1.sql;\' | sqlplus / as sysdba | grep -i -e 'Tablespace altered.' -e 'already part of database' | grep -v '#'\""
				print command
				stdin, stdout, stderr = client1.exec_command(command, timeout=1000, get_pty=True)
		                status = stdout.readlines()
				print status
 		                status = status[0].strip()
				if status == "Tablespace altered.":
					print "TEMPTABLE:P: Tempfile " + actual_path + " added successfully in Temporary Tablespace on target server ( Hostname - " + argv[3] + " )"
					log4erp.write(refresh_id,"POST:P: Tempfile " + actual_path + " added successfully in Temporary Tablespace on target server ( Hostname - " + argv[3] + " )")
				elif status == "already part of database":
					print "TEMPTABLE:P: Tempfile " + actual_path + " already there in Temporary Tablespace on target server ( Hostname - " + argv[3] + " )"
					log4erp.write(refresh_id,"POST:P: Tempfile " + actual_path + " already there in Temporary Tablespace on target server ( Hostname - " + argv[3] + " )")
				else:
					print "TEMPTABLE:F: Adding Tempfile " + actual_path + " to Temporary tablespace failed"
					log4erp.write(refresh_id,"POST:F: Adding Tempfile " + actual_path + " to Temporary tablespace failed")
			
	channel.close()
        channel1.close()
		
			
        client.close()
        client1.close()
			
            #print "TEMPTABLE:I: Connection closed successfully on target server ( Hostname - " + argv[3] + " )"
            #log4erp.write(refresh_id,"POST:I: Connection closed successfully on target server ( Hostname - " + argv[3] + " )")

except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "TEMPTABLE:F:GERR_2101:Hostname unknown"
        log4erp.write(refresh_id,'POST:F: Hostname unknown [Error Code - 2101]')
    elif str(e).strip() == "list index out of range":
    	print "TEMPTABLE:F:GERR_2102:Argument/s missing for TempTable script"
    elif str(e) == "Authentication failed.":
        print "TEMPTABLE:F:GERR_2103:Authentication failed."
    	log4erp.write(refresh_id,'POST:F:Authentication failed[Error Code - 2103]')
    elif str(e) == "[Errno 110] Connection timed out":
        print "TEMPTABLE:F:GERR_2104:Host Unreachable"
	write(refresh_id,'POST:F:Host Unreachable.[Error Code - 2104]')
    elif "getaddrinfo failed" in str(e):
        print "TEMPTABLE:F:GERR_2105: Please check the hostname that you have provide"
        log4erp.write(refresh_id,'POST:F: Please check the hostname that you have provide [Error Code - 2105]')
    elif "[Errno None] Unable to connect to port 22 on" in str(e):
        print "TEMPTABLE:F:GERR_2106:Host Unreachable or Unable to connect to port 22"
        write(refresh_id,'POST:F: Host Unreachable or Unable to connect to port 22 [Error Code - 2106]')
    else:
        print "TEMPTABLE:F: " + str(e)
