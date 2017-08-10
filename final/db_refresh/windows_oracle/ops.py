#!/usr/bin/python
# target IP - $1
# database sid - $2
# application sid - $3
# schema passwd - $4
import os
from sys import *
import subprocess
import log4erp
from log4erp import *

# print userapp
# print userdb
try:
#    if argv[1] == "--u":
#        print "usage: python ops.py <Target Database Host> <Target Database SID> <Target Application SID> <Target Schema Password> <Target Sudo User> <Target Sudo Password> <Refresh ID>"
#    else:
                hostname = argv[1]
                username = argv[5]
                password = argv[6]
                user = "ora" + argv[2].lower()
                dbsid = argv[2].upper()
                appsid = argv[3].upper()
                userapp = "OPS\$" + appsid + "ADM"
                userdb = "OPS\$ORA"
                userdb = userdb + dbsid
                refresh_id = argv[7] + ".log"
                syspass = argv[8]
                schema = argv[9]
                location = argv[10]

                # print schema
                # #print type(schema)

                # status="su - " +  user + " -c \"echo \'SELECT USERNAME FROM DBA_USERS;\' | sqlplus system/Welcome2\" | grep -i ops"
                command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "echo \'SELECT USERNAME FROM DBA_USERS;\' | sqlplus system/' + syspass + '"'
                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()
                if command.returncode == 0:
                    print "OPS:I: SELECTING USERNAME FROM DBA_USERS"
                    log4erp.write(refresh_id, 'POST:I: SELECTING USERNAME FROM DBA_USERS ')
                else:
                    print "OPS:F: Not able to select username from DBA_USERS"
                    log4erp.write(refresh_id, 'POST:F: Not able to Select USERNAME from DBA_USERS ')
                    status = stdout.readlines()

                #				command="sudo su - " +  user + " -c \"echo \'CREATE USER " + "\"" + userapp + "\"" + " DEFAULT TABLESPACE SYSTEM TEMPORARY TABLESPACE PSAPTEMP IDENTIFIED EXTERNALLY;\' | sqlplus / as sysdba\" > /dev/null 2>&1"
                command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "echo \'CREATE USER ' + '\"' + userapp + '\"' + ' DEFAULT TABLESPACE SYSTEM TEMPORARY TABLESPACE PSAPTEMP IDENTIFIED EXTERNALLY;\' | sqlplus / as sysdba "'
         #       print command
                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()
                if command.returncode == 0:
                    print "OPS:I: Creating First User " + userapp
                    log4erp.write(refresh_id, 'POST:I: Creating First User ' + userapp + '')
                else:
                    print "OPS:I: Not able to create First User " + userapp
                    log4erp.write(refresh_id, 'POST:I: Not able to create First User ' + userapp + '')

                command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "echo \'CREATE USER ' + '\"' + userdb + '\"' + ' DEFAULT TABLESPACE SYSTEM TEMPORARY TABLESPACE PSAPTEMP IDENTIFIED EXTERNALLY;\' | sqlplus / as sysdba"'
                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()
                if command.returncode == 0:
                    print "OPS:I: Creating Second User " + userdb
                    log4erp.write(refresh_id, 'POST:I: Creating Second User ' + userdb + '')
                else:
                    print "OPS:I: Not able to Second User " + userdb
                    log4erp.write(refresh_id, 'POST:I: Not able to create Second User ' + userdb + '')

                command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "echo \'GRANT DBA, SAPDBA, CONNECT, RESOURCE TO ' + '\"' + userapp + '\"' + ';\' | sqlplus / as sysdba"'
                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()
                if command.returncode == 0:
                    print "OPS:I: Granting DBA, SAPDBA, CONNECT, RESOURCE permission to " + userapp
                    log4erp.write(refresh_id,'POST:I: Granting DBA, SAPDBA, CONNECT, RESOURCE permission to ' + userapp + '')
                else:
                    print "OPS:F: Not able to Grant DBA, SAPDBA, CONNECT, RESOURCE permission to " + userapp
                    log4erp.write(refresh_id,'POST:F: Not able to Grant DBA, SAPDBA, CONNECT, RESOURCE permission to ' + userapp + '')

                command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "echo \'GRANT DBA, SAPDBA, CONNECT, RESOURCE TO ' + '\"' + userdb + '\"' + ';\' | sqlplus / as sysdba"'
                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()
                if command.returncode == 0:
                    print "OPS:I: Granting DBA, SAPDBA, CONNECT, RESOURCE permission to " + userdb
                    log4erp.write(refresh_id,'POST:I: Granting DBA, SAPDBA, CONNECT, RESOURCE permission to ' + userdb + '')
                else:
                    print "OPS:F: Not able to Grant DBA, SAPDBA, CONNECT, RESOURCE permission to " + userdb
                    log4erp.write(refresh_id,'POST:F: Not able to Grant DBA, SAPDBA, CONNECT, RESOURCE permission to ' + userdb + '')

                command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "echo \'GRANT UNLIMITED TABLESPACE TO ' + '\"' + userapp + '\"' + ';\' | sqlplus / as sysdba"'
                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()
                if command.returncode == 0:
                    print "OPS:I: Granting UNLIMITED TABLESPACE to " + userapp
                    log4erp.write(refresh_id, 'POST:I: Granting UNLIMITED TABLESPACE to ' + userapp + '')
                else:
                    print "OPS:F: Not able to Grant UNLIMITED TABLESPACE to " + userapp
                    log4erp.write(refresh_id, 'POST:F: Not able to Grant UNLIMITED TABLESPACE to ' + userapp + '')

                command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "echo \'GRANT UNLIMITED TABLESPACE TO ' + '\"' + userdb + '\"' + ';\' | sqlplus / as sysdba"'
                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()
                if command.returncode == 0:
                    print "OPS:I: Granting UNLIMITED TABLESPACE to " + userdb
                    log4erp.write(refresh_id, 'POST:I: Granting UNLIMITED TABLESPACE to ' + userdb + '')
                else:
                    print "OPS:F: Not able to Grant UNLIMITED TABLESPACE to " + userdb
                    log4erp.write(refresh_id, 'POST:F: Not able to Grant UNLIMITED TABLESPACE to ' + userdb + '')

                #command = "sudo su - " + user + " -c \"echo \'CREATE TABLE " + "\\\"" + userapp + "\\\".SAPUSER" + " (USERID VARCHAR2(256), PASSWD VARCHAR2(256));\' | sqlplus / as sysdba\""
                command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "echo \'CREATE TABLE ' + '\"' + userapp + '\".SAPUSER' + ' (USERID VARCHAR2(256), PASSWD VARCHAR2(256));\' | sqlplus / as sysdba"'
         #       print command
                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()
                if command.returncode == 0:
                    print "OPS:I: Creating Table " + userapp + ".SAPUSER"
                    log4erp.write(refresh_id, 'POST:I: Creating Table ' + userapp + '.SAPUSER ')
                else:
                    print "OPS:F: Not able to Create Table " + userapp + ".SAPUSER"
                    log4erp.write(refresh_id, 'POST:F: Not able to Creating Table ' + userapp + '.SAPUSER ')

                command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "echo \'CREATE TABLE ' + '\"' + userdb + '\".SAPUSER" + " (USERID VARCHAR2(256), PASSWD VARCHAR2(256));\' | sqlplus / as sysdba"'
                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()
                if command.returncode == 0:
                    print "OPS:I: Creating Table " + userdb + ".SAPUSER"
                    log4erp.write(refresh_id, 'POST:I: Creating Table ' + userdb + '.SAPUSER ')
                else:
                    print "OPS:F: Not able to Create Table " + userdb + ".SAPUSER"
                    log4erp.write(refresh_id, 'POST:F: Not able to Creating Table ' + userdb + '.SAPUSER ')


                #command = "sudo su - " + user + " -c \"echo \'INSERT INTO \"" + userapp + "\".SAPUSER VALUES('\\'" + schema.strip() + "\\'','\\'" + argv[4] + "\\'');'\" > /home/" + argv[5].lower() + "/insert.sql"
                command = "c:\python27\python.exe " + location + "\wmiexec.py " + username.strip() + ':' + password.strip() + '@' + hostname + " \"echo \'INSERT INTO \"" + userapp + "\".SAPUSER VALUES('\\'" + schema.strip() + "\\'','\\'" + argv[4] + "\\'');'\" | sqlplus / as sysdba"
	#	print command
                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()
                if command.returncode == 0:
                        print "OPS:I: Alter values in table \"" + userapp + "\".SAPUSER"
                        log4erp.write(refresh_id, 'POST:I: Inserting values in table \"' + userapp + '\".SAPUSER ')
                else:
                        print "OPS:F: Not able to Insert values in table \"" + userapp + "\".SAPUSER"
                        log4erp.write(refresh_id, 'POST:F: Not able to Insert values in table \"' + userapp + '\".SAPUSER ')

                command = "c:\python27\python.exe " + location + "\wmiexec.py " + username.strip() + ':' + password.strip() + '@' + hostname + " \"echo \'INSERT INTO \"" + userdb + "\".SAPUSER VALUES('\\'" + schema.strip() + "\\'','\\'" + argv[4] + "\\'');'\" | sqlplus / as sysdba"
                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()
                if command.returncode == 0:
                        print "OPS:I: Alter values in table " + userdb + "\".SAPUSER"
                        log4erp.write(refresh_id, 'POST:I: Inserting values in table ' + userdb + '\".SAPUSER ')
                else:
                        print "OPS:F: Not able to Inser values in table" + userdb + "\".SAPUSER"
                        log4erp.write(refresh_id, 'POST:F: Not able to Insert values in table ' + userdb + '\".SAPUSER ')

                command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "echo \'ALTER USER \"' + userapp + '\" TEMPORARY TABLESPACE PSAPTEMP;\' | sqlplus / as sysdba"'
                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()

                command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "echo \'ALTER USER \"' + userdb + '\" TEMPORARY TABLESPACE PSAPTEMP;\' | sqlplus / as sysdba"'
                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()

                command = 'c:\python27\python.exe ' + location + '\wmiexec.py ' + username.strip() + ':' + password.strip() + '@' + hostname + ' "echo \'commit;\' | sqlplus / as sysdba"'
                command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
                out, err = command.communicate()
                if command.returncode == 0:
                    print "OPS:P: Commited all the changes in the Database"
                    log4erp.write(refresh_id, 'POST:P: Commited all the changes in the Database ')
                else:
                    print "OPS:F: Not able to Commit all the changes in the Database"
                    log4erp.write(refresh_id, 'POST:F: Not able to Commit all the changes in the Database ')


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
