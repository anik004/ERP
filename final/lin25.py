from paramiko import *
import paramiko
from sys import *
import log4erp
from log4erp import *
from time import gmtime, strftime

try:
    if argv[1] == "--u":
        print "usage: python ddic_setzero.py <Application Hostname> <Root User Name> <Root user password> <Application SID> <Target/Source>"
    else:

        hostname = argv[1]
        username = argv[2]
        password = argv[3]
        application_sid = argv[4].lower()
	profile_path = argv[5]
        user = application_sid.lower() + "adm"
	logfile = "geminyo.txt"

        client = SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect( hostname,username = username, password = password)
        channel = client.invoke_shell()

        command = 'sudo su - ' + user + ' -c \'cd ' + profile_path + ';ls | grep -i "' + application_sid.upper() + '_DVEBMGS" | grep -v "\."\''
        print command
	#write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	output = stdout.readlines()
	#write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
        profilefile = ''.join(output).strip()

        command = 'sudo su - ' + user + ' -c \'cd ' + profile_path + ';cat ' + profilefile + ' | grep -iw "login/no_automatic_user_sapstar" | grep -v "#"\''
        print command
	#write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
	stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
        output = stdout.readlines()
	#write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')

        if not output:
            command = 'sudo su - ' + user + ' -c \'cd ' + profile_path + ';echo "login/no_automatic_user_sapstar = 0" >> ' + profilefile + '\''
	    print command
	    #write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
            stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
	    output = stdout.readlines()
	    #write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
            if stdout.channel.recv_exit_status() == 0:
                print "PRE:P: Parameter set to 0"
		#write(logfile, "PRE:P: Parameter set to 0" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
            else:
                print "PRE:F: Parameter change failed"
		#write(logfile, "PRE:F: Parameter change failed" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
        elif output.__len__() == 1:
            output = ''.join(output).strip()
            output = output.replace('/','\/')
            command = 'sudo su - ' + user + ' -c \'cd ' + profile_path + ';sed "s/' + output + '/login\/no_automatic_user_sapstar = 0/g" ' + profilefile + ' >> /home/' + application_sid.lower() + 'adm/paramstar.txt \''
	    print command
	    #write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
            stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
            output = stdout.readlines()
	    #write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
	
            if stdout.channel.recv_exit_status() == 0:
		command = 'sudo su - ' + user + ' -c \'cd ' + profile_path + ';pwd \''
		print command
		#write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
		stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
		output = stdout.readlines()
		#write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
		output = output[0]
		command = 'sudo mv /home/' + application_sid.lower() + 'adm/paramstar.txt ' + output.strip()+ '/' + profilefile
		print command
		#write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
                stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
                output = stdout.readlines()
		#write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
		if stdout.channel.recv_exit_status() == 0:
                	print "PRE:P: Parameter set to 0"
			#write(logfile, "PRE:P: Parameter set to 0" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
			command = "sudo rm /home/" + application_sid.lower() + "adm/paramstar.txt"
			#write(logfile, command + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
			stdin, stdout, stderr = client.exec_command(command, timeout=1000, get_pty=True)
			output = stdout.readlines()
			#write(logfile, str(output) + ': " ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
		else:
			print "PRE:F: Parameter change failed"
			#write(logfile, "PRE:F: Parameter change failed" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
            else:
                print "PRE:F: Parameter change failed"
		#write(logfile, "PRE:F: Parameter change failed" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')
        else:
	    print "PRE:F: Parameter change failed"
	    #write(logfile, "PRE:F: Parameter change failed" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' "')

        channel.close()
        client.close()

except Exception as e:
    print "F: " + str(e)
