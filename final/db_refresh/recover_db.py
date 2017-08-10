import paramiko
from paramiko import *
from sys import *
from log4erp import *

try:
    if argv[1] == "--u":
        print "Usage: python recover_db.py <Target database host> <Target database root> <Target database root passwd><db sid> <date> <time> <refresh ID>"
    else:
        hostname = argv[1]
        username_db = argv[2]
        password_db = argv[3]
	db_sid = argv[4]
	date= argv[5]
	time = argv[6]
        logfile= argv[7]
	user_db = "ora" + db_sid.lower()

	client = SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname,username = username_db, password = password_db)
	channel = client.invoke_shell()

	for i in range(1,3):
		command = 'sudo su - ' + user_db + ' -c "echo \'recover database using backup controlfile until time \'\\\'' + date + ' ' + time + '\\\'\' \'|  sqlplus / as sysdba\"'
        	print command
	        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        	out = stdout.readlines()
	        status = stdout.channel.recv_exit_status()
#		print out
		print out[9]
		#print out[0].strip()
		if "SQL> Media recovery complete." in out[9]:
			print "DB:P: Target Database has been recovered successfully"
			exit()
		else:# "RECOVER succeeded but OPEN RESETLOGS would get error below" in out[9]:
			command = 'sudo su - ' + user_db + ' -c "echo \'SET AUTORECOVERY ON \' > /oracle/' + db_sid.upper() + '/sapreorg/recover.sql;chmod 777 /oracle/' + db_sid.upper() + '/sapreorg/recover.sql"'
			print command
                        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
                        out = stdout.readlines()
 #                       print out

			command = 'sudo su - ' + user_db + ' -c "echo \'recover database using backup controlfile until cancel \' >> /oracle/' + db_sid.upper() + '/sapreorg/recover.sql;chmod 777 /oracle/' + db_sid.upper() + '/sapreorg/recover.sql"'
			print command
	                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        	        out = stdout.readlines()
#			print out
			command = 'sudo su - ' + user_db + ' -c "echo @/oracle/' + db_sid.upper() + '/sapreorg/recover.sql | sqlplus / as sysdba\"'
	 	        print command
		        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
#			print stdout.readlines()
	


        channel.close()
        client.close()

except Exception as e:
     if str(e) == "[Errno -2] Name or service not known":
                print "DBSTOP:F:GERR_1301:Hostname unknown"
                write(logfile,'PRE:F: Hostname unknown [Error Code - 1301]')
     elif str(e) == "list index out of range":
                print "DBSTOP:F:GERR_1302:Argument/s missing for the script"
     elif str(e) == "Authentication failed.":
                print "DBSTOP:F:GERR_1303:Authentication failed."
                write(logfile,'PRE:F:Authentication failed.[Error Code - 1303]')
     elif str(e) == "[Errno 110] Connection timed out":
                print "DBSTOP:F:GERR_1304:Host Unreachable"
                write(logfile,'PRE:F:Host Unreachable.[Error Code - 1304]')
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
