from __future__ import division
from paramiko import *
from sys import *
import re
import paramiko
from log4erp import *

def cleanup(hostname, username, password, database_sid,logfile):

    user = "ora" + database_sid.lower()
    path_array = []
    total= 0


    try:
        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect( hostname,username = username, password = password)
        channel = client.invoke_shell()

	command = "ls /oracle/" + database_sid.upper() + " >&1 /dev/null"
#        print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        status = stdout.channel.recv_exit_status()
#       print status
#       print stdout.readlines()

        if status != 0:
            print "CLEANUP:F:Provided input for the database SID ( " + database_sid + " ) in " + hostname + " host is incorrect"
            write(logfile,"PRE:F:Provided input for the database SID ( " + database_sid + " ) in " + hostname + " host is incorrect")
            exit()

        sftp_client = client.open_sftp()
        command = '/oracle/' + database_sid.upper() + '/sapreorg/control_script_' + database_sid.upper() + '.sql' # | grep -i "sapdata*"' # variable IN
        remote_file = sftp_client.open(command)
        remote_file = list(set(remote_file))
        for line in remote_file:
            paths = ""
            if "ALTER" not in line:
                if re.search("sapdata", line):
                    directory = line.split("/")
                    for dire in directory:
                        if "sapdata" in dire:
                            paths = str(paths) + "/" + str(dire)
                            break
                        else:
                            paths = str(paths) + "/" + str(dire)
                    path_array.append(paths[4:])
        path_array = list(set(path_array))
        for each in path_array:
            command = "rm -rf " + each + "/*"
	    print command
            stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
            status = stdout.channel.recv_exit_status()
	    #print status
            if status == 0 or status == 1:
                print "CLEANUP:P:cleanup of " + each + " in Target Server is successful"
		log = 'PRE:P: CLEANUP of ' + each + ' in Target Server is successful'
		write (logfile, log)
	    else:
		print "CLEANUP:F::cleanup of " + each + " in Target Server is unsuccessful"
		log = 'PRE:P: CLEANUP of ' + each + ' in Target Server is unsuccessful'
		write (logfile, log)
        command = 'rm -rf /oracle/' + database_sid.upper() + '/sapreorg/sql.sql'
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
    except Exception as e:
     if str(e) == "[Errno -2] Name or service not known":
                print "CLEANUP:F:GERR_1401:Target Hostname unknown"
                write(logfile,'PRE:F:Target Hostname unknown [Error Code - 1401]')
     elif str(e) == "list index out of range":
                print "CLEANUP:F:GERR_1402:Argument/s missing for the script"
     elif str(e) == "Authentication failed.":
                print "CLEANUP:F:GERR_1403:Authentication failed to Target Server."
                write(logfile,'PRE:F:Authentication failed to Target Server..[Error Code - 1403]')
     elif str(e) == "[Errno 110] Connection timed out":
                print "CLEANUP:F:GERR_1404:Target Host Unreachable"
                write(logfile,'PRE:F:Target Host Unreachable[Error Code - 1404]')
     elif "getaddrinfo failed" in str(e):
                print "CLEANUP:F:GERR_1405: Please check the Target Hostname that you have provide"
                write(logfile,'PRE:F: Please check the Target Hostname that you have provide [Error Code - 1405]')
     elif "[Errno None] Unable to connect to port 22 on" in str(e):
                print "CLEANUP:F:GERR_1406:Host Unreachable or Unable to connect to port 22"
                write(logfile,'PRE:F: Host Unreachable or Unable to connect to port 22 [Error Code - 1406]')
     elif "invalid decimal" in str(e):
                print "CLEANUP:F:GERR_1407:Unknown Error:" + str(e)
                write(logfile,'PRE:F: Unknown Error:' + str(e) + '[Error Code - 1407]')
     else:
                print "CLEANUP:F: " + str(e)
###############################################################################################################

try:
    if argv[1] == "--u":
        print "usage: python cleanup.py <target Host> <target Login user> <target Login user password> <target Database SID> <logfilename>"
    else:
	logfile = argv[5] + ".log"
        cleanup(argv[1], argv[2], argv[3], argv[4],logfile)

except Exception as e:

     if str(e) == "[Errno -2] Name or service not known":
                print "CLEANUP:F:GERR_1401:Hostname unknown"
                write(logfile,'PRE:F: Hostname unknown [Error Code - 1401]')
     elif str(e) == "list index out of range":
                print "CLEANUP:F:GERR_1402:Argument/s missing for the script"
     elif str(e) == "Authentication failed.":
                print "CLEANUP:F:GERR_1403:Authentication failed."
                write(logfile,'PRE:F:Authentication failed.[Error Code - 1403]')
     elif str(e) == "[Errno 110] Connection timed out":
                print "CLEANUP:F:GERR_1404:Host Unreachable"
                write(logfile,'PRE:F:Authentication failed.[Error Code - 1404]')
     elif "getaddrinfo failed" in str(e):
                print "CLEANUP:F:GERR_1405: Please check the hostname that you have provide"
                write(logfile,'PRE:F: Please check the hostname that you have provide [Error Code - 1405]')
     elif "[Errno None] Unable to connect to port 22 on" in str(e):
                print "CLEANUP:F:GERR_1406:Host Unreachable or Unable to connect to port 22"
                write(logfile,'PRE:F: Host Unreachable or Unable to connect to port 22 [Error Code - 1406]')
     elif "invalid decimal" in str(e):
                print "CLEANUP:F:GERR_1407:Unknown Error:" + str(e)
                write(logfile,'PRE:F: Unknown Error:' + str(e) + '[Error Code - 1407]')
     else:
                print "CLEANUP:F: " + str(e)
