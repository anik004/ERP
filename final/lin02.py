from __future__ import division
from paramiko import *
import paramiko
from sys import *
import re
#from log4erp import *


def mount(hostname, username, password, database_sid):

    user = "ora" + database_sid.lower()
    path_array = []
    total= 0

    try:
#	database_sid=argv[2]

        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect( hostname,username = username, password = password)
        channel = client.invoke_shell()

	command = "sudo ls /oracle/" + database_sid.upper() + " >&1 /dev/null"
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        status = stdout.channel.recv_exit_status()

        if status != 0:
	    print "PRE:F: Provided input for the database SID ( " + database_sid +  " ) is incorrect"
	    exit()

        command = "sudo ls /home/" + user + "/control_script_" + database_sid.upper() + ".sql >&1 /dev/null"
        #print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        status = stdout.channel.recv_exit_status()
	#print status
        if status == 0:
            command = "sudo mv /home/" + user + "/control_script_" + database_sid.upper() + ".sql /home/" + username + "/control_script_" + database_sid.upper() + ".bkp.sql"
            #print command
	    stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
            status = stdout.channel.recv_exit_status()
            #print status

	command = 'sudo su - ' + user + ' -c "echo \'alter database backup controlfile to trace as \'\\\'/home/' + user + '/control_script_' + database_sid.upper() + '.sql\\\'\';\' > /home/' + user + '/sql.sql;chmod 777 /home/' + user + '/sql.sql"'
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	status = stdout.channel.recv_exit_status()

	command = 'sudo su - ' + user + ' -c "echo @/home/' + user + '/sql.sql | sqlplus system/Welcome2" | grep --color=never -i "ERROR:"'
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	if stdout.readlines():
		print "PRE:F: The database is not available in the host ( " + hostname + ")"
		exit()
	status = stdout.channel.recv_exit_status()

#	command = "sudo su -" + user + " -c ' mv /home/" + user + "/control_script_" + database_sid.upper() + ".sql /home/" + username + "/control_script_" + database_sid.upper() + ".sql'"
	#print command
#	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
#       #status = stdout.channel.recv_exit_status()

	command = "sudo ls /home/" + user + "/control_script_" + database_sid.upper() + ".sql >&1 /dev/null"
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        status = stdout.channel.recv_exit_status()
	#print status
        if status != 0:
#	    print "PRE:F: The control file has not been generated on the target database server (HOSTNAME - " + hostname + ")"
	    mount(argv[1], argv[2], argv[3], argv[4])
	else:
            sftp_client = client.open_sftp()
            command = '/home/' + user + '/control_script_' + database_sid.upper() + '.sql' # | grep -i "sapdata*"' # variable IN
	    #print command
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
        #print path_array

        for each in path_array:
		command = "sudo du -sh "+ each + " | awk '{print $1}'"
            	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
            	output = stdout.readline().rstrip()
            	if output.rstrip()[-1] is "M":
                	total = float(total) + float(output[:-1]) / 1024
			#print hostname + str(total)
            	else:
                	total = float(total) + float(output[:-1])
			#print hostname + str(total)

        command = 'sudo rm -rf /home/' + user + '/sql.sql; sudo rm -rf /home/' + user + '/control_script_' + database_sid.upper() + '.sql '
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        return float(total)

    except Exception as e:
	if str(e) == "'decimal' codec can't encode character u'\u2018' in position 18: invalid decimal Unicode string":
	    print "PRE:F: The proper data is not available in the system"
	    exit()
	else:
            print "F: " + str(e)


try:
        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        hostname = argv[5]
        username = argv[6]
        password = argv[7]
        client.connect( hostname,username = username, password = password)
        channel = client.invoke_shell()
        source_server = mount(argv[1], argv[2], argv[3], argv[4])
        target_server = mount(argv[5], argv[6], argv[7], argv[8])
        command = "sudo df -m | awk '{s+=$4} END {print s}'"
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        free_space = int(stdout.readline()) / 1024
        total_space = free_space + target_server
        if total_space >= source_server:
            print "PRE:P: There is enough space available in the target database server for DB Refresh"
        else:
            print "PRE:F: There is no enough space available in the target database server for DB Refresh"

        channel.close()
        client.close()

except Exception as e:
     if str(e) == "[Errno -2] Name or service not known":
                print "PRE:F:GERR_0501:Hostname unknown"
     elif str(e) == "list index out of range":
                print "PRE:F:GERR_0502:Argument/s missing for the script"
     elif str(e) == "Authentication failed.":
                print "PRE:F:GERR_0503:Authentication failed."
     elif str(e) == "[Errno 110] Connection timed out":
                print "PRE:F:GERR_0504:Host Unreachable"
     elif "getaddrinfo failed" in str(e):
                print "PRE:F:GERR_0505: Please check the hostname that you have provide"
     elif "[Errno None] Unable to connect to port 22 on" in str(e):
                print "PRE:F:GERR_0506:Host Unreachable or Unable to connect to port 22"
     elif "invalid decimal" in str(e):
		print "PRE:F:GERR_0507:Unknown Error:" + str(e)
     else:
                print "PRE:F: " + str(e)

