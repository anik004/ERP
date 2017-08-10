import paramiko
from paramiko import *
from sys import *

# target IP - argv[1]
# Login User Name - argv[2]
# Login User Password - argv[3]
# Database SID - argv[4]

try:
    #if argv[1] == "--u":
     #   print "python db_sys.py <DB Host> <DB Sudo Login User Name> <DB Sudo Login User Password> <DB SID> <SYSTEM User Password> <Target/Source>"
    #else:
        hostname = argv[1]
        username = argv[2]
        password = argv[3]
        db_sid = argv[4]
#	db_username = argv[5]
#       db_password = argv[6]

        user = "ora" + argv[4].lower()
	loc = argv[7].rstrip('/')
	refid = argv[8]

        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname,username = username, password = password)
        channel = client.invoke_shell()

        schema = 'sudo su - ' + user + ' -c \'echo $dbs_ora_schema\''
	#print schema
        stdin, stdout, stderr = client.exec_command(schema, timeout=1000, get_pty=True)
        schema = stdout.readline().rstrip()
        command = "sudo su - " + user + " -c \"echo '@bdls.sql' | sqlplus / as sysdba\""
	print command
	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	status = stdout.channel.recv_exit_status()
	output = stdout.readlines()
#	print output[11]
#	print output[len(output)-7]
#	print status
#	print output
        if status == 0:
#            print "PRE:F: The database user ( " + argv[5] + " ) is not able to login to the server (HOSTNAME - " + hostname + ")"
	    for i in range(11,len(output)-7):
		if "TABNAME" not in output[i].strip() and "-" not in output[i].strip() and output[i].strip() and "FIELDNAME" not in output[i].strip():
		    		table = output[i].split()
				table_name = table[0]
				field_name = table[1].strip()
#				print table_name
				#print table[1]
				if "/" not in table_name:
					command = 'sudo su - ' + user + ' -c "echo \'drop index ' + table_name + '_' + field_name + ';\' | sqlplus / as sysdba"'
					#print command
					#f.write(command + '\n')
						
        				stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        				status = stdout.channel.recv_exit_status()
        				out = stdout.readlines()
					if status != 0:
						print 'PRE:F:bitmap index drop failed'
						exit()
	    print 'PRE:P:bitmap index dropped successfully'
					
        else:
            print "PRE:P: The database user ( " +  argv[5] + " ) is able to login to the server (HOSTNAME - " + hostname + ")"

except Exception as e:
    if str(e) == "[Errno -2] Name or service not known":
        print "PRE:F:GERR_0701:Hostname unknown"
    elif str(e) == "list index out of range":
        print "PRE:F:GERR_0702:Argument/s missing for the script"
    elif str(e) == "Authentication failed.":
        print "PRE:F:GERR_0703:Authentication failed."
    elif str(e) == "[Errno 110] Connection timed out":
        print "PRE:F:GERR_0704:Host Unreachable"
    elif "getaddrinfo failed" in str(e):
        print "PRE:F:GERR_0705: Please check the hostname that you have provide"
    elif "[Errno None] Unable to connect to port 22 on" in str(e):
        print "PRE:F:GERR_0706:Host Unreachable or Unable to connect to port 22"
    elif "invalid decimal" in str(e):
        print "PRE:F:GERR_0707:Unknown Error:" + str(e)
    else:
        print "PRE:F: " + str(e)

