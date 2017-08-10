from __future__ import division
from paramiko import *
import paramiko
from sys import *
import re
import log4erp
from log4erp import *

def mount(hostname, username, password, database_sid, system_name, logfile):

    user = "ora" + database_sid.lower()
    path_array = []
    total= 0

    try:
        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect( hostname,username = username, password = password)
        channel = client.invoke_shell()

	command = "ls /oracle/" + database_sid.upper() + " >&1 /dev/null"
	print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        status = stdout.channel.recv_exit_status()
	print status
	#print stdout.readlines()

        if status != 0:
            print "MOUNTPOINT:F:Provided input for the database SID ( " + database_sid + " ) in " + system_name + " host is incorrect"
            write(logfile,"PRE:F:Provided input for the database SID ( " + database_sid + " ) in " + system_name + " host is incorrect")
            exit()

	command = "ls /oracle/" + database_sid.upper() + "/sapreorg/control_script_" + database_sid.upper() + ".sql >&1 /dev/null"
        print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        status = stdout.channel.recv_exit_status()
	print status
 #       print stdout.readlines()

	if status == 0:
            #command = "sudo su - " + user + " -c \'mv -f /home/" + user + "/control_script_" + database_sid.upper() + ".sql /home/" + user + "/control_script_" + database_sid.upper() + ".bkp.sql\'"
	    
            command = "mv -f /oracle/" + database_sid.upper() + "/sapreorg/control_script_" + database_sid.upper() + ".sql /oracle/" + database_sid.upper() + "/sapreorg/control_script_" + database_sid.upper() + ".bkp.sql"
            print command
            stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
            status = stdout.channel.recv_exit_status()
            print status
	    
	command = 'sudo su - ' + user + ' -c "echo \'alter database backup controlfile to trace as \'\\\'/oracle/' + database_sid.upper() + '/sapreorg/control_script_' + database_sid.upper() + '.sql\\\'\';\' > /oracle/' + database_sid.upper() + '/sapreorg/sql.sql;chmod 777 /oracle/' + database_sid.upper() + '/sapreorg/sql.sql"'
	print command
	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	status = stdout.channel.recv_exit_status()
	print status

	command = 'sudo su - ' + user + ' -c "echo @/oracle/' + database_sid.upper() + '/sapreorg/sql.sql | sqlplus / as sysdba" | grep -i "ERROR"'
	print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        if stdout.readlines():
                print "MOUNTPOINT:F: The database is not available in the " + system_name + " host ( " + hostname + ")"
                write(logfile,"PRE:F:The database is not available in the " + system_name + " host ( " + hostname + ")")
                exit()
        status = stdout.channel.recv_exit_status()

	sftp_client = client.open_sftp()
        command = '/oracle/' + database_sid.upper() + '/sapreorg/control_script_' + database_sid.upper() + '.sql' # | grep -i "sapdata*"' # variable IN
#        print command
        remote_file = sftp_client.open(command)
        remote_file = list(set(remote_file))
#	print remote_file

	for line in remote_file:
		paths = ""
#		print line
		if "ALTER" not in line:
                        if re.search("sapdata", line):
                                directory = line.split("/")
				#print directory
				for dire in directory:
#					print "dire"
	#				print dire
                                        if "sapdata" in dire:
                                                paths = str(paths) + "/" + str(dire)
	#					print paths
						break
                                        else:
                                                paths = str(paths) + "/" + str(dire)
	#					print paths

				path_array.append(paths[4:])

	path_array = list(set(path_array))
        #print path_array	

	for each in path_array:
                command = "du -sh "+ each + " | awk '{print $1}'"    # du -sg for size in gb in AIX system
		#print command
                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
                output = stdout.readline().rstrip()
        #        print output

		if output.rstrip()[-1] == "M":
                        total = float(total) + (float(output[:-1]) / 1024)
                else:
                        total = float(total) + float(output[:-1])

	
	return float(total)
	
	channel.close()
	client.close()

    except Exception as e:
	if str(e) == "[Errno -2] Name or service not known":
                print "MOUNTPOINT:F:GERR_1101:Hostname unknown for " + system_name + " server (" + hostname + ")"
                write(logfile,'PRE:F:Hostname unknown [Error Code - 1101] for ' + system_name + ' server (' + hostname + ')')
                exit()
        elif str(e) == "list index out of range":
                print "MOUNTPOINT:F:GERR_1102:Argument/s missing for the script"
        elif str(e) == "Authentication failed.":
                print "MOUNTPOINT:F:GERR_1103:Authentication failed for " + system_name + " server (" + hostname + ")"
                write(logfile,'PRE:F:Authentication failed for .' + system_name + ' server (' + hostname + ') [Error Code - 1103]')
                exit()
        elif str(e) == "[Errno 110] Connection timed out":
                print "MOUNTPOINT:F:GERR_0504: " + system_name + " Host Unreachable (" + hostname + ")"
                write(logfile,'PRE:F:GERR_0504: ' + system_name + ' Host Unreachable (' + hostname + ')')
                exit()
        elif "getaddrinfo failed" in str(e):
                print "MOUNTPOINT:F:GERR_0505: Please check the " + system_name + " hostname that you have provide (" + hostname + ")"
                write(logfile,'PRE:F:GERR_0505: Please check the ' + system_name + ' hostname that you have provide (' + hostname + ')')
                exit()
        elif "[Errno None] Unable to connect to port 22 on" in str(e):
                print "MOUNTPOINT:F:GERR_0506: " + system_name + "Host Unreachable or Unable to connect to port 22 (" + hostname + ")"
                write(logfile,'PRE:F:GERR_0506: ' + system_name + 'Host Unreachable or Unable to connect to port 22 (' + hostname + ')')
        elif "invalid decimal" in str(e):
                print "MOUNTPOINT:F:GERR_0507:Unknown Error:" + str(e)
                write(logfile,'PRE:F:GERR_0507:Unknown Error:' + str(e))
        else:
                print "MOUNTPOINT:F:" + str(e)


try:
    if argv[1] == "--u":
        print "usage: python mountpoint.py <source Database Host> <source Database Sudo user> <source database Sudo user password> <source Database SID> <Source> <target database Host> <target database Login user> <target database user password> <target Database SID> <Target> <Refresh ID>"
    else:
	logfile = argv[11]

	source_server = mount(argv[1], argv[2], argv[3], argv[4], argv[5], logfile)
#	print source_server

	target_server = mount(argv[6], argv[7], argv[8], argv[9], argv[10], logfile)
 #       print target_server

	client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect( argv[6],username = argv[7], password = argv[8])
        channel = client.invoke_shell()

	command = "df -m | awk '{s+=$4} END {print s}'"
#	print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        free_space = int(stdout.readline()) / 1024
 #       print free_space
        total_space = free_space + target_server
  #      print total_space

	if total_space >= source_server:
            print "MOUNTPOINT:P: There is enough space available in the target database server for DB Refresh"
            log = "PRE:P:There are enough space available in the target database server for DB Refresh"
            write(logfile,log)
        else:
            print "MOUNTPOINT:F: There is no enough space available in the target database server for DB Refresh"
	    log = "PRE:F:There are no enough space available in the target database server for DB Refresh"
            write(logfile,log)

        channel.close()
        client.close()


except Exception as e:
	if str(e) == "[Errno -2] Name or service not known":
                print "MOUNTPOINT:F:GERR_1101:Hostname unknown"
                write(logfile,'PRE:F:Hostname unknown [Error Code - 1101]')
        elif str(e) == "list index out of range":
                print "MOUNTPOINT:F:GERR_1102:Argument/s missing for the script"
        elif str(e) == "Authentication failed.":
                print "MOUNTPOINT:F:GERR_1103:Authentication failed."
                write(logfile,'PRE:F:Authentication failed.[Error Code - 1103]')
        elif str(e) == "[Errno 110] Connection timed out":
                print "MOUNTPOINT:F:GERR_0504:Host Unreachable"
                write(logfile,'PRE:F:GERR_0504:Host Unreachable')
        elif "getaddrinfo failed" in str(e):
                print "MOUNTPOINT:F:GERR_0505: Please check the hostname that you have provide"
                write(logfile,'PRE:F:GERR_0505: Please check the hostname that you have provide')
        elif "[Errno None] Unable to connect to port 22 on" in str(e):
                print "MOUNTPOINT:F:GERR_0506:Host Unreachable or Unable to connect to port 22"
                write(logfile,'PRE:F:GERR_0506:Host Unreachable or Unable to connect to port 22')
        elif "invalid decimal" in str(e):
                print "MOUNTPOINT:F:GERR_0507:Unknown Error:" + str(e)
                write(logfile,'PRE:F:GERR_0507:Unknown Error:' + str(e))
        else:
                print "MOUNTPOINT:F:" + str(e)
