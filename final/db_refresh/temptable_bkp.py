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
#    if argv[1] == "--u":
#        print "usage: python temptable.py <Source DB Host> <Source DB sid> <Target DB Host> <Target DB sid> <Target Application sid> <Source Sudo user> <source sudo pass> <target sudo user> <target sudo pass> <Refersh ID> <Instance ID>"
#    else:
        refresh_id = argv[10] + ".log"
		
        print "TEMPTABLE:I: Establishing Connection on source server ( Hostname - " + argv[1] + " )"
        log4erp.write(refresh_id,"POST:I: Establishing Connection on source server ( Hostname - " + argv[1] + " )")
		
        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect( argv[1],username = argv[6], password = argv[7])
        channel = client.invoke_shell()
		
        print "TEMPTABLE:I: Connection established successfully on source server ( Hostname - " + argv[1] + " )"
        log4erp.write(refresh_id,"POST:I: Connection established successfully on source server ( Hostname - " + argv[1] + " )")

        print "TEMPTABLE:I: Establishing Connection on target server ( Hostname - " + argv[3] + " )"
        log4erp.write(refresh_id,"POST:I: Establishing Connection on target server ( Hostname - " + argv[3] + " )")
		
        client1 = SSHClient()
        client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client1.connect( argv[3],username = argv[8], password = argv[9])
        channel1 = client1.invoke_shell()
		
        print "TEMPTABLE:I: Connection established successfully on target server ( Hostname - " + argv[3] + " )"
        log4erp.write(refresh_id,"POST:I: Connection established successfully on target server ( Hostname - " + argv[3] + " )")

        user_source_db="ora" + argv[2].lower()
        user_target_db="ora" + argv[4].lower()
        upper_source=argv[2].upper()
        upper_target=argv[4].upper()

        #print "TEMPTABLE:I: Starting SAP on target server ( Hostname - " + argv[3] + " )"
        #log4erp.write(refresh_id,"POST:I: Starting SAP on target server ( Hostname - " + argv[1] + " )")
        #command = "python sapstartapp.py " + argv[3] + " " + argv[8] + " " + argv[9] + " " + argv[5] + " " + argv[11] + " " + argv[3] + " " + argv[10]# + " > /dev/null 2>&1"
        #command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        #out, err = command.communicate()
	#print out.strip()
	status = 0
        if status ==0:
            #log4erp.write(refresh_id,"POST:I: SAP started on target server ( Hostname - " + argv[3] + " )")
            #log4erp.write(refresh_id,"POST:I: SAP started on target server ( Hostname - " + argv[3] + " )")

            print "TEMPTABLE:I: Getting temporary tablespace and associated datafile details on source server ( Hostname - " + argv[1] + " )"
            log4erp.write(refresh_id,"POST:I: Getting temporary tablespace and associated datafile details on source server ( Hostname - " + argv[1] + " )")
            path="sudo su - " +  user_source_db + " -c \"echo \'select tablespace_name,file_name from DBA_TEMP_FILES;\' | sqlplus / as sysdba\" | grep \".data\" | grep -v \"asdasd\""
            print path
            stdin, stdout, stderr = client.exec_command(path, timeout=1000, get_pty=True)
            path1 = stdout.readlines()
	    print path1
            print "TEMPTABLE:I: Fetched details of temporary tablespace and associated datafiles successfully on source server ( Hostname - " + argv[1] + " )"
            log4erp.write(refresh_id,"POST:I: Fetched details of temporary tablespace and associated datafiles successfully on target server ( Hostname - " + argv[1] + " )")
            for source_path in path1:
                actual_path=source_path.strip().replace(upper_source,upper_target)
                command = "sudo ls " + actual_path + " >&1 /dev/null"
                #print command
                stdin, stdout, stderr = client1.exec_command(command, timeout=1000, get_pty=True)
                status = stdout.channel.recv_exit_status()

                if status == 0:
                    print "TEMPTABLE:I: Adding Tempfile \'" + actual_path + "' in Temporary Tablespace on target server ( Hostname - " + argv[3] + " )"
		    command = "echo \"ALTER TABLESPACE PSAPTEMP ADD TEMPFILE \'" + actual_path + "\' SIZE 2000M REUSE;\" > /home/soladm/sql1.sql; chmod 777 /home/soladm/sql1.sql"
		    print command
		    command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                    out, err = command.communicate()

# -----------------------------------------------------------------------------------------------------------------------------------------------------
		    port = 22
		    t_host = argv[3]
		    t_user = argv[8]
		    t_pass = argv[9]
		    localpath = "/home/soladm/sql1.sql"
		    filepath = "/home/" + user_target_db + "/sql1.sql"
		    print filepath
		    transport1 = paramiko.Transport((t_host, port))
	            transport1.connect(username=t_user, password=t_pass)
	            sftp1 = paramiko.SFTPClient.from_transport(transport1)
	            sftp1.put(localpath, filepath)
# -----------------------------------------------------------------------------------------------------------------------------------------------------

                    command="sudo su - " + user_target_db + " -c \"echo \'@/home/" + user_target_db + "/sql1.sql;\' | sqlplus / as sysdba | grep -i -e 'Tablespace altered.' -e 'already part of database' | grep -v '#'\""
		    print command
                    stdin, stdout, stderr = client1.exec_command(command, timeout=1000, get_pty=True)
                    status = stdout.readlines()
		    #print status
		    #print type(status)
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
                #print "TEMPTABLE:I: Closing connection on source server ( Hostname - " + argv[1] + " )"
                #log4erp.write(refresh_id,"POST:I: Closing connection on source server ( Hostname - " + argv[1] + " )")
			
            channel.close()
            channel1.close()
		
            #print "TEMPTABLE:I: Connection closed successfully on source server ( Hostname - " + argv[1] + " )"
            #log4erp.write(refresh_id,"POST:I: Connection closed successfully on source server ( Hostname - " + argv[1] + " )")

            #print "TEMPTABLE:I: Closing connection on target server ( Hostname - " + argv[3] + " )"
            #log4erp.write(refresh_id,"POST:I: Closing connection on target server ( Hostname - " + argv[3] + " )")
			
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
