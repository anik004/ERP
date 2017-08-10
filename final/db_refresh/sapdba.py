import paramiko
import numpy as np
from paramiko import *
from sys import *
from log4erp import *
import log4erp

try:
    if argv[1] == "--u":
        print "python sapdba.py <Target database Host> <Target database Sudo User Name> <Target Database Sudo User Password> <Target Database SID> <source app sid> <source db sid> <Refresh ID"
    else:
        hostname = argv[1]
        username = argv[2]
        password = argv[3]
        db_sid = argv[4]
	s_app_sid = argv[5]
	s_db_sid = argv[6]
        refresh_id = argv[7] + ".log"

        user = "ora" + argv[4].lower()
        s_db_user= "ora" + argv[6].lower()
	s_app_user = argv[5].lower() + "adm"
	ops_app_user = "OPS$" + s_app_user.upper()
	ops_db_user = "OPS$" + s_db_user.upper()
#	print ops_app_user


        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname,username = username, password = password)
        channel = client.invoke_shell()
        print "SAPDBA:I: Connection established Successfully (Hostname -" + hostname + ")"
        log4erp.write(refresh_id,'POST:I: Connection established Successfully (Hostname -' + hostname + ')')

	command = 'sudo su - ' + user + ' -c \'echo "select username from dba_users;" | sqlplus / as sysdba\''
	#print command
	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	out = stdout.readlines()
#	print out
	exist = out[0]
	if "does not exist" in exist:
		print "SAPDBA:F: Target Database SID entered by the user - " + db_sid + " is incorrect"
		log4erp.write(refresh_id,"POST:F: Target Database SID entered by the user - " + db_sid + " is incorrect")
		exit()

	myarray = np.asarray(out)


	for users in myarray:
		b = users.encode('UTF8')
		if b.strip() == ops_app_user :
			command = "sudo su - " + user + " -c \"echo \'drop user \"OPS\$" + s_app_user.upper() + "\" cascade;' | sqlplus / as sysdba\""
		#	print command
			stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
			if stdout.channel.recv_exit_status() != 0:
				print "SAPDBA:F: Failed to delete the " + b.strip() + " user from the Target Database (Hostname -" + hostname + ")"
				log4erp.write(refresh_id,'POST:F: Failed to delete the ' + b.strip() + " user from the Target Database (Hostname -" + hostname + ")")
				exit()
		if b.strip() == ops_db_user :
			command = "sudo su - " + user + " -c \"echo \'drop user \"OPS\$" + s_db_user.upper() + "\" cascade;' | sqlplus / as sysdba\""
		#	print command
                        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
                        if stdout.channel.recv_exit_status() != 0:
                                print "SAPDBA:F: Failed to delete the " + b.strip() + " user from the Target Database (Hostname -" + hostname + ")"
                                log4erp.write(refresh_id,'POST:F: Failed to delete the ' + b.strip() + " user from the Target Database (Hostname -" + hostname + ")")
                                exit() 

	command = 'sudo su - ' + user + ' -c \'echo $dbs_ora_schema\''
#	print command
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        if stdout.channel.recv_exit_status() == 0:
            print "SAPDBA:I: Fetching the Schema user name from Target (Hostname -" + hostname + ")"
            log4erp.write(refresh_id,'POST:I: Fetching the Schema user name from Target (Hostname -' + hostname + ')')
            schema = stdout.readline().rstrip()
#	    print schema

            command = 'sudo su - ' + user + ' -c \"cdexe; sqlplus /nolog @sapdba_role.sql ' + schema + '_user UNIX\"'
#	    print command
            stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)

            if stdout.channel.recv_exit_status() == 0:
                print "SAPDBA:P: The SAPDBA role updation has been successful on the target server (HOSTNAME - " + hostname + ")"
                log4erp.write(refresh_id,'POST:P: The SAPDBA role updation has been successful on the target server (HOSTNAME - ' + hostname + ')')
            else:
                print "SAPDBA:F:The SAPDBA role updation has been failed on the target server (HOSTNAME - " + hostname + ")"
                log4erp.write(refresh_id,'POST:F: The SAPDBA role updation has been failed on the target server (HOSTNAME -' + hostname + ')')
        else:
            print "SAPDBA:F: Not able to fetch the Schema user name from Target (Hostname -" + hostname + ")"
            log4erp.write(refresh_id,'POST:F: Not able to fetch the Schema user name from Target (Hostname -' + hostname + ')') 

        channel.close()
        client.close()

except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "SAPDBA:F:GERR_2801:Target Hostname unknown - " + hostname
        log4erp.write(refresh_id,'POST:F: Target Hostname unknown - ' + hostname + ' [Error Code - 2801]')
    elif str(e).strip() == "list index out of range":
        print "SAPDBA:F:GERR_2802:Argument/s missing for SAPDBA script"
    elif str(e) == "Authentication failed.":
        print "SAPDBA:F:GERR_2803:Authentication failed to the Target Server - " + hostname
        log4erp.write(refresh_id,'POST:F:Authentication failed to the Target Server - ' + hostname + ' [Error Code - 2803]')
    elif str(e) == "[Errno 110] Connection timed out":
        print "SAPDBA:F:GERR_2804:Target Host Unreachable"
	write(refresh_id,'POST:F:Target Host Unreachable.[Error Code - 2804]')
    elif "getaddrinfo failed" in str(e):
        print "SAPDBA:F:GERR_2805: Please check the target hostname that you have provide"
        log4erp.write(refresh_id,'POST:F: Please check the target hostname that you have provide [Error Code - 2805]')
    elif "[Errno None] Unable to connect to port 22 on" in str(e):
        print "SAPDBA:F:GERR_2806:Host Unreachable or Unable to connect to port 22"
        write(refresh_id,'POST:F: Host Unreachable or Unable to connect to port 22 [Error Code - 2806]')
    else:
        print "SAPDBA:F: " + str(e)
	write(refresh_id,'POST:F: ' + str(e))
