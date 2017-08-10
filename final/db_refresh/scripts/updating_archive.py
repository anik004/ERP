import paramiko
from paramiko import *
from sys import *
import log4erp
from log4erp import *

try:
	if argv[1] == "--u":
		print "Usage: python updating_archive.py <source host> <source user> <source password> <source db sid> <logfile name>"
	else:
		s_host = argv[1]
		s_user = argv[2]
		s_pass = argv[3]
		s_dbsid = argv[4]
		logfile = argv[5] + ".log"
		s_dbuser = "ora" + s_dbsid.lower()

		client = SSHClient()
	        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        	client.connect(s_host,username = s_user,password = s_pass)
		channel = client.invoke_shell()

		cmd = 'sudo su - ' + s_dbuser + ' -c "echo \'ALTER SYSTEM ARCHIVE LOG CURRENT ; \'| sqlplus / as sysdba\"'
                #print cmd
                stdin, stdout, stderr = client.exec_command(cmd, timeout=1000, get_pty=True)
                out = stdout.readlines()
                #print out[11]
                if "System altered." in out[11]:
			print "UPDATING_ARCHIVE:P: Source System archive update have been completed successfully - " + s_host
		        log4erp.write(logfile,"POST:P: Source System archive update have been completed successfully - " + s_host)
		else:
			print "UPDATING_ARCHIVE:F: Source System archive update have been Failed - " + s_host
			log4erp.write(logfile,"POST:F: Source System archive update have been Failed - " + s_host)

		channel.close()
	        client.close()
except Exception as e:
     if str(e) == "[Errno -2] Name or service not known":
                print "UPDATING_ARCHIVE:F:GERR_1301:Source Hostname unknown - " + s_host
                write(logfile,'POST:F: Source Hostname unknown - ' + s_host + ' [Error Code - 1301]')
     elif str(e) == "list index out of range":
                print "UPDATING_ARCHIVE:F:GERR_1302:Argument/s missing for the script"
     elif str(e) == "Authentication failed.":
                print "UPDATING_ARCHIVE:F:GERR_1303:Authentication failed to the Source Server - " + s_host
                write(logfile,'POST:F:Authentication failed to the Source Server - ' + s_host + ' [Error Code - 1303]')
     elif str(e) == "[Errno 110] Connection timed out":
                print "UPDATING_ARCHIVE:F:GERR_1304:Source Host Unreachable"
                write(logfile,'POST:F:Source Host Unreachable.[Error Code - 1304]')
     elif "getaddrinfo failed" in str(e):
                print "UPDATING_ARCHIVE:F:GERR_1305: Please check the Source hostname that you have provide" + s_host
                write(logfile,'POST:F: Please check the Source hostname that you have provide ' + + s_host + ' [Error Code - 1305]')
     elif "[Errno None] Unable to connect to port 22 on" in str(e):
                print "UPDATING_ARCHIVE:F:GERR_1306:Source Host Unreachable or Unable to connect to port 22"
                write(logfile,'POST:F: Source Host Unreachable or Unable to connect to port 22 [Error Code - 1306]')
     elif "invalid decimal" in str(e):
                print "UPDATING_ARCHIVE:F:GERR_1307:Unknown Error:" + str(e)
                write(logfile,'Post:F: Unknown Error:' + str(e) + '[Error Code - 1307]')
     else:
                print "UPDATING_ARCHIVE:F: " + str(e)
		write(logfile,'Post:F: ' + str(e))
