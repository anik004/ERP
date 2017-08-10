import paramiko
from paramiko import *
from sys import *
from log4erp import *

try:
    if argv[1] == "--u":
        print "Usage: python recover_db.py <Target database host> <Target database root> <Target database root passwd><db sid> <date> <time> <Source Host> <Source Sudo User> <Source Passwd> <source dbsid> <refresh ID>"
    else:
        hostname = argv[1]
        username_db = argv[2]
        password_db = argv[3]
	db_sid = argv[4]
	date= argv[5]
	time = argv[6]
	s_host = argv[7]
	s_user = argv[8]
	s_pass = argv[9]
	s_dbsid = argv[10]
        logfile= argv[11] + ".log"
	s_dbuser = "ora" + s_dbsid.lower()

	user_db = "ora" + db_sid.lower()

	client = SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname,username = username_db, password = password_db)
	channel = client.invoke_shell()

	for i in range(1,5):
		command = 'sudo su - ' + user_db + ' -c "echo \'recover database using backup controlfile until time \'\\\'' + date + ' ' + time + '\\\'\' \'|  sqlplus / as sysdba\"'
        	print command
	        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        	out = stdout.readlines()
	        status = stdout.channel.recv_exit_status()
		print out
		print out[9]
		#print out[0].strip()
		if "SQL> Media recovery complete." in out[9]:
			print "DB:P: Target Database has been recovered successfully"
			exit()
		if "RECOVER succeeded but OPEN RESETLOGS would get error below" in out[9]:
			client1 = SSHClient()
			client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			client1.connect(s_host,username = s_user, password = s_pass)
			channel1 = client1.invoke_shell()

			cmd = 'sudo su - ' + s_dbuser + ' -c "echo \'ALTER SYSTEM ARCHIVE LOG CURRENT ; \'| sqlplus / as sysdba\"'
			print cmd
			stdin, stdout, stderr = client1.exec_command(cmd, timeout=1000, get_pty=True)
			out = stdout.readlines()
			print out[11]
			if "System altered." in out[11]:
				cmd = 'sudo su - ' + s_dbuser + ' -c "echo \'archive log list \'| sqlplus / as sysdba\"'
				print cmd
			        stdin, stdout, stderr = client1.exec_command(cmd, timeout=1000, get_pty=True)
				out = stdout.readlines()
				out = out[15].split()
				num = out[3]
				num = int(num) -1
				num = str(num)
				cmd = "sudo ls /oracle/" + s_dbsid.upper() + "/oraarch/*" + num + "*"
				print cmd
				stdin, stdout, stderr = client1.exec_command(cmd, timeout=1000, get_pty=True)
        	                out = stdout.readlines()
				out = "".join(out)
				out = out.encode('UTF8')
#				each = "/oracle/" + s_dbsid.upper() + "/oraarch/" + out.split()
#				print each
				cmd = "expect scparch.exp " + s_host + " " + s_user + " " + s_pass + " " + s_dbsid.upper() + " " + hostname + " " + username_db + " " + password_db + " " + db_sid.upper() + " " + out.strip()
				print cmd
		                command=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
        		        out, err = command.communicate()
          #     		 print out
				cmd = "python arch_change.py"
				print cmd
				command=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
                                out, err = command.communicate()

				cmd = "python permission.py"
				print cmd
				command=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
                                out, err = command.communicate()

			channel1.close()
			client1.close()
			 

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
