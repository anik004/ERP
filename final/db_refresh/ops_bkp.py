#!/usr/bin/python
# target IP - $1
# database sid - $2
# application sid - $3
# schema passwd - $4
import paramiko
from sys import *
from paramiko import *
from log4erp import *
import log4erp
import os

# print userapp
# print userdb
try:
#    if argv[1] == "--u":
#        print "usage: python ops.py <Target Database Host> <Target Database SID> <Target Application SID> <Target Schema Password> <Target Sudo User> <Target Sudo Password> <Refresh ID>"
#    else:
        t_db_user = "ora" + argv[2].lower()
        t_dbsid = argv[2].upper()
	t_appsid = argv[3].upper()
        t_userapp = "OPS\$" + t_appsid + "ADM"
        userdb = "OPS\$ORA"
        t_userdb = userdb + t_dbsid
        refresh_id = argv[7] + ".log"
	syspass = argv[8]

        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(argv[1], username=argv[5], password=argv[6])
        channel = client.invoke_shell()

        print "OPS:I: Connection established Successfully (Hostname -" + argv[1] + ")"
        log4erp.write(refresh_id, 'POST:I: Connection established Successfully (Hostname -' + argv[1] + ')')

        print "OPS:I: Checking User Existence in target server (Hostname -" + argv[1] + ")"
        log4erp.write(refresh_id, 'POST:I: Checking User Existence in target server (Hostname -' + argv[1] + ')')

	command = 'sudo su - ' + user + ' -c \'echo "select username from dba_users;" | sqlplus / as sysdba\''
	print command
        command = "sudo su - " + user + " -c 'exit'; echo $?"
        stdin, stdout, stderr = client.exec_command(command, timeout=60, get_pty=True)
        status = stdout.readline()[0].rstrip()
	print command
        if status != "0":
            print "OPS:F: user " + user + " does not exist in target server (Hostname -" + argv[1] + ")"
            log4erp.write(refresh_id,'POST:F: User ' + user + ' does not exist in target server (Hostname -' + argv[1] + ')')
            exit(0)
        else:
            print "OPS:I: User " + user + " exist in target server (Hostname -" + argv[1] + ")"
            log4erp.write(refresh_id, 'POST:I: User ' + user + ' exist in target server (Hostname -' + argv[1] + ')')
            # schema = 'su - ' + user + ' -c \'echo $dbs_ora_schema\''
            schema = 'sudo su - ' + user + ' -c \'echo $dbs_ora_schema\''
            stdin, stdout, stderr = client.exec_command(schema, timeout=1000, get_pty=True)
	    schema = stdout.readlines()
            if stdout.channel.recv_exit_status() == 0:
                print "OPS:I: Fetching the Schema user name in target server (Hostname -" + argv[1] + ")"
                log4erp.write(refresh_id,'POST:I: Fetching the Schema user name in target server (Hostname -' + argv[1] + ')')
                # print schema[0]
                # #print type(schema)

                # status="su - " +  user + " -c \"echo \'SELECT USERNAME FROM DBA_USERS;\' | sqlplus system/Welcome2\" | grep -i ops"
                status = "sudo su - " + user + " -c \"echo \'SELECT USERNAME FROM DBA_USERS;\' | sqlplus system/" + syspass + "\" | grep -i ops"
                stdin, stdout, stderr = client.exec_command(status, timeout=1000, get_pty=True)
                if stdout.channel.recv_exit_status() == 0:
                    print "OPS:I: SELECTING USERNAME FROM DBA_USERS"
                    log4erp.write(refresh_id, 'POST:I: SELECTING USERNAME FROM DBA_USERS ')
                else:
                    print "OPS:F: Not able to select username from DBA_USERS"
                    log4erp.write(refresh_id, 'POST:F: Not able to Select USERNAME from DBA_USERS ')
                status = stdout.readlines()

                #				command="sudo su - " +  user + " -c \"echo \'CREATE USER " + "\"" + userapp + "\"" + " DEFAULT TABLESPACE SYSTEM TEMPORARY TABLESPACE PSAPTEMP IDENTIFIED EXTERNALLY;\' | sqlplus / as sysdba\" > /dev/null 2>&1"
                command = "sudo su - " + user + " -c \"echo \'CREATE USER " + "\"" + userapp + "\"" + " DEFAULT TABLESPACE SYSTEM TEMPORARY TABLESPACE PSAPTEMP IDENTIFIED EXTERNALLY;\' | sqlplus / as sysdba\""
                print command
                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
                #print stdout.readlines()
                status = stdout.channel.recv_exit_status()
                #print status
                if status == 0:
                    print "OPS:I: Creating First User " + userapp
                    log4erp.write(refresh_id, 'POST:I: Creating First User ' + userapp + '')
                else:
                    print "OPS:I: Not able to create First User " + userapp
                    log4erp.write(refresh_id, 'POST:I: Not able to create First User ' + userapp + '')

                command = "sudo su - " + user + " -c \"echo \'CREATE USER " + "\"" + userdb + "\"" + " DEFAULT TABLESPACE SYSTEM TEMPORARY TABLESPACE PSAPTEMP IDENTIFIED EXTERNALLY;\' | sqlplus / as sysdba\""
                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
		print command
                if stdout.channel.recv_exit_status() == 0:
                    print "OPS:I: Creating Second User " + userdb
                    log4erp.write(refresh_id, 'POST:I: Creating Second User ' + userdb + '')
                else:
                    print "OPS:I: Not able to Second User " + userdb
                    log4erp.write(refresh_id, 'POST:I: Not able to create Second User ' + userdb + '')

                command = "sudo su - " + user + " -c \"echo \'GRANT DBA, SAPDBA, CONNECT, RESOURCE TO " + "\"" + userapp + "\"" + ";\' | sqlplus / as sysdba\""
                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
		print command
                if stdout.channel.recv_exit_status() == 0:
                    print "OPS:I: Granting DBA, SAPDBA, CONNECT, RESOURCE permission to " + userapp
                    log4erp.write(refresh_id,'POST:I: Granting DBA, SAPDBA, CONNECT, RESOURCE permission to ' + userapp + '')
                else:
                    print "OPS:F: Not able to Grant DBA, SAPDBA, CONNECT, RESOURCE permission to " + userapp
                    log4erp.write(refresh_id,'POST:F: Not able to Grant DBA, SAPDBA, CONNECT, RESOURCE permission to ' + userapp + '')

                command = "sudo su - " + user + " -c \"echo \'GRANT DBA, SAPDBA, CONNECT, RESOURCE TO " + "\"" + userdb + "\"" + ";\' | sqlplus / as sysdba\""
                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
		print command
                if stdout.channel.recv_exit_status() == 0:
                    print "OPS:I: Granting DBA, SAPDBA, CONNECT, RESOURCE permission to " + userdb
                    log4erp.write(refresh_id,'POST:I: Granting DBA, SAPDBA, CONNECT, RESOURCE permission to ' + userdb + '')
                else:
                    print "OPS:F: Not able to Grant DBA, SAPDBA, CONNECT, RESOURCE permission to " + userdb
                    log4erp.write(refresh_id,'POST:F: Not able to Grant DBA, SAPDBA, CONNECT, RESOURCE permission to ' + userdb + '')

                command = "sudo su - " + user + " -c \"echo \'GRANT UNLIMITED TABLESPACE TO " + "\"" + userapp + "\"" + ";\' | sqlplus / as sysdba\""
                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
		print command
                if stdout.channel.recv_exit_status() == 0:
                    print "OPS:I: Granting UNLIMITED TABLESPACE to " + userapp
                    log4erp.write(refresh_id, 'POST:I: Granting UNLIMITED TABLESPACE to ' + userapp + '')
                else:
                    print "OPS:F: Not able to Grant UNLIMITED TABLESPACE to " + userapp
                    log4erp.write(refresh_id, 'POST:F: Not able to Grant UNLIMITED TABLESPACE to ' + userapp + '')

                command = "sudo su - " + user + " -c \"echo \'GRANT UNLIMITED TABLESPACE TO " + "\"" + userdb + "\"" + ";\' | sqlplus / as sysdba\""
                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
		print command
                if stdout.channel.recv_exit_status() == 0:
                    print "OPS:I: Granting UNLIMITED TABLESPACE to " + userdb
                    log4erp.write(refresh_id, 'POST:I: Granting UNLIMITED TABLESPACE to ' + userdb + '')
                else:
                    print "OPS:F: Not able to Grant UNLIMITED TABLESPACE to " + userdb
                    log4erp.write(refresh_id, 'POST:F: Not able to Grant UNLIMITED TABLESPACE to ' + userdb + '')

                #command = "sudo su - " + user + " -c \"echo \'CREATE TABLE " + "\\\"" + userapp + "\\\".SAPUSER" + " (USERID VARCHAR2(256), PASSWD VARCHAR2(256));\' | sqlplus / as sysdba\""
                command = "sudo su - " + user + " -c \"echo \'CREATE TABLE " + "\"" + userapp + "\".SAPUSER" + " (USERID VARCHAR2(256), PASSWD VARCHAR2(256));\' | sqlplus / as sysdba\""
                print command
                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
                status = stdout.channel.recv_exit_status()
                #print status
                if status == 0:
                    print "OPS:I: Creating Table " + userapp + ".SAPUSER"
                    log4erp.write(refresh_id, 'POST:I: Creating Table ' + userapp + '.SAPUSER ')
                else:
                    print "OPS:F: Not able to Create Table " + userapp + ".SAPUSER"
                    log4erp.write(refresh_id, 'POST:F: Not able to Creating Table ' + userapp + '.SAPUSER ')

                command = "sudo su - " + user + " -c \"echo \'CREATE TABLE " + "\"" + userdb + "\".SAPUSER" + " (USERID VARCHAR2(256), PASSWD VARCHAR2(256));\' | sqlplus / as sysdba\""
                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
                print command
                if stdout.channel.recv_exit_status() == 0:
                    print "OPS:I: Creating Table " + userdb + ".SAPUSER"
                    log4erp.write(refresh_id, 'POST:I: Creating Table ' + userdb + '.SAPUSER ')
                else:
                    print "OPS:F: Not able to Create Table " + userdb + ".SAPUSER"
                    log4erp.write(refresh_id, 'POST:F: Not able to Creating Table ' + userdb + '.SAPUSER ')

                command = "sudo su - " + user + " -c \"touch /home/" + user + "/insert.sql\""
                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
                print command

                #command = "sudo su - " + user + " -c \"echo \'INSERT INTO \"" + userapp + "\".SAPUSER VALUES('\\'" + schema[0].strip() + "\\'','\\'" + argv[4] + "\\'');'\" > /home/" + argv[5].lower() + "/insert.sql"
		command = "sudo su - " + user + " -c \"echo \'INSERT INTO \"" + userapp + "\".SAPUSER VALUES('\\'" + schema[0].strip() + "\\'','\\'" + argv[4] + "\\'');'\" > /tmp/insert.sql"
		print command
                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
                #print command
                print command
                if stdout.channel.recv_exit_status() == 0:
                    #command = "sudo mv /home/" + argv[5].lower() + "/insert.sql" + " /home/" + user + "/insert.sql"
		    command = "sudo mv /tmp/insert.sql" + " /home/" + user + "/insert.sql"	
                    stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
                    if stdout.channel.recv_exit_status() == 0:
                        print "OPS:I: Alter values in table \"" + userapp + "\".SAPUSER"
                        log4erp.write(refresh_id, 'POST:I: Inserting values in table \"' + userapp + '\".SAPUSER ')
                else:
                    print "OPS:F: Not able to Insert values in table \"" + userapp + "\".SAPUSER"
                    log4erp.write(refresh_id, 'POST:F: Not able to Insert values in table \"' + userapp + '\".SAPUSER ')

                command = "sudo su - " + user + " -c \"echo \'@/home/" + user + "/insert.sql\'" + " | sqlplus / as sysdba\" | grep -i created"
                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
                print command

                command = "sudo su - " + user + " -c \"touch /home/" + user + "/insert.sql\""
                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
                print command

                #command = "sudo su - " + user + " -c \"echo \'INSERT INTO \"" + userdb + "\".SAPUSER VALUES('\\'" + schema[0].strip() + "\\'','\\'" + argv[4] + "\\'');'\" > /home/" + argv[5] + "/insert.sql"
		command = "sudo su - " + user + " -c \"echo \'INSERT INTO \"" + userdb + "\".SAPUSER VALUES('\\'" + schema[0].strip() + "\\'','\\'" + argv[4] + "\\'');'\" > /tmp/insert.sql"
                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
                print command
                if stdout.channel.recv_exit_status() == 0:
                    #command = "sudo mv /home/" + argv[5].lower() + "/insert.sql" + " /home/" + user + "/insert.sql"
		    command = "sudo mv /tmp/insert.sql" + " /home/" + user + "/insert.sql"
                    if stdout.channel.recv_exit_status() == 0:
                        print "OPS:I: Alter values in table " + userdb + "\".SAPUSER"
                        log4erp.write(refresh_id, 'POST:I: Inserting values in table ' + userdb + '\".SAPUSER ')
                else:
                    print "OPS:F: Not able to Inser values in table" + userdb + "\".SAPUSER"
                    log4erp.write(refresh_id, 'POST:F: Not able to Insert values in table ' + userdb + '\".SAPUSER ')
                command = "sudo su - " + user + " -c \"echo \'@/home/" + user + "/insert.sql\'" + " | sqlplus / as sysdba\" | grep -i created"
                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
                print command

                command = "sudo rm -rf " + "/home/" + user + "/insert.sql"
                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
                print command

                command = "sudo su - " + user + " -c \"echo \'ALTER USER \"" + userapp + "\" TEMPORARY TABLESPACE PSAPTEMP;\' | sqlplus / as sysdba\""
                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
                print command
                result = stdout.readlines()

                command = "sudo su - " + user + " -c \"echo \'ALTER USER \"" + userdb + "\" TEMPORARY TABLESPACE PSAPTEMP;\' | sqlplus / as sysdba\""
                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
                print command
                result = stdout.readlines()

                command = "sudo su - " + user + " -c \"echo \'commit;\' | sqlplus / as sysdba\""
                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
                print command
                if stdout.channel.recv_exit_status() == 0:
                    print "OPS:P: Commited all the changes in the Database"
                    log4erp.write(refresh_id, 'POST:P: Commited all the changes in the Database ')
                else:
                    print "OPS:F: Not able to Commit all the changes in the Database"
                    log4erp.write(refresh_id, 'POST:F: Not able to Commit all the changes in the Database ')

        channel.close()
        client.close()

except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "OPS:F:GERR_2201:Hostname unknown"
        log4erp.write(refresh_id, 'POST:F: Hostname unknown [Error Code - 2201]')
    elif str(e).strip() == "list index out of range":
        print "OPS:F:GERR_2202:Argument/s missing for OPS script"
    elif str(e) == "Authentication failed.":
        print "OPS:F:GERR_2203:Authentication failed."
        log4erp.write(refresh_id, 'POST:F:Authentication failed[Error Code - 2203]')
    elif str(e) == "[Errno 110] Connection timed out":
        print "OPS:F:GERR_2204::Host Unreachable"
	write(refresh_id,'POST:F:Host Unreachable.[Error Code - 2204]')	
    elif "getaddrinfo failed" in str(e):
        print "OPS:F:GERR_2205: Please check the hostname that you have provide"
        log4erp.write(refresh_id, 'POST:F: Please check the hostname that you have provide [Error Code - 2205]')
    elif "[Errno None] Unable to connect to port 22 on" in str(e):
        print "OPS:F:GERR_2206:Host Unreachable or Unable to connect to port 22"
        write(refresh_id,'POST:F: Host Unreachable or Unable to connect to port 22 [Error Code - 2206]')
    else:
        print "OPS:F: " + str(e)
