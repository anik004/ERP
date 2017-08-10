from paramiko import *
import paramiko
from sys import *
import log4erp
from log4erp import *
from time import gmtime, strftime


try:
    if argv[1] == "--u":
        print "usage: python sapdelete.py <Application Hostname> <Sudo User Name> <Sudo user password> <Application SID> <Client Name> <Target/Source>"
    else:
        hostname = argv[1]
        username = argv[2]
        password = argv[3]
        application_sid = argv[4]
        user = "ora" + application_sid
        clientname = argv[5]
	logfile = "geminyo.txt"

        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect( hostname,username = username, password = password)
        channel = client.invoke_shell()

        command = 'sudo su - ' + user + ' -c \'echo $dbs_ora_schema\''
	print command
	write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
        stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	output = stdout.readlines()
	write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
        output = ''.join(output).strip()
        #print output
        if stdout.channel.recv_exit_status() == 0:
            #DELETE SAP<SID>.usr02 where mandt='CLIENT.NO' and bname=SAP
            command = 'sudo su - ' + user + ' -c "echo \'delete '+ output + '.usr02 where mandt=' + clientname + ' and bname=\'\\\'SAP\\*\\\'\';\' | sqlplus / as sysdba"'
            print command
	    write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
            stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
            if stdout.channel.recv_exit_status() == 0:
                print "POST:P: password reseted successfully for sap* in  server ( Hostname - " + hostname + " )"
		write(logfile, "POST:P: password reseted successfully for sap* in  server ( Hostname - " + hostname + " )" + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
            else:
                print "POST:F: password reset failed for sap* in server ( Hostname - " + hostname + " )"
		write(logfile, "POST:F: password reset failed for sap* in server ( Hostname - " + hostname + " )")
	else:
	    print "POST:F: password reset failed for sap* in server ( Hostname - " + hostname + " )"
	    write(logfile, "POST:F: password reset failed for sap* in server ( Hostname - " + hostname + " )")

	channel.close()
        client.close()

except Exception as e:
    print "POST:F: " + str(e)
