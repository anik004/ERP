import paramiko
from sys import *
from paramiko import *
import re
import threading 
import subprocess
import log4erp
from log4erp import *

def check(hostname,username,password,database_sid,user):
    try:

	client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect( hostname,username = username, password = password)
        channel = client.invoke_shell()

        command = "ls /oracle/" + database_sid.upper() + " >&1 /dev/null"
#	print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        status = stdout.channel.recv_exit_status()
#	print status

	command = "sudo su - ora" + database_sid.lower()+ " -c \'chmod 777 /oracle/" + database_sid.upper()  + "/sapreorg/\'"
	print command 
	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	print stdout.channel.recv_exit_status()

        if status != 0:
            print "SCP_CONTROL:F: Provided input for the database SID ( " + database_sid + " ) in " + hostname + " host is incorrect"
	    write(logfile,'POST:F: Provided input for the database SID ( ' + database_sid + ' ) in '  + hostname + ' host is incorrect')
            exit()

	channel.close()
	client.close()

    except Exception as e:
	    print "F: " + str(e)

try:
	sourcehostname = argv[1]
	sourceusername = argv[2]
	#print sourceusername
	sourcepassword = argv[3]
	sourcedatabase_sid = argv[4]
	user = "ora" + sourcedatabase_sid.lower()
	targethostname = argv[5]
	targetusername = argv[6]
	targetpassword = argv[7]
	targetdatabase_sid = argv[8].upper()
	target_db_user_passwd = argv[9]
	logfile = argv[10]

	path_array = []
	user1 = "ora" + targetdatabase_sid.lower()

	check(sourcehostname,sourceusername,sourcepassword,sourcedatabase_sid,user)
	check(targethostname,targetusername,targetpassword,targetdatabase_sid,user1)

	each = "/oracle/" + sourcedatabase_sid.upper() + "/sapreorg/control_script_" + sourcedatabase_sid.upper()+ ".sql"
	print each
	command = "expect scp_control.exp " + sourcehostname + " " + sourceusername + " " + sourcepassword + " " + targethostname + " " + user1 + " " + target_db_user_passwd + " " + each + " " + targetdatabase_sid
        print command
	command=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        out, err = command.communicate()
#	print out
	print "SCP_CONTROL:P:Control File has been transfered successfully from the source server -" + sourcehostname + " to the target server - " + targethostname
	write(logfile,"POST:P: Control File has been transfered successfully from the source server -" + sourcehostname + " to the target server - " + targethostname)

except Exception as e:
    print "F: " + str(e)
