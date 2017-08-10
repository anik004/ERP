import paramiko
from paramiko import *
from sys import *
from log4erp import *
import log4erp

# Source Host - argv[1]
# Source Login User - argv[2]
# Source User Password - argv[3]
# Source Database SID - argv[4]
# Target Database SID - argv[5]

def check(hostname,username,password,database_sid):
    try:

        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect( hostname,username = username, password = password)
        channel = client.invoke_shell()

        command = "sudo ls /oracle/" + database_sid.upper() + " >&1 /dev/null"
#       print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        status = stdout.channel.recv_exit_status()
#       print status

        if status != 0:
            print "SAPFILE:F: Provided input for the database SID ( " +  database_sid+ " ) in " + hostname + " host is incorrect"

            exit()

        channel.close()
        client.close()

    except Exception as e:
            print "F: " + str(e)

try:
#    if argv[1] == "--u":
#        print "usage: python control.py <Source Database Host> <Source Database Sudo User Name> <Source Database Sudo User Password> <Source Database SID> <Target Database SID> <Refresh ID>"
#    else:
        hostname = argv[1]
        username = argv[2]
        password = argv[3]
        s_db_sid = argv[4]
        t_db_sid = argv[5]
        refresh_id = argv[6] + ".log"

	check(hostname,username,password,s_db_sid)

        s_user = "ora" + s_db_sid.lower()
        t_user = "ora" + t_db_sid.lower()

        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname,username = username, password = password)
        channel = client.invoke_shell()
        print "CONTROL:I :Connection established Successfully with the target server (Hostname -" + hostname + ")"
        log4erp.write(refresh_id,'POST:I:Connection established Successfully with the target server (Hostname -' + hostname + ')')

        print "CONTROL:I :Updating Control File in the Source Server (Hostname -" + hostname + ")"
        log4erp.write(refresh_id,'POST:I:Updating Control File in the Source Server (Hostname -' + hostname + ')')

        command = 'sudo sed -i "s/\/oracle\/' + s_db_sid.upper() + '/\/oracle\/' + t_db_sid.upper() + '/g\" /home/' + s_user + '/control_script_' + s_db_sid.upper() + '.sql'
	print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	print stdout.channel.recv_exit_status()

        command = 'sudo sed -i \"s/' + s_db_sid.upper() + '/' + t_db_sid.upper() + '/g\" /home/' + s_user + '/control_script_' + s_db_sid.upper() + '.sql'
	print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	print stdout.channel.recv_exit_status()

        command = 'sudo sed -i \"/--/d\" /home/' + s_user + '/control_script_' + s_db_sid.upper() + '.sql'
	print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	print stdout.channel.recv_exit_status()

        command = "sudo awk '/;/{ print NR; exit }' /home/" + s_user + "/control_script_" + s_db_sid.upper() + ".sql"
	print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	print stdout.channel.recv_exit_status()

        line_no = int(stdout.readline()) + 1
        command = 'sudo sed -i \'' + str(line_no) + ',$d\' /home/' + s_user + '/control_script_' + s_db_sid.upper() + '.sql'
	print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	print stdout.channel.recv_exit_status()

        command = 'sudo sed -i \'/^$/d\' /home/' + s_user + '/control_script_' + s_db_sid.upper() + '.sql'
	print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	print stdout.channel.recv_exit_status()

        command = 'sudo sed -i \'s/NORESETLOGS/RESETLOGS/\' /home/' + s_user + '/control_script_' + s_db_sid.upper() + '.sql'
	print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	print stdout.channel.recv_exit_status()

        command = 'sudo sed -i \'s/CREATE CONTROLFILE REUSE DATABASE "' + t_db_sid.upper() + '" RESETLOGS/CREATE CONTROLFILE REUSE SET DATABASE "' + t_db_sid.upper() + '" RESETLOGS/\' /home/' + s_user + '/control_script_' + s_db_sid.upper() + '.sql'
	print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	print stdout.channel.recv_exit_status()

        if stdout.channel.recv_exit_status() == 0:
            print "CONTROL:P:The control file has been modified as per the target server configuration (HOSTNAME - " + hostname + ")"
            log4erp.write(refresh_id,'POST:P:The control file has been modified as per the target server configuration')
        else:
            print "CONTROL:F:Failed to modify the control file in the source server (HOSTNAME - " + hostname + ")"
            log4erp.write(refresh_id,'POST:F:Failed to modify the control file in the source server')

        channel.close()
        client.close()

except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "CONTROL:F:GERR_1601:Hostname unknown"
        log4erp.write(refresh_id,'POST:F: Hostname unknown [Error Code - 1601]')
    elif str(e).strip() == "list index out of range":
        print "CONTROL:F:GERR_1602:Argument/s missing for Control script"
    elif str(e) == "Authentication failed.":
        print "CONTROL:F:GERR_1603:Authentication failed."
        log4erp.write(refresh_id,'POST:F:Authentication failed[Error Code - 1603]')
    elif str(e) == "[Errno 110] Connection timed out":
        print "CONTROL:F:GERR_1604:Host Unreachable"
	log4erp.write(refresh_id,'POST:F:Host Unreachable[Error Code - 1604]')
    elif "getaddrinfo failed" in str(e):
        print "CONTROL:F:GERR_1605: Please check the hostname that you have provide"
        log4erp.write(refresh_id,'POST:F: Please check the hostname that you have provide [Error Code - 1605]')
    elif "[Errno None] Unable to connect to port 22 on" in str(e):
        print "CONTROL:F:GERR_1606:Host Unreachable or Unable to connect to port 22"
        write(refresh_id,'POST:F: Host Unreachable or Unable to connect to port 22 [Error Code - 1606]')
    else:
        print "CONTROL:F: " + str(e)
