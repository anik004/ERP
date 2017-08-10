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

def check(hostname,username,password,database_sid,logfile):
    try:

        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect( hostname,username = username, password = password)
        channel = client.invoke_shell()

        command = "ls /oracle/" + database_sid.upper() + " >&1 /dev/null"
#       print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        status = stdout.channel.recv_exit_status()
#       print status

        if status != 0:
            print "SAPFILE:F: Provided input for the database SID ( " +  database_sid+ " ) in " + hostname + " host is incorrect"
	    log4erp.write(logfile,"POST:F: Provided input for the database SID ( " +  database_sid+ " ) in " + hostname + " host is incorrect")
            exit()

        channel.close()
        client.close()

    except Exception as e:
     if str(e) == "[Errno -2] Name or service not known":
                print "CONTROL:F:GERR_1201:Hostname unknown for Target Server (" + hostname + ")"
                write(logfile,'POST:F:Hostname unknown for Target Server (' + hostname + ')[Error Code - 1201]')
     elif str(e) == "list index out of range":
                print "CONTROL:F:GERR_1202:Argument/s missing for the script"
     elif str(e) == "Authentication failed.":
                print "CONTROL:F:GERR_1203:Authentication failed to the Target Server (" + hostname + ")"
                write(logfile,'POST:F:Authentication failed to the Target Server (' + hostname + ')[Error Code - 1203]')
     elif str(e) == "[Errno 110] Connection timed out":
                print "CONTROL:F:GERR_1204:Target Host Unreachable (" + hostname + ")"
                write(logfile,'POST:F:Target Host Unreachable (' + hostname + ') [Error Code - 1204]')
     elif "getaddrinfo failed" in str(e):
                print "CONTROL:F:GERR_1205: Please check the Target Hostname - " + hostname + " that you have provide"
                write(logfile,'POST:F:Please check the Target Hostname - ' + hostname + ' that you have provide [Error Code - 1205]')
     elif "[Errno None] Unable to connect to port 22 on" in str(e):
                print "CONTROL:F:GERR_1206:Host Unreachable or Unable to connect to port 22"
                write(logfile,'POST:F:Host Unreachable or Unable to connect to port 22 [Error Code - 1206]')
     elif "invalid decimal" in str(e):
                print "CONTROL:F:GERR_1207:Unknown Error:" + str(e)
                write(logfile,'POST:F:Unknown Error:' + str(e) + '[Error Code - 1207]')
     else:
                print "CONTROL:F:" + str(e)
                write(logfile,'POST:F:' + str(e))

try:
    if argv[1] == "--u":
        print "usage: python control.py <Target Database Host> <target Database Sudo User Name> <target Database Sudo User Password> <source Database SID> <Target Database SID> <Refresh ID>"
    else:
        hostname = argv[1]
        username = argv[2]
        password = argv[3]
        s_db_sid = argv[4]
        t_db_sid = argv[5]
        logfile = argv[6] + ".log"

	check(hostname,username,password,t_db_sid,logfile)

        s_user = "ora" + s_db_sid.lower()
        t_user = "ora" + t_db_sid.lower()

        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname,username = username, password = password)
        channel = client.invoke_shell()
        print "CONTROL:I :Connection established Successfully with the target server (Hostname -" + hostname + ")"
        log4erp.write(logfile,'POST:I:Connection established Successfully with the target server (Hostname -' + hostname + ')')

        print "CONTROL:I :Updating Control File in the Source Server (Hostname -" + hostname + ")"
        log4erp.write(logfile,'POST:I:Updating Control File in the Source Server (Hostname -' + hostname + ')')

#	command = 'sudo sed -i "s/\/oracle\/' + s_db_sid.upper() + '/\/oracle\/' + t_db_sid.upper() + '/g\" /home/' + t_user + '/scp/control_script_' + s_db_sid.upper() + '.sql'
#        print command
#        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
#        print stdout.channel.recv_exit_status()

########################################################## REPLACING SOURCE DB SID WITH TARGET DB SID #################################

	command = "sudo su - ora" + t_db_sid.lower() + " -c \'chmod 777 /oracle/" + t_db_sid.upper() + "/sapreorg/control_script_" + s_db_sid.upper() + ".sql\'"
	print command
	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        print stdout.channel.recv_exit_status()
	command = 'sed -i \"s/' + s_db_sid.upper() + '/' + t_db_sid.upper() + '/g\" /oracle/' + t_db_sid.upper() + '/sapreorg/control_script_' + s_db_sid.upper() + '.sql'
        print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        print stdout.channel.recv_exit_status()

########################################################### DELETING UNNECESARY LINES ###########################################

	command = 'sed -i \"/--/d\" /oracle/' + t_db_sid.upper() + '/sapreorg/control_script_' + s_db_sid.upper() + '.sql'
        print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        print stdout.channel.recv_exit_status()

########################################################## CHECKING THE ; POSITION AND DELETING LINES AFTER THAT LINE  #############################################

	command = "awk '/;/{ print NR; exit }' /oracle/" + t_db_sid.upper() + "/sapreorg/control_script_" + s_db_sid.upper() + ".sql"
        print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	
        print stdout.channel.recv_exit_status()
	
	line_no = int(stdout.readline())
	print line_no
	line_no = line_no + 1
	print line_no
        command = 'sed -i \'' + str(line_no) + ',$d\' /oracle/' + t_db_sid.upper() + '/sapreorg/control_script_' + s_db_sid.upper() + '.sql'
        print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        print stdout.channel.recv_exit_status()

######################################################## DELETING EMPTY LINES ########################################

	command = 'sed -i \'/^$/d\' /oracle/' + t_db_sid.upper() + '/sapreorg/control_script_' + s_db_sid.upper() + '.sql'
        print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        print stdout.channel.recv_exit_status()

######################################################## CHANGING NORESETLOG TO RESETLOG #########################

	command = 'sed -i \'s/NORESETLOGS/RESETLOGS/\' /oracle/' + t_db_sid.upper() + '/sapreorg/control_script_' + s_db_sid.upper() + '.sql'
        print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        print stdout.channel.recv_exit_status()

######################################################## CHANGING REUSE TO REUSE SET ###############################

	command = 'sed -i \'s/CREATE CONTROLFILE REUSE DATABASE "' + t_db_sid.upper() + '" RESETLOGS/CREATE CONTROLFILE REUSE SET DATABASE "' + t_db_sid.upper() + '" RESETLOGS/\' /oracle/' + t_db_sid.upper() + '/sapreorg/control_script_' + s_db_sid.upper() + '.sql'
        print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        print stdout.channel.recv_exit_status()

        if stdout.channel.recv_exit_status() == 0:
	    command = "mv -f /oracle/" + t_db_sid.upper() + "/sapreorg/control_script_" + s_db_sid.upper() + ".sql /oracle/" + t_db_sid.upper() + "/sapreorg/control_script_" + t_db_sid.upper() + ".sql"
#	    print command
            stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
            print stdout.channel.recv_exit_status()
	    if stdout.channel.recv_exit_status() == 0:
	            print "CONTROL:P:The control file has been modified as per the target server configuration (HOSTNAME - " + hostname + ")"
        	    log4erp.write(logfile,'POST:P:The control file has been modified as per the target server configuration')
            else:
    	            print "CONTROL:F:Failed to modify the control file in the source server (HOSTNAME - " + hostname + ")"
            	    log4erp.write(logfile,'POST:F:Failed to modify the control file in the source server')

        channel.close()
	client.close()

except Exception as e:
     if str(e) == "[Errno -2] Name or service not known":
                print "CONTROL:F:GERR_1201:Hostname unknown for Target Server (" + hostname + ")"
                write(logfile,'POST:F:Hostname unknown for Target Server (' + hostname + ')[Error Code - 1201]')
     elif str(e) == "list index out of range":
                print "CONTROL:F:GERR_1202:Argument/s missing for the script"
     elif str(e) == "Authentication failed.":
                print "CONTROL:F:GERR_1203:Authentication failed to the Target Server (" + hostname + ")"
                write(logfile,'POST:F:Authentication failed to the Target Server (' + hostname + ')[Error Code - 1203]')
     elif str(e) == "[Errno 110] Connection timed out":
                print "CONTROL:F:GERR_1204:Target Host Unreachable (" + hostname + ")"
                write(logfile,'POST:F:Target Host Unreachable (' + hostname + ') [Error Code - 1204]')
     elif "getaddrinfo failed" in str(e):
                print "CONTROL:F:GERR_1205: Please check the Target Hostname - " + hostname + " that you have provide"
                write(logfile,'POST:F:Please check the Target Hostname - ' + hostname + ' that you have provide [Error Code - 1205]')
     elif "[Errno None] Unable to connect to port 22 on" in str(e):
                print "CONTROL:F:GERR_1206:Host Unreachable or Unable to connect to port 22"
                write(logfile,'POST:F:Host Unreachable or Unable to connect to port 22 [Error Code - 1206]')
     elif "invalid decimal" in str(e):
                print "CONTROL:F:GERR_1207:Unknown Error:" + str(e)
                write(logfile,'POST:F:Unknown Error:' + str(e) + '[Error Code - 1207]')
     else:
                print "CONTROL:F:" + str(e)
		write(logfile,'POST:F:' + str(e))
